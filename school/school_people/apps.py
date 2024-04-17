from django.apps import AppConfig


class SchoolPeopleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'school_people'


    def ready(self):
        import school_people.signals
