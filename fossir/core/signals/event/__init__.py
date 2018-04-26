

# isort:skip_file

from blinker import Namespace


_signals = Namespace()

from fossir.core.signals.event.abstracts import *
from fossir.core.signals.event.contributions import *
from fossir.core.signals.event.core import *
from fossir.core.signals.event.designer import *
from fossir.core.signals.event.notes import *
from fossir.core.signals.event.persons import *
from fossir.core.signals.event.registration import *
from fossir.core.signals.event.timetable import *
