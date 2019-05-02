from faker import Faker

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from books.factories import BookFactory, AuthorFactory
from books.models import Author, Book, Publisher


class Command(BaseCommand):
    help = "Populate mysite with sample data. Generates books, authors, and publishers."

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            help='Wipe existing data from the database before loading fixtures.',
            action='store_true',
            default=False,
        )

        parser.add_argument(
            '--seed',
            help='The initial seed to use when generating random data.',
            default='mysite',
            type=str,
        )

    def handle(self, *args, **options):
        """
        Generate all the data needed for mysite.

        This is an all or nothing operation, so if any DB exceptions are raised,
        we rollback so as to leave the DB in the same state we found it.
        """

        try:
            with transaction.atomic():
                if options['clean']:
                    self._clean_db()

                faker_seed = options.get('seed')
                self._seed_faker(faker_seed)

                self._load_fixtures()

        except Exception as e:
            raise CommandError(f"{e}\n\nTransaction was not committed due to the above exception.")

    def _clean_db(self):
        """
        Wipe out any existing data in the database.
        """
        self.stdout.write("Flushing database...")

        for model in [Author, Book, Publisher]:
            model.objects.all().delete()

        self.stdout.write("Database flush completed successfully.")

    def _seed_faker(self, seed):
        self.stdout.write(f"Using seed \'{seed}\' for randomization.")
        fake = Faker()
        fake.seed(seed)

    def _load_fixtures(self):
        """
        Create and save the necessary factories.
        """
        self.stdout.write("Attempting to load mysite fixtures...")

        author1 = AuthorFactory.create()
        author2 = AuthorFactory.create()
        BookFactory.create(authors=[author1, author2])

        self.stdout.write("Fixtures loaded successfully.")
