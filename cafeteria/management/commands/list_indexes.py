# list_indexes.py
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'List all indexes for all tables in the database'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            tables = connection.introspection.table_names(cursor)
            for table_name in tables:
                constraints = connection.introspection.get_constraints(cursor, table_name)
                self.stdout.write(f"Indexes for table {table_name}:")
                for constraint_name, constraint_details in constraints.items():
                    if constraint_details['index']:
                        self.stdout.write(f"  - {constraint_name}: {constraint_details}")
