

import pytest

from fossir.modules.rb import rb_settings
from fossir.modules.rb.util import rb_check_user_access, rb_is_admin
from fossir.testing.util import bool_matrix


@pytest.mark.parametrize(('is_rb_admin', 'acl_empty', 'in_acl', 'expected'), bool_matrix('...', expect=any))
def test_rb_check_user_access(db, mocker, dummy_user, dummy_group, is_rb_admin, acl_empty, in_acl, expected):
    if is_rb_admin:
        mocker.patch('fossir.modules.rb.util.rb_is_admin', return_value=True)
    if not acl_empty:
        rb_settings.acls.add_principal('authorized_principals', dummy_group)
    if in_acl:
        rb_settings.acls.add_principal('authorized_principals', dummy_user)
    assert rb_check_user_access(dummy_user) == expected


@pytest.mark.parametrize(('is_admin', 'is_rb_admin', 'expected'), bool_matrix('..', expect=any))
def test_rb_is_admin(create_user, is_admin, is_rb_admin, expected):
    user = create_user(1, admin=is_admin, rb_admin=is_rb_admin)
    assert rb_is_admin(user) == expected
