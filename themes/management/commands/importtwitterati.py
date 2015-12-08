import csv

from django.core.management.base import BaseCommand, CommandError

from themes.models import TwitteratiMember, TwitteratiMemberCategory


class Command(BaseCommand):
    help = 'Imports the relevant data for Twitterati members from a CSV file'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('path_to_csv', type=str)

        # Named (optional) arguments
        parser.add_argument('--categories',
            action='store_true',
            dest='import_categories',
            default=False,
            help='Import Twitterati categories instead of Twitterati members')

    def handle(self, *args, **options):
        '''['ERROR', 'ERROR_OUTPUT',
        'HTTP_BAD_REQUEST', 'HTTP_INFO', 'HTTP_NOT_FOUND', 'HTTP_NOT_MODIFIED', 'HTTP_REDIRECT', 'HTTP_SERVER_ERROR', 'HTTP_SUCCESS',
        'MIGRATE_FAILURE', 'MIGRATE_HEADING', 'MIGRATE_LABEL', 'MIGRATE_SUCCESS',
        'NOTICE',
        'SQL_COLTYPE', 'SQL_FIELD', 'SQL_KEYWORD', 'SQL_TABLE',
        'WARNING']
        '''
        if options['import_categories']:
            self._import_categories(options['path_to_csv'])
        else:
            self._import_members(options['path_to_csv'])

    def _import_categories(self, path_to_csv):
        self.stdout.write(self.style.NOTICE("Importing Twitterati categories from '{}'...".format(path_to_csv)))
        with open(path_to_csv, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            rows_created = 0
            rows_updated = 0
            for row in reader:
                # This should update the description for any rows that already exist
                category, created = TwitteratiMemberCategory.objects.get_or_create(name=row[0])
                if created:
                    rows_created += 1
                else:
                    rows_updated += 1
                category.description = row[1]
                category.save()
        total_rows = len(TwitteratiMemberCategory.objects.all())
        self.stdout.write(self.style.NOTICE("Created {} row(s). Updated {} row(s). Total: {} row(s).".format(rows_created, rows_updated, total_rows)))

    def _import_members(self, path_to_csv):
        self.stdout.write(self.style.NOTICE("Importing Twitterati members from '{}'...".format(path_to_csv)))
        with open(path_to_csv, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            rows_created = 0
            rows_updated = 0
            for row in reader:
                # Get the category first to enforce foreign key constraints
                category = TwitteratiMemberCategory.objects.get(name=row[4])
                # This should update the description for any rows that already exist
                member, created = TwitteratiMember.objects.get_or_create(twitter_handle=row[2], category=category)
                member.first_name = row[0]
                member.last_name = row[1]
                member.biography = row[3]
                if created:
                    rows_created += 1
                else:
                    rows_updated += 1
                member.description = row[1]
                member.save()
        total_rows = len(TwitteratiMember.objects.all())
        self.stdout.write(self.style.NOTICE("Created {} row(s). Updated {} row(s). Total: {} row(s).".format(rows_created, rows_updated, total_rows)))
