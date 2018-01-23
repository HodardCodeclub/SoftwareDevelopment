

from __future__ import unicode_literals


def serialize_ip_network_group(group):
    """Serialize group to JSON-like object"""
    return {
        'id': group.id,
        'name': group.name,
        'identifier': 'IPNetworkGroup:{}'.format(group.id),
        '_type': 'IPNetworkGroup'
    }
