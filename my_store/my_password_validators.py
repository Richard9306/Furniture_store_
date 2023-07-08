import re
from difflib import SequenceMatcher
from django.contrib.auth.password_validation import MinimumLengthValidator, CommonPasswordValidator, \
    UserAttributeSimilarityValidator, exceeds_maximum_length_ratio, NumericPasswordValidator
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.utils.translation import ngettext


class MyMinimumLengthValidator(MinimumLengthValidator):
    def __init__(self, min_length=9):
        self.min_length = min_length
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "This password is too short. It must contain at least %(min_length)d character.",
                    # "This password is too short. It must contain at least %(min_length)d characters.",
                    "Podane hasło jest za krótkie, powinno zawierać co najmniej %(min_length)d znaków",
                    self.min_length
                ),
            code='password_too_short',
            params={'min_length': self.min_length},
            )
    def get_help_text(self):
       return ngettext(
           "Your password must contain at least %(min_length)d character.",
           # "Your password must contain at least %(min_length)d characters.",
             "Twoje hasło musi zawierać co najmniej %(min_length)d znaków.",
           self.min_length
       ) % {'min_length': self.min_length}

class MyCommonPasswordValidator(CommonPasswordValidator):

    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                "Podane hasło jest zbyt proste.",
                code="password_too_common",
            )

    def get_help_text(self):
        return "Twoje hasło nie może być powszechnie używanym hasłem."

class MyUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def validate(self, password, user=None):
        if not user:
            return

        password = password.lower()
        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_lower = value.lower()
            value_parts = re.split(r"\W+", value_lower) + [value_lower]
            for value_part in value_parts:
                if exceeds_maximum_length_ratio(
                        password, self.max_similarity, value_part
                ):
                    continue
                if (
                        SequenceMatcher(a=password, b=value_part).quick_ratio()
                        >= self.max_similarity
                ):
                    try:
                        verbose_name = str(
                            user._meta.get_field(attribute_name).verbose_name
                        )
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        "Podane hasło jest zbyt podobne do %(verbose_name)s.",
                        code="password_too_similar",
                        params={"verbose_name": verbose_name},
                    )

    def get_help_text(self):
        return "Twoje hasło nie może być zbyt podobne do innych Twoich danych osobowych."

class MyNumericPasswordValidator(NumericPasswordValidator):


    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                "Podane hasło składa się z samych cyfr.",
                code="password_entirely_numeric",
            )

    def get_help_text(self):
        return "Twoje hasło nie może składać się wyłącznie z cyfr."
