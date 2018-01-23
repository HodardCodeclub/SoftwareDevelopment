

from functools import wraps

from flask import request
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import NotFound

from indico.modules.rb import Room
from indico.modules.rb.models.locations import Location
from indico.util.decorators import smart_decorator
from indico.util.i18n import _


@smart_decorator
def requires_location(f, parameter_name='roomLocation', attribute_name='_location', request_attribute='view_args'):
    @wraps(f)
    def wrapper(*args, **kw):
        location_name = getattr(request, request_attribute).get(parameter_name, None)
        location = Location.find_first(name=location_name)
        if not location:
            raise NotFound(_('There is no location named: {0}').format(location_name))
        setattr(args[0], attribute_name, location)
        return f(*args, **kw)

    return wrapper


@smart_decorator
def requires_room(f, parameter_name='roomID', attribute_name='_room', location_attribute_name='_location',
                  request_attribute='view_args'):
    @wraps(f)
    def wrapper(*args, **kw):
        location = getattr(args[0], location_attribute_name)

        room_id = getattr(request, request_attribute).get(parameter_name, None)
        try:
            room = Room.query.with_parent(location).filter_by(id=room_id).one()
        except NoResultFound:
            raise NotFound(_("There is no room at '{1}' with id: {0}").format(room_id, location.name))
        setattr(args[0], attribute_name, room)
        return f(*args, **kw)

    return wrapper
