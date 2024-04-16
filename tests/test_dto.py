from datetime import datetime

import pytest

from src.dto import Payment, Operation


def test_init_payment_from_str():
    payment = Payment.init_from_str('Visa Classic 6831982476737658')
    assert payment.name == 'Visa Classic'
    assert payment.number == '6831982476737658'


@pytest.mark.parametrize(
    ['payment_str', 'safe_payment'],
    [
        ('Счет 64686473678894779589', 'Счет, **9589'),
        ('MasterCard 7158300734726758', 'MasterCard, 7158 30** **** 6758'),
        ('Visa Classic 6831982476737658', 'Visa Classic, 6831 98** **** 7658')
    ]
)
def test_safe_payment_hide_number(payment_str, safe_payment):
    payment = Payment.init_from_str(payment_str)
    assert payment.safe() == safe_payment


def test_split_card_number_by_blocks():
    card_number = '7158300734726758'
    _result = Payment.split_card_number_by_blocks(card_number)
    assert _result == '7158 3007 3472 6758'


def test_init_operation__from_dict(operation_data_without_from):
    op = Operation.init_from_dict(operation_data_without_from)

    assert op.id == 522357576
    assert op.state == "EXECUTED"
    assert op.date == datetime(2019, 7, 12, 20, 41, 47, 882230)
    assert op.amount.value == 51463.70
    assert op.amount.currency_name == 'USD'
    assert op.amount.currency_code == 'USD'
    assert op.description == 'Открытие вклада'
    assert op.payment_to.name == 'Счет'
    assert op.payment_to.number == '38976430693692818358'


def test_safe_operation_with_from(operation_data_with_from):
    operation = Operation.init_from_dict(operation_data_with_from)
    expected_result = (
        '12.07.2019. Перевод организации\n'
        'Visa Classic, 6831 98** **** 7658 -> Счет, **8358\n'
        '51463.70 USD'
    )

    assert operation.safe() == expected_result


def test_safe_operation_without_from(operation_data_without_from):
    operation = Operation.init_from_dict(operation_data_without_from)
    expected_result = (
        '12.07.2019. Открытие вклада\n'
        'Счет, **8358\n'
        '51463.70 USD')

    assert operation.safe() == expected_result
