# django-phone-form-field

This package contains a django MultiValueField subclass that uses a drop-down list to select a country code and a CharField to input the national number. This package relies on the python phonenumbers package to validate the phone numbers. You can get the dependency with "pip install phonenumbers."

The field allows for setting an initial value when used with a subclass of PhoneForm. Set the initial value in the Form's constructor with phone_number=. It accepts a phone number string in any format that the phonenumbers package can parse. 
