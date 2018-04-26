

from blinker import Namespace


_signals = Namespace()


get_definitions = _signals.signal('get-definitions', """
Expected to return a list of AgreementDefinition classes.
""")
