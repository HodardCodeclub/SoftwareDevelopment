

from __future__ import unicode_literals

from fossir.core.auth import multipass
from fossir.legacy.fossils.user import IGroupFossil
from fossir.modules.groups import GroupProxy
from fossir.util.fossilize import Fossilizable, fossilizes
from fossir.util.string import encode_utf8, return_ascii, to_unicode


class GroupWrapper(Fossilizable):
    """Group-like wrapper class that holds a DB-stored (or remote) group."""

    fossilizes(IGroupFossil)

    def __init__(self, group_id):
        self.id = to_unicode(group_id).encode('utf-8')

    @property
    def group(self):
        """Returns the underlying GroupProxy

        :rtype: fossir.modules.groups.core.GroupProxy
        """
        raise NotImplementedError

    def getId(self):
        return self.id

    def getName(self):
        raise NotImplementedError

    def getFullName(self):
        return self.getName()

    def getEmail(self):
        return ''

    def exists(self):
        return self.group.group is not None

    def __eq__(self, other):
        if not hasattr(other, 'group') or not isinstance(other.group, GroupProxy):
            return False
        return self.group == other.group

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.group)

    @return_ascii
    def __repr__(self):
        return u'<{} {}: {}>'.format(type(self).__name__, self.id, self.group)


class LocalGroupWrapper(GroupWrapper):
    is_local = True
    groupType = 'Default'

    @property
    def group(self):
        return GroupProxy(self.id)

    @encode_utf8
    def getName(self):
        return self.group.group.name if self.exists() else self.id


class LDAPGroupWrapper(GroupWrapper):
    is_local = False
    provider_name = None
    groupType = 'LDAP'

    @property
    def provider(self):
        if self.provider_name:
            return self.provider_name
        provider = multipass.default_group_provider
        assert provider, 'No identity provider has default_group_provider enabled'
        return provider.name

    @property
    def group(self):
        return GroupProxy(self.id, self.provider)

    @encode_utf8
    def getName(self):
        return self.id
