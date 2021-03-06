
from __future__ import unicode_literals

import pytest

from fossir.modules.categories import Category


@pytest.fixture
def create_category(db):
    """Returns a callable which lets you create dummy events"""

    def _create_category(id_=None, **kwargs):
        kwargs.setdefault('title', u'cat#{}'.format(id_) if id_ is not None else u'dummy')
        kwargs.setdefault('timezone', 'UTC')
        if 'parent' not in kwargs:
            kwargs['parent'] = Category.get_root()
        return Category(id=id_, acl_entries=set(), **kwargs)

    return _create_category


@pytest.fixture
def dummy_category(create_category):
    """Creates a mocked dummy category"""
    return create_category(title='dummy')
