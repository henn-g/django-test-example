import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_data = forms.DateField(help_text="Enter date for renewal (default 3)")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # check if date is note in the past
        if data < datetime.date.today():
            raise ValidationError(_('invalid date! renewal in past'))

        # check if date is not allowed in range (more than 4 weeks from today)
        if data > datetime.date.today + datetime.timedelta(weeks=4):
            raise ValidationError(_("invalid date! needs to be less than 4 weeks from today"))
        return data
