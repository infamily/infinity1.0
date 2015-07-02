# coding: utf-8
import MySQLdb

from django.core.management.base import BaseCommand
from core.models import Language


class Command(BaseCommand):
    help = 'prefill languages objects'

    def handle(self, *args, **options):
        self.prefill()

    def prefill(self):
        db = MySQLdb.connect(host="localhost", user="root", passwd="pwd",
                             db="omegawiki")
        cur = db.cursor()
        cur.execute("select language_id, language_name from language_names where name_language_id = 85;")
        db.text_factory = str
        for row in cur.fetchall():
            Language.objects.create(omegawiki_language_id=int(row[0]),
                                    name=row[1])
