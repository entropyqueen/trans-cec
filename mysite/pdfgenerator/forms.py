# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin import widgets

REGISTERED_FORMS = {}
class Fieldset(object):
    def __init__(self, id, field_names, legend):
        self.id = id
        self.field_names = field_names
        self.legend = legend


class FieldsetForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'

    def get_fieldsets(self):
        # a list of tuples containing a Fieldset and a list of bound form fields
        # to display in a template
        fieldsets = []
        handled_fields = []
        try:
            declared_fieldsets = self.Meta.fieldsets
        except AttributeError:
            declared_fieldsets = []
        for fs in declared_fieldsets:
            fields = [self[field_name] for field_name in fs.field_names]
            fieldsets.append((fs, fields))
            handled_fields += fs.field_names

        # we include other fields in a fallback fieldset, at the end of the form
        remaining_fields = [k for k in self.fields if k not in handled_fields]
        if remaining_fields:
            fs = Fieldset(
                'procurant_id',
                legend='Autres informations',
                field_names=remaining_fields,
            )
            fields = [self[field_name] for field_name in fs.field_names]
            fieldsets.append((fs, fields))

        return fieldsets

def register_form(category, id, title, url=None):
    """
    Register a form class with configuration options so it can be displayed
    automatically with the proper URL/template/title:

        @register_form(category='form_category', id='form_id', title='Hello')
        class MyFormClass():
            ...

    Would serve the form MyFormClass on /form_category/form_id, with the
    page title being "hello".

    If you provide the url argument, the form url will use that instead of the {category}/{id} scheme.
    """
    def decorator(form_class):
        if category:
            full_id = '{}_{}'.format(category, id)
            url_path = url or '{}/{}'.format(category, id)
        else:
            full_id = id
            url_path = url or id
        REGISTERED_FORMS[full_id] = {
            'form_class': form_class,
            'url_path': url_path,
            'title': title,
            'category': category,
        }
        return form_class

    return decorator

# Dict matching a usual char to it's escaped equivalent in TeX
SPECIAL_CHARS = {
        "_" : "\\_"
        # /!\ Warning the following charecter is *not* the simple quote
        ,"'" : "’"
        # Escaping double quote isn't that simple
        #,'"' : '\\"'
        }

def sanitizeStringForTex(string_value):
    # Escape backlash and avoid injection
    value = string_value.replace("\\", "\\textbackslash ")
    for key in SPECIAL_CHARS:
        value = value.replace(key, SPECIAL_CHARS[key])
    return value

# CharField subclass that cleans the value so it is properly rendered by TeX
class CharFieldTex(forms.CharField):
    def clean(self, val):
        cleaned_data = super().clean(val)
        cleaned_data = sanitizeStringForTex(cleaned_data)
        return cleaned_data

# EmailField subclass that cleans the value so it is properly rendered by TeX
class EmailFieldTex(forms.EmailField):
    def clean(self, val):
        cleaned_data = super().clean(val)
        cleaned_data = sanitizeStringForTex(cleaned_data)
        return cleaned_data


@register_form(category='attestation', id="chgmtprenom", title="Nouvelle attestation de changement de prénom")
class ChgmtPrenomForm(FieldsetForm):
    procurantfirstname = CharFieldTex(label="Prénom")
    procurantlastname = CharFieldTex(label="Nom de famille")
    procurantlistofname = CharFieldTex(label="Liste des prénoms")
    procurantdob = forms.DateField(label="Date de naissance", widget=forms.SelectDateWidget(years=range(1900, 3000), attrs={'class': 'date-widget form-control'}))
    procurantpob = CharFieldTex(label="Lieu et département de naissance", widget=forms.TextInput(attrs={'placeholder': 'Nantes (Loire-Atlantique)'}))
    procurantaddress1 = CharFieldTex(label="Adresse")
    procurantaddress2 = CharFieldTex(label="Code postal et Ville")
    procurantgender = forms.ChoiceField(label="Accords", choices=((0, "féminin"), (1, "masculin")))
    procurantville = CharFieldTex(label="Ville de dépendance à l'État-Civil")
    personignoredeadname = forms.ChoiceField(label="Ignorer le deadname", choices=((0, "oui"), (1, "non")))
    procurantdeadname = CharFieldTex(label="Deadname (facultatif)", required=False)
    date = forms.DateField(label="Date de l'attestation", widget=forms.SelectDateWidget(attrs={'class': 'date-widget form-control'}))
    personfirstname = CharFieldTex(label="Prénom de la personne qui fait l'attestation")
    personlastname = CharFieldTex(label="Nom de famille de la personne qui fait l'attestation")
    personlistofname = CharFieldTex(label="Liste des prénoms de la personne qui fait l'attestation")
    persondob = forms.DateField(label="Date de naissance de la personne qui fait l'attestation", widget=forms.SelectDateWidget(years=range(1900, 3000), attrs={'class': 'date-widget form-control'}))
    personpob = CharFieldTex(label="Lieu et département de naissance de la personne qui fait l'attestation", widget=forms.TextInput(attrs={'placeholder': 'Nantes (Loire-Atlantique)'}))
    persontelephone = forms.RegexField(
        label="Numéro de téléphone",
        regex=r'^\+33\d{9}$',
        widget=forms.TextInput(attrs={'placeholder': '+33612345678'})
    )
    personlocation = CharFieldTex(label="Lieu où est faite la lettre")
    personemail = EmailFieldTex(label="Email procurant")
    personaddress1 = CharFieldTex(label="Adresse")
    personaddress2 = CharFieldTex(label="Code postal et Ville")
    persongender = forms.ChoiceField(label="Accord de la personne", choices=((0, "féminin"), (1, "masculin")))


PROCURANT_IDENTITY_FIELDSETS = Fieldset(
    'procurant_id',
    legend='Identité de la personne faisant la procuration',
    field_names=[
        'procurantfirstname',
        'procurantlastname',
        'procurantlistofname',
        'procurantgender',
        'procurantdeadname',
        'procurantdob',
        'procurantpob',
    ]
)


PROCURANT_CONTACT_FIELDSETS = Fieldset(
    'procurant_id',
    legend='Coordonnées de la personne faisant la procuration',
    field_names=[
        'procurantemail',
        'procuranttelephone',
        'procurantaddress1',
        'procurantaddress2',
    ]
)
PERSON_IDENTITY_FIELDSETS = Fieldset(
    'person_id',
    legend='Identité de la personne recevant la procuration',
    field_names=[
        'personfirstname',
        'personlastname',
        'personlistofname',
        'persongender',
        'persondob',
        'personpob',
    ]
)

PERSON_CONTACT_FIELDSETS = Fieldset(
    'person_contact',
    legend='Coordonnées de la personne recevant la procuration',
    field_names=[
        'personemail',
        'persontelephone',
        'personaddress1',
        'personaddress2',
    ]
)

PROCURATION_FIELDSETS = Fieldset(
    'procuration',
    legend='Informations relatives à la procuration',
    field_names=[
        'procurantlocation',
        'debutprocuration',
        'finprocuration',
    ]
)

CUSTOMISATION_FIELDSETS = Fieldset(
    'customisation',
    legend='Customisation du contenu de la lettre',
    field_names=[
        'changementprenom',
        'changementcivilite',
    ]
)

class ProcurationForm(FieldsetForm):
    procurantfirstname = CharFieldTex(label="Prénom")
    procurantlastname = CharFieldTex(label="Nom de famille")
    procurantlistofname = CharFieldTex(label="Liste des prénoms", widget=forms.TextInput(attrs={'placeholder': 'Corentin, Sebastien, Pierre'}))
    procuranttelephone = forms.RegexField(
        label="Numéro de téléphone",
        regex=r'^\+33\d{9}$',
        widget=forms.TextInput(attrs={'placeholder': '+33612345678'})
    )
    procurantdob = forms.DateField(label="Date de naissance", widget=forms.SelectDateWidget(years=range(1900, 3000), attrs={'class': 'date-widget form-control'}))
    procurantpob = CharFieldTex(label="Lieu et département de naissance", widget=forms.TextInput(attrs={'placeholder': 'Nantes (Loire-Atlantique)'}))
    procurantaddress1 = CharFieldTex(label="Adresse")
    procurantaddress2 = CharFieldTex(label="Code postal et Ville")
    procurantlocation = CharFieldTex(label="Lieu où est faite la procuration")
    procurantemail = EmailFieldTex(label="Email")
    procurantgender = forms.ChoiceField(label="Accords", choices=((0, "féminin"), (1, "masculin")))
    procurantdeadname = CharFieldTex(label="Deadname (prénom)")
    debutprocuration = forms.DateField(label="Début de la procuration", widget=forms.SelectDateWidget(years=range(1900, 3000), attrs={'class': 'date-widget form-control'}))
    finprocuration = forms.DateField(label="Fin de la procuration", widget=forms.SelectDateWidget(attrs={'class': 'date-widget form-control'}))
    personfirstname = CharFieldTex(label="Prénom")
    personlastname = CharFieldTex(label="Nom de famille")
    personlistofname = CharFieldTex(label="Liste des prénoms", widget=forms.TextInput(attrs={'placeholder': 'Émilie, Delphine, Coralie'}))
    persondob = forms.DateField(label="Date de naissance", widget=forms.SelectDateWidget(years=range(1900, 3000), attrs={'class': 'date-widget form-control'}))
    personpob = CharFieldTex(label="Lieu et département de naissance", widget=forms.TextInput(attrs={'placeholder': 'Nantes (Loire-Atlantique)'}))
    persontelephone = forms.RegexField(
        label="Numéro de téléphone",
        regex=r'^\+33\d{9}$',
        widget=forms.TextInput(attrs={'placeholder': '+33612345678'})
    )
    personlocation = CharFieldTex(label="Lieu où est faite la lettre")
    personemail = EmailFieldTex(label="Email")
    personaddress1 = CharFieldTex(label="Adresse")
    personaddress2 = CharFieldTex(label="Code postal et Ville")
    persongender = forms.ChoiceField(label="Accord", choices=((0, "féminin"), (1, "masculin")))
    changementprenom = forms.ChoiceField(label="Texte pour un changement de prénom", choices=((0, "inclure"), (1, "ne pas inclure")))
    changementcivilite = forms.ChoiceField(label="Texte pour un changement de civilité", choices=((0, "inclure"), (1, "ne pas inclure")))

    class Meta:
        fieldsets = [
            PROCURANT_IDENTITY_FIELDSETS,
            PROCURANT_CONTACT_FIELDSETS,
            PERSON_IDENTITY_FIELDSETS,
            PERSON_CONTACT_FIELDSETS,
            PROCURATION_FIELDSETS,
            CUSTOMISATION_FIELDSETS,
        ]

@register_form(category='procuration', id='poleemploi', title='Pôle Emploi')
class PoleEmploiProcuration(ProcurationForm):
    entite = CharFieldTex(label="Ville/Département du Pôle Emploi")
    numero = CharFieldTex(label="Numéro Pôle Emploi")

@register_form(category='procuration', id='conciliateurcpam', title='Nouvelle procuration pour la conciliation de la CPAM')
class ConciliateurCPAMProcuration(ProcurationForm):
    procurantdepartement = CharFieldTex(label="Département de la caisse de CPAM de la personne faisant la procuration")
    procurantss = forms.IntegerField(label="Numéro de sécu")

@register_form(category='procuration', id="cpam", title="Nouvelle procuration pour la CPAM")
class CPAMProcuration(ProcurationForm):
    procurantdepartement = CharFieldTex(label="Département de la caisse de CPAM de la personne faisant la procuration")
    procurantss = forms.IntegerField(label="Numéro de sécu")

@register_form(category='procuration', id="ecole", title="Nouvelle procuration pour une École/Université")
class EcoleProcuration(ProcurationForm):
    procurantecole = CharFieldTex(label="École/Université de la personne faisant la procuration")


@register_form(category='procuration', id="banque", title="Nouvelle procuration pour une Banque")
class BanqueProcuration(ProcurationForm):
    procurantbanque = CharFieldTex(label="Banque de la personne faisant la procuration")

@register_form(category='procuration', id="entreprise", title="Nouvelle procuration pour une entreprise avec numéro de contrat")
class EntrepriseProcuration(ProcurationForm):
    procurantentreprise = CharFieldTex(label="Entreprise de la personne faisant la procuration")
    procurantcontrat = CharFieldTex(label="Numéro de contrat")

@register_form(category='procuration', id="free", title="Nouvelle procuration pour Free")
class FreeProcuration(ProcurationForm):
    pass

@register_form(category='procuration', id="impots", title="Nouvelle procuration pour les impôts")
class ImpotsProcuration(ProcurationForm):
    procurantimpots = CharFieldTex(label="Ville dont on dépend pour les impots")
    procurantfiscal = CharFieldTex(label="Numéro fiscal")

class RelanceProcurationForm(ProcurationForm):
    datepremiercourrier = forms.DateField(label="Date du premier courrier", widget=forms.SelectDateWidget(years=range(2019, 3000), attrs={'class': 'date-widget form-control'}))

@register_form(category='procuration_relance', id="cpam", title="Relance procuration pour la CPAM", url='procuration/relance/cpam')
class CPAMRelanceProcuration(RelanceProcurationForm, CPAMProcuration):
    pass

@register_form(category='procuration_relance', id="ecole", title="Relance une École/Université", url='procuration/relance/ecole')
class EcoleRelanceProcuration(RelanceProcurationForm, EcoleProcuration):
    pass

@register_form(category='procuration_relance', id="banque", title="Relance pour une Banque", url='procuration/relance/banque')
class BanqueRelanceProcuration(RelanceProcurationForm, BanqueProcuration):
    pass

@register_form(category='procuration_relance', id="entreprise", title="Relance pour entreprise avec numéro de contrat", url='procuration/relance/entreprise')
class EntrepriseRelanceProcuration(RelanceProcurationForm, EntrepriseProcuration):
    pass

@register_form(category='procuration_relance', id="free", title="Relance pour Free", url='procuration/relance/free')
class FreeRelanceProcuration(RelanceProcurationForm, FreeProcuration):
    pass

@register_form(category='procuration_relance', id="impots", title="Relance pour les impôts", url='procuration/relance/impots')
class ImpotsRelanceProcuration(RelanceProcurationForm, ImpotsProcuration):
    pass


IDENTITY_FIELDSETS = Fieldset(
    'person_id',
    legend='Identité',
    field_names=[
        'firstname',
        'lastname',
        'listofname',
        'deadname',
        'gender',
        'dob',
        'pob',
    ]
)

CONTACT_FIELDSETS = Fieldset(
    'person_contact',
    legend='Coordonnées',
    field_names=[
        'email',
        'telephone',
        'address1',
        'address2',
    ]
)

CUSTOMISATION_FIELDSET = Fieldset(
    'customisation',
    legend='Customisation',
    field_names=[
        'changementprenom',
        'changementcivilite',
    ]
)

class StandaloneForm(FieldsetForm):
    firstname = CharFieldTex(label="Prénom")
    deadname = CharFieldTex(label="Deadname")
    lastname = CharFieldTex(label="Nom de famille")
    listofname = CharFieldTex(label="Liste des prénoms")
    telephone = forms.RegexField(
        label="Numéro de téléphone",
        regex=r'^\+33\d{9}$',
        widget=forms.TextInput(attrs={'placeholder': '+33612345678'})
    )
    dob = forms.DateField(label="Date de naissance ", widget=forms.SelectDateWidget(years=range(1900, 3000), attrs={'class': 'date-widget form-control'}))
    pob = CharFieldTex(label="Lieu et département de naissance", widget=forms.TextInput(attrs={'placeholder': 'Nantes (Loire-Atlantique)'}))
    address1 = CharFieldTex(label="Adresse")
    address2 = CharFieldTex(label="Code postal et Ville")
    location = CharFieldTex(label="Lieu où est faite la lettre")
    email = EmailFieldTex(label="Email")
    gender = forms.ChoiceField(label="Accords ", choices=((0, "féminin"), (1, "masculin")))
    date = forms.DateField(label="Date du courrier", widget=forms.SelectDateWidget(years=range(1900, 3000), attrs={'class': 'date-widget form-control'}))
    changementprenom = forms.ChoiceField(label="Texte pour un changement de prénom", choices=((0, "inclure"), (1, "ne pas inclure")))
    changementcivilite = forms.ChoiceField(label="Texte pour un changement de civilité", choices=((0, "inclure"), (1, "ne pas inclure")))

    class Meta:
        fieldsets = [
            IDENTITY_FIELDSETS,
            CONTACT_FIELDSETS,
            CUSTOMISATION_FIELDSET,
        ]

@register_form(category='standalone', id='poleemploi', title='Pôle Emploi')
class PoleEmploiStandalone(StandaloneForm):
    entite = CharFieldTex(label="Ville/Département du Pôle Emploi")
    numero = CharFieldTex(label="Numéro Pôle Emploi")

@register_form(category='standalone', id='conciliateurcpam', title='Conciliateur CPAM')
class ConciliateurCPAMStandalone(StandaloneForm):
    departement = CharFieldTex(label="Département de la caisse de CPAM")
    ss = forms.IntegerField(label="Numéro de sécu")
@register_form(category='standalone', id="cpam", title="CPAM")
class CPAMStandalone(StandaloneForm):
    departement = CharFieldTex(label="Département de la caisse de CPAM")
    ss = forms.IntegerField(label="Numéro de sécu")

@register_form(category='standalone', id="edf", title="EDF")
class EDFStandalone(StandaloneForm):
    client_id = forms.IntegerField(label="Numéro client")

@register_form(category='standalone', id="assurance", title="Assurance")
class AssuranceStandalone(StandaloneForm):
    insurance = forms.IntegerField(label="Nom de l'assurance")
    insurance_id = forms.IntegerField(label="Numéro client")

@register_form(category='standalone', id="ecole", title="École/Université")
class EcoleStandalone(StandaloneForm):
    ecole = CharFieldTex(label="École/Université")

@register_form(category='standalone', id="banque", title="Banque")
class BanqueStandalone(StandaloneForm):
    banque = CharFieldTex(label="Banque")

@register_form(category='standalone', id="entreprise", title="entreprise avec numéro de contrat")
class EntrepriseStandalone(StandaloneForm):
    entreprise = CharFieldTex(label="Entreprise")
    contrat = CharFieldTex(label="Numéro de contrat")

@register_form(category='standalone', id="free", title="Free")
class FreeStandalone(StandaloneForm):
    pass

@register_form(category='standalone', id="impots", title="Impôts")
class ImpotsStandalone(StandaloneForm):
    impots = CharFieldTex(label="Ville dont on dépend pour les impots")
    fiscal = CharFieldTex(label="Numéro fiscal")
