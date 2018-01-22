

from __future__ import unicode_literals

from flask_multipass.providers.sqlalchemy import SQLAlchemyAuthProviderBase, SQLAlchemyIdentityProviderBase

from fossir.modules.auth import Identity
from fossir.modules.auth.forms import LocalLoginForm
from fossir.modules.users import User


class fossirAuthProvider(SQLAlchemyAuthProviderBase):
    login_form = LocalLoginForm
    identity_model = Identity
    provider_column = Identity.provider
    identifier_column = Identity.identifier
    multi_instance = False

    def check_password(self, identity, password):
        # No, the passwords are not stored in plaintext. Magic is happening here!
        return identity.password == password


class fossirIdentityProvider(SQLAlchemyIdentityProviderBase):
    user_model = User
    identity_user_relationship = 'user'
    multi_instance = False
