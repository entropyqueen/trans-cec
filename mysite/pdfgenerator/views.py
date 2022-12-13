# -*- coding: utf-8 -*-
from django.shortcuts import render
from django_tex.views import render_to_pdf
from django_tex.exceptions import TexError
from django import http
import traceback

from .forms import CPAMProcuration, BanqueProcuration, EcoleProcuration, EntrepriseProcuration, FreeProcuration, ImpotsProcuration
from .forms import CPAMRelanceProcuration, BanqueRelanceProcuration, EcoleRelanceProcuration, EntrepriseRelanceProcuration, FreeRelanceProcuration, ImpotsRelanceProcuration
from .forms import CPAMStandalone, EDFStandalone, BanqueStandalone, EcoleStandalone, EntrepriseStandalone, FreeStandalone, ImpotsStandalone
from .forms import ChgmtPrenomForm
from . import forms
from . import lists
from . import strings

def context(obj):
    obj['lists'] = lists.LISTS.items()
    obj['strings'] = strings.STRINGS
    return obj

def landing_page(request):
    return render(request, "pdfgenerator/landing_page.html", context({}), using='jinja2')

def error_404(request, exception=None):
    return render(request, 'pdfgenerator/404.html', context({}), using='jinja2', status=404)

def error_500(request, exception=None):
    return render(request, 'pdfgenerator/500.html', context({}), using='jinja2', status=500)

def list(request, category):
    try:
        list = lists.LISTS[category]
    except KeyError:
        raise http.Http404
    list['category'] = category
    return render(request, "pdfgenerator/list.html", context({"list": list}), using='jinja2')

def form(request, category, id):
    form_id = '{}_{}'.format(category, id)
    form_config = forms.REGISTERED_FORMS[form_id]
    form_class = form_config['form_class']
    latex_name = form_config.get('latex_name', 'pdfgenerator/latex/{}.tex'.format(form_id))
    form_context = form_config.copy()
    if request.method == "POST":
        form = form_class(request.POST)
        form_context['form'] = form
        if form.is_valid():
            try:
                return render_to_pdf(
                    request,
                    latex_name,
                    {'cleaned_data': form.cleaned_data},
                    filename="{}.pdf".format(form_id)
                )
            except TexError:
                print(traceback.format_exc())
                form.add_error(None, "Une erreur s'est produite lors de la génération du PDF")
            except:
                print(traceback.format_exc())
                form.add_error(None, "Une erreur inconnue s'est produite, merci de contacter les"
                        + " administrateur.rice.s")
    else:
        form = form_class()
        form_context['form'] = form
    return render(request, "pdfgenerator/form.html", context(form_context), using='jinja2')
