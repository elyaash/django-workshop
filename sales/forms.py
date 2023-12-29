from typing import Any
from django.forms import ModelForm
from .models import Csv


class CsvModelFrom(ModelForm):
    def save(self, commit: bool = ...) -> Any:
        #print(self.data)
        print(self.files["filename"])
        return super().save(commit)
    class Meta:
        model = Csv
        fields = ["filename"]