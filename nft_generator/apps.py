from django.apps import AppConfig


class PickerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nft_generator'

    def ready(self):
        import nft_generator.signals
