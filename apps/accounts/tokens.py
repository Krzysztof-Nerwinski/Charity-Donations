from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Added last login time to hash value so link is valid only until user first login
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        return str(user.username) + str(login_timestamp) + str(timestamp) + str(user.is_active)


account_activation_token = AccountActivationTokenGenerator()
