

from __future__ import unicode_literals

from fossir.core.marshmallow import mm
from fossir.modules.users import User


class UserSchema(mm.ModelSchema):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'affiliation')


user_schema = UserSchema()
