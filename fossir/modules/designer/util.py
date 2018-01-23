

from __future__ import unicode_literals

from sqlalchemy.orm import joinedload

from fossir.core.db import db
from fossir.modules.designer.models.templates import DesignerTemplate
from fossir.modules.designer.placeholders import GROUP_TITLES
from fossir.modules.events.models.events import Event
from fossir.modules.events.registration.models.forms import RegistrationForm
from fossir.util.date_time import now_utc
from fossir.util.placeholders import get_placeholders


def get_placeholder_options():
    groups = {group_id: {'title': group_title, 'options': {}} for group_id, group_title in GROUP_TITLES.viewitems()}
    for pname, placeholder in get_placeholders('designer-fields').viewitems():
        groups[placeholder.group]['options'][pname] = placeholder.description
    return groups


def get_all_templates(obj):
    """Get all templates usable by an event/category"""
    category = obj.category if isinstance(obj, Event) else obj
    return set(DesignerTemplate.find_all(DesignerTemplate.category_id.in_(categ['id'] for categ in category.chain)))


def get_inherited_templates(obj):
    """Get all templates inherited by a given event/category"""
    return get_all_templates(obj) - set(obj.designer_templates)


def get_not_deletable_templates(obj):
    """Get all non-deletable templates for an event/category"""

    not_deletable_criteria = [
        DesignerTemplate.is_system_template,
        DesignerTemplate.backside_template_of != None,  # noqa
        DesignerTemplate.ticket_for_regforms.any(RegistrationForm.event.has(Event.ends_after(now_utc())))
    ]
    return set(DesignerTemplate.query.filter(DesignerTemplate.owner == obj, db.or_(*not_deletable_criteria)))


def get_default_template_on_category(category, only_inherited=False):
    if not only_inherited and category.default_ticket_template:
        return category.default_ticket_template
    parent_chain = category.parent_chain_query.options(joinedload('default_ticket_template')).all()
    return next((category.default_ticket_template for
                 category in reversed(parent_chain) if category.default_ticket_template), None)
