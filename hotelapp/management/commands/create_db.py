from django.core.management.base import BaseCommand
from django.conf import settings
import psycopg2
from psycopg2 import sql

class Command(BaseCommand):
    help = "Create the database defined in settings.DATABASES"

    def handle(self, *args, **kwargs):
        db_settings = settings.DATABASES['default']

        # Получение параметров подключения
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_password = db_settings['PASSWORD']
        db_host = db_settings['HOST']
        db_port = db_settings['PORT']

        # Подключение к PostgreSQL (суперпользователь)
        try:
            connection = psycopg2.connect(
                dbname="postgres",
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            connection.autocommit = True
            cursor = connection.cursor()

            # Создание базы данных
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(db_name)
            ))
            self.stdout.write(self.style.SUCCESS(f"Database '{db_name}' created successfully."))
        except psycopg2.errors.DuplicateDatabase:
            self.stdout.write(self.style.WARNING(f"Database '{db_name}' already exists."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))
        finally:
            if 'connection' in locals():
                cursor.close()
                connection.close()
