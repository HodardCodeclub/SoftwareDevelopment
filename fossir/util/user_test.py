

from mock import MagicMock

from fossir.modules.groups import GroupProxy
from fossir.modules.networks.models.networks import IPNetworkGroup
from fossir.modules.users import User
from fossir.util.user import iter_acl, unify_user_args


def test_iter_acl():
    user = User()
    user_p = MagicMock(principal=user, spec=['principal'])
    ipn = IPNetworkGroup()
    ipn_p = MagicMock(principal=ipn, spec=['principal'])
    local_group = GroupProxy(123, _group=MagicMock())
    local_group_p = MagicMock(principal=local_group, spec=['principal'])
    remote_group = GroupProxy('foo', 'bar')
    remote_group_p = MagicMock(principal=remote_group, spec=['principal'])
    acl = [ipn, user_p, remote_group, local_group_p, user, local_group, remote_group_p, ipn_p]
    assert list(iter_acl(iter(acl))) == [user_p, user,
                                         ipn, ipn_p,
                                         local_group_p, local_group,
                                         remote_group, remote_group_p]


def test_unify_user_args(dummy_avatar):
    avatar = dummy_avatar
    user = dummy_avatar.user

    @unify_user_args
    def fn(a, b, c, d, e, f):
        # posargs
        assert a == 'foo'
        assert b == user
        assert c == user
        # kwargs
        assert d == 'bar'
        assert e == user
        assert f == user

    fn('foo', user, avatar, d='bar', e=user, f=avatar)
