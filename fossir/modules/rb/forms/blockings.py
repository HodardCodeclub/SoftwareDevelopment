


from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, ValidationError

from fossir.modules.rb.models.blocked_rooms import BlockedRoom
from fossir.modules.rb.models.blockings import Blocking
from fossir.modules.rb.models.rooms import Room
from fossir.util.i18n import _
from fossir.web.forms.base import fossirForm
from fossir.web.forms.fields import fossirDateField, JSONField, PrincipalListField


class BlockingForm(fossirForm):
    reason = TextAreaField(_(u'Reason'), [DataRequired()])
    principals = PrincipalListField(groups=True, allow_external=True)
    blocked_rooms = JSONField(default=[])

    def validate_blocked_rooms(self, field):
        try:
            field.data = map(int, field.data)
        except Exception as e:
            # In case someone sent crappy data
            raise ValidationError(str(e))

        # Make sure all room ids are valid
        if len(field.data) != Room.find(Room.id.in_(field.data)).count():
            raise ValidationError('Invalid rooms')

        if hasattr(self, '_blocking'):
            start_date = self._blocking.start_date
            end_date = self._blocking.end_date
            blocking_id = self._blocking.id
        else:
            start_date = self.start_date.data
            end_date = self.end_date.data
            blocking_id = None

        overlap = BlockedRoom.find_first(
            BlockedRoom.room_id.in_(field.data),
            BlockedRoom.state != BlockedRoom.State.rejected,
            Blocking.start_date <= end_date,
            Blocking.end_date >= start_date,
            Blocking.id != blocking_id,
            _join=Blocking
        )
        if overlap:
            msg = 'Your blocking for {} is overlapping with another blocking.'.format(overlap.room.full_name)
            raise ValidationError(msg)


class CreateBlockingForm(BlockingForm):
    start_date = fossirDateField(_(u'Start date'), [DataRequired()])
    end_date = fossirDateField(_(u'End date'), [DataRequired()])

    def validate_start_date(self, field):
        if self.start_date.data > self.end_date.data:
            raise ValidationError('Blocking may not end before it starts!')

    validate_end_date = validate_start_date
