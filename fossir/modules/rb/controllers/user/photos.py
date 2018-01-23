

import posixpath
from io import BytesIO

from flask import redirect

from fossir.core.config import config
from fossir.legacy.common.cache import GenericCache
from fossir.modules.rb.models.photos import Photo
from fossir.modules.rb.models.rooms import Room
from fossir.web.flask.util import send_file


_cache = GenericCache('Rooms')


def _redirect_no_photo(size):
    return redirect(posixpath.join(config.IMAGES_BASE_URL, 'rooms/{}_photos/NoPhoto.jpg'.format(size)))


def room_photo(roomID, size, **kw):
    cache_key = 'photo-{}-{}'.format(roomID, size)
    photo_data = _cache.get(cache_key)

    if photo_data == '*':
        return _redirect_no_photo(size)
    elif photo_data is None:
        photo = Photo.find_first(Room.id == roomID, _join=Photo.room)
        if photo is None:
            _cache.set(cache_key, '*')
            return _redirect_no_photo(size)
        photo_data = photo.thumbnail if size == 'small' else photo.data
        _cache.set(cache_key, photo_data)

    io = BytesIO(photo_data)
    return send_file('photo-{}.jpg'.format(size), io, 'image/jpeg', no_cache=False)
