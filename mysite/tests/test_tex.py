import pytest

from django_tex.core import compile_template_to_pdf

from . import factories


@pytest.mark.parametrize('form_id, data', [
    ('procuration_banque', {'procurantbanque': 'LCL'}),
    ('procuration_cpam', {'procurantdepartement': 'Var', 'procurantss': "1876734587698"}),
    ('procuration_ecole', {}),
    ('procuration_entreprise', {}),
    ('procuration_free', {}),
    ('procuration_impots', {}),
])
def test_procuration_templates(form_id, data):
    cleaned_data = factories.ProcurationFormData()
    cleaned_data.update(data)
    assert compile_template_to_pdf(
        'pdfgenerator/latex/{}.tex'.format(form_id),
        {'cleaned_data': cleaned_data})
