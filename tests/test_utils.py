from _pytest.fixtures import fixture

from src.dto import Operation
from src.utils import filter_operation_by_state


@fixture
def canceled_operation(operation_data_with_from):
    operation = Operation.init_from_dict(operation_data_with_from)
    operation.state = 'CANCELED'
    return operation


@fixture
def executed_operation(operation_data_with_from):
    operation = Operation.init_from_dict(operation_data_with_from)
    operation.state = 'EXECUTED'
    return operation


def test_filtered_operation(canceled_operation, executed_operation):
    operations = executed_operation, canceled_operation

    result = filter_operation_by_state(*operations, state='CANCELED')
    assert result == [canceled_operation]

    result = filter_operation_by_state(*operations, state='EXECUTED')
    assert result == [executed_operation]
