from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(max_length=255, min_length=2, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'search',
                                                                                                'placeholder': 'search for items here...'}))