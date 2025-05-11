from django import forms

class searchAuto(forms.Form):
    from_loc = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Current location", 'id': 'autocomplete', 'required': True}),
        label="From"  # Optional: adding a label
    )
    to_loc = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Select location", 'id': 'autocomplete2', 'required': True}),
        label="To"  # Optional: adding a label
    )
    landmark = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Enter your landmark", 'id': 'landmark', 'required': True}),
        label="Landmark"  # Optional: adding a label
    )