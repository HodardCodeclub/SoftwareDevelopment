

from __future__ import unicode_literals

from datetime import timedelta

import pytest

from fossir.modules.events.contributions.models.contributions import Contribution


@pytest.fixture
def create_contribution(db):
    """Returns a a callable that lets you create a contribution"""

    def _create_contribution(event, title, duration):
        entry = Contribution(event=event, title=title, duration=duration)
        db.session.add(entry)
        db.session.flush()
        return entry

    return _create_contribution


@pytest.fixture
def dummy_contribution(create_contribution, dummy_event):
    return create_contribution(dummy_event, "Dummy Contribution", timedelta(minutes=20))
