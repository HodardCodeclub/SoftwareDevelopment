

from fossir.modules.rb.models.aspects import Aspect


pytest_plugins = 'fossir.modules.rb.testing.fixtures'


def test_default_on_startup(dummy_location, db):
    aspect = Aspect(name=u'Test', center_latitude='', center_longitude='', zoom_level=0, top_left_latitude=0,
                    top_left_longitude=0, bottom_right_latitude=0, bottom_right_longitude=0)
    dummy_location.aspects.append(aspect)
    db.session.flush()
    assert not aspect.default_on_startup
    dummy_location.default_aspect = aspect
    db.session.flush()
    assert aspect.default_on_startup
