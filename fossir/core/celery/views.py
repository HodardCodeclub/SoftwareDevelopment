

from __future__ import unicode_literals

from fossir.modules.admin.views import WPAdmin


class WPCelery(WPAdmin):
    template_prefix = 'celery/'
