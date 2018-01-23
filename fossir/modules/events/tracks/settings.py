

from __future__ import unicode_literals

from fossir.core.db.sqlalchemy.descriptions import RenderMode
from fossir.core.settings.converters import EnumConverter
from fossir.modules.events.settings import EventSettingsProxy


track_settings = EventSettingsProxy('tracks', {
    'program': '',
    'program_render_mode': RenderMode.markdown
}, converters={
    'program_render_mode': EnumConverter(RenderMode)
})
