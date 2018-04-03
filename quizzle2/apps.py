from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "quizzle2"

    def ready(self):
        import_module("quizzle2.receivers")
