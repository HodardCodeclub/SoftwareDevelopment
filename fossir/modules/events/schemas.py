

from __future__ import unicode_literals

from fossir.core.marshmallow import mm


class PersonLinkSchema(mm.Schema):
    class Meta:
        fields = ('id', 'person_id', 'email', 'first_name', 'last_name', 'title', 'affiliation', 'address', 'phone')
