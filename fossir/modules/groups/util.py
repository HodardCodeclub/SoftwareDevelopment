

from __future__ import unicode_literals


def serialize_group(group):
    """Serialize group to JSON-like object"""
    if group.is_local:
        identifier = 'Group::{}'.format(group.id)
    else:
        identifier = 'Group:{}:{}'.format(group.provider, group.name)
    return {
        'id': group.id if group.is_local else group.name,
        'name': group.name,
        'provider': group.provider,
        'identifier': identifier,
        '_type': 'LocalGroup' if group.is_local else 'MultipassGroup',
        'isGroup': True
    }
