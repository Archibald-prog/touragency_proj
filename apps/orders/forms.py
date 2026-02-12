from django import forms


class CreateOrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    email = forms.EmailField()
    payment_on_get = forms.ChoiceField(
        choices=[
            ("0", 'False'),
            ("1", 'True'),
        ],
    )
