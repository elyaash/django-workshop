from typing import Any
from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from sales.models import Collection
from pathlib import Path
from django.conf import settings
import os
import json
from django.core.management import call_command
class Command(BaseCommand):
    help = 'Seed collections'
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('nums', type= int)

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.loaddata('collection.json')
        self.loaddata('promotion.json')
        self.loaddata('product.json')
        #Collection.objects.bulk_create()
        return     
    def loaddata(self, fixture):
        print(f"Loading fiture... {fixture}",end="...")
        file =os.path.join(Path(__file__).resolve().parent, fixture)
        if (os.path.isfile(file) and os.path.getsize(file) > 10):       
            call_command('loaddata',file)
        else:
            print("no data")
        