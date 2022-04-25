import pytest
import datetime
from django import http
from django.utils import html

from pdfgenerator import forms
from pdfgenerator import lists
from pdfgenerator import views


def test_list_view(rf):
    request = rf.get('/')
    response = views.list(request, 'procuration')
    list = lists.LISTS['procuration']

    assert response.status_code == 200

    content = response.content.decode()
    assert '<h1>{}</h1>'.format(html.escape(list['title'])) in content

    for form in list['forms']:
        assert '<p>{}</p>'.format(html.escape(form['description'])) in content


def test_list_view_unkwnown(rf):
    with pytest.raises(http.Http404):
        views.list(rf.get('/'), 'unkwown')


def test_form_view_get(rf):
    request = rf.get('/')
    response = views.form(request, 'procuration', 'banque')
    form = forms.REGISTERED_FORMS['procuration_banque']

    assert response.status_code == 200

    content = response.content.decode()
    assert '<h1>{}</h1>'.format(html.escape(form['title'])) in content


def test_form_view_get(rf, mocker):
    render_to_pdf = mocker.patch.object(views, 'render_to_pdf')
    data = {
        'procurantfirstname': 'Alice',
        'procurantlastname': 'Test',
        'procurantlistofname': 'Luc',
        'procuranttelephone': '+33621347094',
        'procurantdob_day': '7',
        'procurantdob_month': '1',
        'procurantdob_year': '1908',
        'procurantpob': 'Lille (Nord)',
        'procurantaddress1': '78',
        'procurantaddress2': '13001 Marseille',
        'procurantlocation': 'Poitiers',
        'procurantemail': 'test@test.com',
        'procurantgender': '0',
        'procurantdeadname': 'Test',
        'debutprocuration_day': '1',
        'debutprocuration_month': '1',
        'debutprocuration_year': '1908',
        'finprocuration_day': '1',
        'finprocuration_month': '1',
        'finprocuration_year': '2019',
        'personfirstname': 'Olive',
        'personlastname': 'Ettom',
        'personlistofname': 'Ilsferont',
        'persondob_day': '1',
        'persondob_month': '8',
        'persondob_year': '1900',
        'personpob': 'Nantes(Loire-Atlantique)',
        'persontelephone': '+33621347067',
        'personlocation': 'Poitiers',
        'personemail': 'receveur@test.com',
        'personaddress1': 'test receveur',
        'personaddress2': '75000 Paris',
        'persongender': '0',
        'procurantbanque': 'LCL',
    }

    cleaned_data = {
        'procurantfirstname': 'Alice',
        'procurantlastname': 'Test',
        'procurantlistofname': 'Luc',
        'procuranttelephone': '+33621347094',
        'procurantdob': datetime.date(1908, 1, 7),
        'procurantpob': 'Lille (Nord)',
        'procurantaddress1': '78',
        'procurantaddress2': '13001 Marseille',
        'procurantlocation': 'Poitiers',
        'procurantemail': 'test@test.com',
        'procurantgender': '0',
        'procurantdeadname': 'Test',
        'debutprocuration': datetime.date(1908, 1, 1),
        'finprocuration': datetime.date(2019, 1, 1),
        'personfirstname': 'Olive',
        'personlastname': 'Ettom',
        'personlistofname': 'Ilsferont',
        'persondob': datetime.date(1900, 8, 1),
        'personpob': 'Nantes(Loire-Atlantique)',
        'persontelephone': '+33621347067',
        'personlocation': 'Poitiers',
        'personemail': 'receveur@test.com',
        'personaddress1': 'test receveur',
        'personaddress2': '75000 Paris',
        'persongender': '0',
        'procurantbanque': 'LCL',
    }
    request = rf.post('/', data)
    response = views.form(request, 'procuration', 'banque')

    assert response == render_to_pdf.return_value
    render_to_pdf.assert_called_once_with(
        request,
        'pdfgenerator/latex/procuration_banque.tex',
        {'cleaned_data': cleaned_data},
        filename="procuration_banque.pdf"
    )
