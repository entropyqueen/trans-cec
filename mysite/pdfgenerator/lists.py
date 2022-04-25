forms = [
    {'id': 'cpam', 'title': 'CPAM',
        'description': 'Pour exiger des modifications auprès de la CPAM de votre département.'},
    {'id': 'edf', 'title': 'EDF',
        'description': 'Pour tout ce qui a trait à EDF'},
    {'id': 'banque', 'title': 'Banque',
        'description': 'Pour exiger des modifications aupres de votre banque.'},
    {'id': 'assurance', 'title': 'Assurance',
        'description': 'Pour tout ce qui a trait à vos assurances'},
    {'id': 'ecole', 'title': 'École/Université',
        'description': 'Pour exiger des modifications auprès du service scolarité d\'une école/université (exemple : nouveau diplôme)'},
    {'id': 'free', 'title': 'Free',
        'description': 'Pour exiger des modifications auprès du service client de Free'},
    {'id': 'entreprise', 'title': 'Entreprise avec un numéro de contrat',
        'description': 'Pour exiger des modifications à une entreprise (numéro de contrat exigé)'},
    {'id': 'impots', 'title': 'Impôts',
        'description': 'Pour exiger des modifications au SIP dont vous dépendez'},
    {'id': 'poleemploi', 'title': 'Pôle Emploi',
        'description': 'Pour exiger des modifications à votre Pôle Emploi'},
    {'id': 'conciliateurcpam', 'title': 'Conciliateur de la CPAM',
        'description': 'Pour quand la demande à la CPAM échoue, pensez à contacter le conciliateur de la CPAM.\nVous trouverez son mail sur le site de votre caisse.'},
]

LISTS = {
    'procuration': {
        'title': 'Courriers par procuration',
        'forms': forms
    },
    'procuration_relance': {
        'title': 'Courriers de relance par procuration',
        'forms': forms
    },
    'standalone': {
        'title': 'Courriers sans procuration',
        'forms': forms
    }
}
