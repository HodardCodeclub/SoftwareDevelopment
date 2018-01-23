
import pytest

from fossir.modules.events.payment.models.transactions import PaymentTransaction, TransactionStatus


@pytest.fixture
def create_transaction():
    """Returns a callable which lets you create transactions"""

    def _create_transaction(status, **params):
        params.setdefault('amount', 10)
        params.setdefault('currency', 'USD')
        params.setdefault('provider', '_manual')
        params.setdefault('data', {})
        return PaymentTransaction(status=status, **params)

    return _create_transaction


@pytest.fixture
def dummy_transaction(create_transaction):
    """Gives you a dummy successful transaction"""
    return create_transaction(status=TransactionStatus.successful)
