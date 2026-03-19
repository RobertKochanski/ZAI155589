from django import forms

from .models import Pokemon


class PokemonForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        fields = ["name", "height", "weight", "types", "abilities", "moves", "sprite"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if field.widget.__class__.__name__ == "SelectMultiple":
                field.widget.attrs.update({"class": "form-select"})
            else:
                field.widget.attrs.update({"class": "form-control"})
