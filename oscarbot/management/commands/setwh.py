import requests
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        token = input('Enter your Telegram bot token: ')

        while True:
            msg = 'Enter webhook address'
            if hasattr(settings, 'BASE_URL'):
                msg += f' [or leave blank for "{settings.BASE_URL}"]: '
            else:
                msg += ': '

            base_url = input(msg)

            if base_url:
                if 'http:' in base_url:
                    base_url = base_url.replace('http:', 'https:')
                    self.stdout.write(
                        self.style.WARNING(
                            f'Address must be secure, changed to {base_url}'
                        )
                    )
                elif 'https' not in base_url:
                    base_url = 'https://' + base_url
                    self.stdout.write(
                        self.style.WARNING(
                            f'Full address will be set as {base_url}'
                        )
                    )

                if base_url[-1] != '/':
                    base_url += '/'

                break

            self.stdout.write(
                self.style.ERROR(
                    'Enter valid url or domain name'
                )
            )

        data = {
            'url': f'{base_url}api/bot{token}/'
        }
        response = requests.post(
            f'{settings.TELEGRAM_URL}{token}/setWebhook',
            json=data
        )
        if response.status_code == 200:
            self.stdout.write(
                self.style.SUCCESS(
                    response.json().get('description')
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    response.json().get('description')
                )
            )
