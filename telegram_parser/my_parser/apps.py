from django.apps import AppConfig


class ParserConfig(AppConfig):
    name = 'my_parser'

    def ready(self):
        # Вызов функции вашего парсера
        from my_parser.parser import start
        start()
