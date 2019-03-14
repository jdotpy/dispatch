import time
import pytest
from unittest import mock

from dispatch.core import Reactor


@pytest.fixture
def reactor():
    return Reactor()

def test_basic(reactor):
    m = mock.MagicMock()
    reactor.dispatch(
        reactor.schedule_interval(seconds=1),
        reactor.background_action(m)
    )
    reactor.run_in_background()
    time.sleep(1.1)
    reactor.stop()
    assert m.call_count == 2
