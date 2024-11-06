from django.core.management import BaseCommand

from oscarbot.messages import ResponseMessage


class Command(BaseCommand):
    help = "Help to work with text for messages"

    def add_arguments(self, parser):
        parser.add_argument(
            "--collect",
            action="store_true",
            help="Generate template file for save your messages text",
        )

        parser.add_argument(
            "--force",
            action="store_true",
            help="[Danger Zone] Hard replace messages file without backup",
        )

    def handle(self, *args, **options):
        """  """
        if options['collect']:
            ResponseMessage.collect()
        else:
            ResponseMessage.make_template(options['force'])
