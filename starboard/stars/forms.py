from django import forms

from starboard.stars.models import Repo


class StarOutputForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = forms.ChoiceField(
            label='Language',
            choices=[(l, l) for l in Repo.objects.values_list("language", flat=True).distinct()],
            required=False
        )
