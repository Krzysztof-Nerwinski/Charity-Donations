from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class BigAndSmallLetterPasswordValidator:
    def __init__(self, min_cap_letters=1, min_small_letters=1):
        self.min_cap_letters = min_cap_letters
        self.min_small_letters = min_small_letters

    def validate(self, password, user=None):
        cap_letters = len(list(filter(lambda letter: letter.isupper(), [letter for letter in password])))
        small_letters = len(list(filter(lambda letter: letter.islower(), [letter for letter in password])))
        if cap_letters < self.min_cap_letters:
            raise ValidationError(
                _("Wymagana ilośc dużych liter: %(min_cap_letters)d"),
                code='not_enough_cap_letters',
                params={'min_cap_letters': self.min_cap_letters},
            )
        if small_letters < self.min_small_letters:
            raise ValidationError(
                _("Wymagana ilośc małych liter: %(min_small_letters)d"),
                code='not_enough_cap_letters',
                params={'min_small_letters': self.min_small_letters},
            )

    def get_help_text(self):
        return _(
            "Wymagana ilośc dużych liter: %(min_cap_letters)d oraz małych liter: %(min_small_letters)d"
            % {'min_cap_letters': self.min_cap_letters,
               'min_small_letters': self.min_small_letters}
        )


