from faker import Faker

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, connection


class Command(BaseCommand):
    help = "Populate Bouncer with sample data. Generates books, authors, and publishers."

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
            default='bouncer',
            type=str,
        )

    def handle(self, *args, **options):
        """
        Generate all the data needed for Bouncer.

        This is an all or nothing operation, so if any DB exceptions are raised,
        we rollback so as to leave the DB in the same state we found it.
        """

        try:
            with transaction.atomic():
                if options['clean']:
                    self._clean_db()

                faker_seed = options.get('seed')
                self._seed_faker(faker_seed)

                self._load_bouncer_fixtures()

        except Exception as e:
            raise CommandError(f"{e}\n\nTransaction was not committed due to the above exception.")

    def _clean_db(self):
        """
        Wipe out any existing data in the database, except migrations.
        """
        self.stdout.write("Flushing database...")

        with connection.cursor() as cursor:
            query = """
                SELECT * FROM information_schema.tables
                WHERE table_schema = \'public\' AND table_name <> \'django_migrations\';
            """
            cursor.execute(query)
            tables = cursor.fetchall()
            for table in tables:
                cursor.execute(f"TRUNCATE TABLE {table[2]} CASCADE;")

        self.stdout.write("Database flush completed successfully.")

    def _seed_faker(self, seed):
        self.stdout.write(f"Using seed \'{seed}\' for randomization.")
        fake = Faker()
        fake.seed(seed)

    def _load_bouncer_fixtures(self):
        """
        Do the dang thing.
        """
        self.stdout.write("Attempting to load bouncer fixtures...")

        # ...

        self.stdout.write("Fixtures loaded successfully.")
