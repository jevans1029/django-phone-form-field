from phone_form_field import PhoneField
from django.core.exceptions import ValidationError
import unittest
from phonenumbers.phonenumberutil import NumberParseException
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "[your_app].settings")
import django
django.setup()


class PhoneFieldTest(unittest.TestCase):
    """Put your app's name in the os.environ.setdefault function"""
    valid_initial = ["+14809214823",  "+233652 456 1234",  "+526021648452" ]
    valid = [["+1", "4809214823"], ["+1", "(206)5481245"], ["+52", "642 584-6234"]]
    invalid = [["", ""], [None, ""], ["+25", "345"], ["+927", "1343223422344"], ["+1", "sdfsjj"], ["+1", "8923==1332"], ["+1", "%4809214823"]]
    bad_initial = ["b3", "joijsdfaojo", "34j2-1-494", "23==1452", "14045___624852", "*165161688014801754623"]
    def test_initial_phonenumbers(self):
        for number in self.valid_initial:

            field = PhoneField(initial=number)
            values = field.widget.decompress(number)
            self.assertNotEqual(values, [None, ""])
            self.assertEqual(field.widget.widgets[0].choices[0], values[0])
            self.assertEqual(field.widget.widgets[1].attrs["value"], values[1])

        for number in self.bad_initial:
            field = PhoneField(initial=number)
            self.assertEqual(field.widget.decompress(number), [None, ""])


    def test_valid_clean(self):
        for number in self.valid:
            field = PhoneField()
            data = field.clean(number)


    def test_invalid_clean(self):
        with self.assertRaises(ValidationError) as e:
            for number in self.invalid:

                field = PhoneField()
                field.clean(number)
                self.assertEqual(
                    PhoneField.enter_number_message, str(e.exception))


    def test_attrs(self):
        attrs = {"class": "form-control", "color": "black"}
        field = PhoneField(attrs=attrs)
        self.assertEqual(field.widget.widgets[0].attrs, attrs)
        self.assertEqual(field.widget.widgets[1].attrs, attrs)
        field = PhoneField(attrs=attrs, initial="+19085641734")
        self.assertEqual(field.widget.widgets[0].attrs, attrs)
        self.assertEqual("9085641734", field.widget.widgets[1].attrs["value"])
        self.assertEqual("form-control", field.widget.widgets[1].attrs["class"])
        self.assertEqual("black", field.widget.widgets[1].attrs["color"])










if __name__=="__main__":
    unittest.main()


