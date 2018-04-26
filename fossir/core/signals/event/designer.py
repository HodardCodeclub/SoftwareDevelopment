from blinker import Namespace


_signals = Namespace()

print_badge_template = _signals.signal('print-badge-template', """
Called when printing a badge template. The registration form is passed in the `regform` kwarg.
""")
