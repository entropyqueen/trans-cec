(function () {
    function Memory() {
        var isOn = JSON.parse(localStorage.getItem('memory'));
        var dom = {
            picto: document.getElementById('save'),
            forms: []
        };
        return {
            init: init,
            prepare: prepare
        };

        function clear() {
            if (confirm("Effacer toutes les données personnelles enregistrées ?")) {
                localStorage.removeItem('profile');
            }
        }

        function fill(form) {
            if (isOn) {
                var data = JSON.parse(localStorage.getItem('profile')) || {};
                var inputs = getInputs(form);
                for (var i = 0; i < inputs.length; i++) {
                    var key = inputs[i].id;
                    if (key != undefined && data[key] != undefined) {
                        inputs[i].value = data[key];
                    }
                }
            }
        }

        function getInputs(form) {
            var inputs = Array.prototype.slice.call(form.getElementsByTagName('input'));
            var selects = Array.prototype.slice.call(form.getElementsByTagName('select'));
            return inputs.filter(function(input) { return input.type != "hidden"; })
                .concat(selects);
        }

        function init() {
            dom.picto.classList.toggle('active', isOn);
            dom.picto.addEventListener('click', toggle);
            document.getElementById('forget').addEventListener('click', clear);
        }

        function prepare(form) {
            fill(form);
            form.querySelector('button[type=submit]')
                .addEventListener('click', save(form));
            form.save.addEventListener('click', toggle);
            form.forget.addEventListener('click', clear);
            var spans = {
                enable: form.save.querySelector('.enable'),
                disable: form.save.querySelector('.disable')
            };
            spans[isOn ? 'disable' : 'enable'].classList.add('on');
            dom.forms.push(spans);
        }

        function save(form) {
            return function() {
                if (isOn) {
                    var data = JSON.parse(localStorage.getItem('profile')) || {};
                    var inputs = getInputs(form);
                    for (var i = 0; i < inputs.length; i++) {
                        var key = inputs[i].id;
                        if (key != undefined && inputs[i].checkValidity()) {
                            data[key] = inputs[i].value;
                        }
                    }
                    localStorage.setItem('profile', JSON.stringify(data));
                }
            };
        }

        function toggle() {
            isOn = !isOn;
            dom.picto.classList.toggle('active', isOn);
            for (var i = 0; i < dom.forms.length; i++) {
                var spans = dom.forms[i];
                spans[isOn ? 'disable' : 'enable'].classList.add('on');
                spans[isOn ? 'enable' : 'disable'].classList.remove('on');
            }
            localStorage.setItem('memory', JSON.stringify(isOn));
        }
    }

    window.addEventListener('load', function() {
        var memory = Memory();
        memory.init();
        var forms = document.getElementsByClassName('memory');
        for (var i = 0; i < forms.length; i++) {
            memory.prepare(forms[i]);
        }
    });
})()
