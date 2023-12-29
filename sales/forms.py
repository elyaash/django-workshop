from typing import Any
from django.forms import ModelForm
from .models import Csv,Sales
import csv
import io

class CsvModelFrom(ModelForm):
    def save(self, commit: bool = ...) -> Any:
        #print(self.data)
        csvFile = self.files.get('filename','')
        if (len(csvFile) > 1):
            file = csvFile.read().decode('utf-8-sig')  
            reader = csv.DictReader(io.StringIO(file))
            for row in reader:
                Sales.objects.create(
                    product_id=int(row.get("Product")),
                    salesmen_id=int(row.get("User")),
                    qty=int(row.get("Qty")),
                )           
        return super().save(commit)
    class Meta:
        model = Csv
        fields = ["filename"]