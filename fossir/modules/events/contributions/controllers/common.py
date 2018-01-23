

from __future__ import unicode_literals

from flask import redirect


class ContributionListMixin:
    """Display list of contributions"""

    view_class = None
    template = None

    def _process(self):
        if self.list_generator.static_link_used:
            return redirect(self.list_generator.get_list_url())
        return self._render_template(**self.list_generator.get_list_kwargs())

    def _render_template(self, selected_entry, **kwargs):
        return self.view_class.render_template(self.template, self.event, selected_entry=selected_entry, **kwargs)
