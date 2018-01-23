

from fossir.modules.rb.controllers.admin import index as index_handler
from fossir.modules.rb.controllers.admin import locations as location_handlers
from fossir.modules.rb.controllers.admin import rooms as room_handlers
from fossir.web.flask.wrappers import fossirBlueprint


_bp = fossirBlueprint('rooms_admin', __name__, template_folder='../templates', virtual_template_folder='rb',
                      url_prefix='/admin/rooms')


# Main settings
_bp.add_url_rule('/config/',
                 'settings',
                 index_handler.RHRoomBookingSettings,
                 methods=('GET', 'POST'))


# Locations
_bp.add_url_rule('/locations/',
                 'roomBooking-admin',
                 location_handlers.RHRoomBookingAdmin)

_bp.add_url_rule('/locations/delete',
                 'roomBooking-deleteLocation',
                 location_handlers.RHRoomBookingDeleteLocation,
                 methods=('POST',))

_bp.add_url_rule('/locations/add',
                 'roomBooking-saveLocation',
                 location_handlers.RHRoomBookingSaveLocation,
                 methods=('POST',))

_bp.add_url_rule('/locations/set-default',
                 'roomBooking-setDefaultLocation',
                 location_handlers.RHRoomBookingSetDefaultLocation,
                 methods=('POST',))

_bp.add_url_rule('/location/<locationId>/',
                 'roomBooking-adminLocation',
                 location_handlers.RHRoomBookingAdminLocation)

_bp.add_url_rule('/location/<locationId>/attribute/delete',
                 'roomBooking-deleteCustomAttribute',
                 location_handlers.RHRoomBookingDeleteCustomAttribute,
                 methods=('POST',))

_bp.add_url_rule('/location/<locationId>/attribute/save',
                 'roomBooking-saveCustomAttributes',
                 location_handlers.RHRoomBookingSaveCustomAttribute,
                 methods=('POST',))

_bp.add_url_rule('/location/<locationId>/equipment/delete',
                 'roomBooking-deleteEquipment',
                 location_handlers.RHRoomBookingDeleteEquipment,
                 methods=('POST',))

_bp.add_url_rule('/location/<locationId>/equipment/save',
                 'roomBooking-saveEquipment',
                 location_handlers.RHRoomBookingSaveEquipment,
                 methods=('POST',))


# Rooms
_bp.add_url_rule('/room/<roomLocation>/<int:roomID>/delete',
                 'delete_room',
                 room_handlers.RHRoomBookingDeleteRoom,
                 methods=('POST',))

_bp.add_url_rule('/room/<roomLocation>/create',
                 'create_room',
                 room_handlers.RHRoomBookingCreateRoom,
                 methods=('GET', 'POST'))

_bp.add_url_rule('/room/<roomLocation>/<int:roomID>/modify',
                 'modify_room',
                 room_handlers.RHRoomBookingModifyRoom,
                 methods=('GET', 'POST'))
