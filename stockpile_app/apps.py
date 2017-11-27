from django.apps import AppConfig


class StockpileAppConfig(AppConfig):
    name = 'stockpile_app'

    def ready(self):
        from stockpile_app import signals
