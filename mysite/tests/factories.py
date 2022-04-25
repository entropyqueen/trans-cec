import factory


GENDERS = ['0', '1']
LOCALE = 'fr_FR'

class ProcurationFormData(factory.Factory):
    procurantfirstname = factory.Faker('first_name', locale=LOCALE)
    procurantlastname = factory.Faker('last_name', locale=LOCALE)
    procurantlistofname = factory.Faker('first_name', locale=LOCALE)
    procuranttelephone = factory.Faker('phone_number', locale=LOCALE)
    procurantdob = factory.Faker('date_of_birth', locale=LOCALE)
    procurantpob = factory.Faker('city', locale=LOCALE)
    procurantaddress1 = factory.Faker('street_address', locale=LOCALE)
    procurantaddress2 = factory.Faker('postcode', locale=LOCALE)
    procurantlocation = factory.Faker('city', locale=LOCALE)
    procurantemail = factory.Faker('email', locale=LOCALE)
    procurantgender = factory.Iterator(GENDERS)
    procurantdeadname = factory.Faker('first_name', locale=LOCALE)
    debutprocuration = factory.Faker('date_object', locale=LOCALE)
    finprocuration = factory.Faker('date_object', locale=LOCALE)
    personfirstname = factory.Faker('first_name', locale=LOCALE)
    personlastname = factory.Faker('last_name', locale=LOCALE)
    personlistofname = factory.Faker('first_name', locale=LOCALE)
    persondob = factory.Faker('date_of_birth', locale=LOCALE)
    personpob = factory.Faker('city', locale=LOCALE)
    persontelephone = factory.Faker('phone_number', locale=LOCALE)
    personlocation = factory.Faker('city', locale=LOCALE)
    personemail = factory.Faker('email', locale=LOCALE)
    personaddress1 = factory.Faker('street_address', locale=LOCALE)
    personaddress2 = factory.Faker('postcode', locale=LOCALE)
    persongender = factory.Iterator(GENDERS)

    class Meta:
        model = dict
