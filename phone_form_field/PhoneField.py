import traceback

from django.core.validators import RegexValidator
from django.forms import MultiValueField
from phone_form_field.country_choices import choice_list
from django.forms.widgets import Select
from django.forms.fields import ChoiceField
from django.forms.fields import CharField
from django.forms.widgets import TextInput
from django.forms.widgets import MultiWidget
from django.core.exceptions import ValidationError
from django.forms import Form
from phonenumbers import phonenumber
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException




class CountryCodeWidget(Select):
    initial = None
    """Choice widget that sets the first choice to the country code given in the initial variable. 
    The initial variable must be a tuple of length equal to two. The first index of the tuple will be the value if the option 
    and the second index will be the text content of the drop-down option.  """
    def __init__(self, initial=None, attrs=None):

        self.choices = choice_list.copy()
        if initial is not None:
            if not type(initial) is tuple:
                raise TypeError("Initial Value for Country Code Widget must be a tuple")
            else:
                self.choices[0]=initial
        super().__init__(choices=self.choices, attrs=attrs)


class PhoneField(MultiValueField):
    enter_number_message = "Enter a valid phone number"
    enter_national_number = "Enter a national phone number"
    def __init__(self, initial=None, attrs=None, **kwargs):
        """initial must be passed in the subclass of PhoneForm's constructor"""
        widget = PhoneMultiWidget(attrs=attrs, initial=initial)
        error_messages= {"invalid": "Enter a valid phone number"}
        fields = (
            ChoiceField(
                choices=choice_list
            ),
            CharField(
                error_messages={'incomplete': self.enter_national_number},
            ),

        )
        super().__init__(
            fields=fields, require_all_fields=True, widget=widget, error_messages=error_messages, **kwargs
        )

    def compress(self, data_list):
        """Combines the two field's values into a single value. This is called after each field's values are first cleaned and then combined into a list"""
        try:
            number = phonenumbers.parse(data_list[0] + data_list[1], "US")
        except NumberParseException:
            raise ValidationError(self.enter_number_message)
        if not phonenumbers.is_valid_number(number):
            raise ValidationError(self.enter_number_message)
        else:
            return "+" + str(number.country_code) + str(number.national_number)

class PhoneMultiWidget(MultiWidget):
    def __init__(self, attrs=None, initial=None):
        if initial is not None:
            self.initial = self.decompress(initial)
            if attrs:
                textattrs = attrs.copy()
                textattrs["value"] = self.initial[1]
            else:
                textattrs= {}
                textattrs["value"] = self.initial[1]
            widgets = (CountryCodeWidget(initial=self.initial[0], attrs=attrs), TextInput(attrs=textattrs))
        else:
            widgets = (CountryCodeWidget(attrs=attrs), TextInput(attrs=attrs))
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            try:
                value = phonenumbers.parse(value, "US")
                if value.country_code is not None:
                    return [("+" + str(value.country_code), "Country Code +" + str(value.country_code)), str(value.national_number)]
            except NumberParseException as e:
                print("Could not parse phone number")

        return [None, ""]


class PhoneForm(Form):
    """For the initial value of the Phone Field to work, your form must extend this form and pass the initial phone_number in the constructor
    in the format of a string, with or without the country code. """
    def __init__(self, phone_number=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["phone"] = PhoneField(label="Phone Number", initial=phone_number)