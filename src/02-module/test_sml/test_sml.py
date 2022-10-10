from tkinter import W
from sml import synthetic_data
from unittest import TestCase
import pytest
from contextlib import nullcontext as does_not_raise
import numpy


@pytest.mark.parametrize(
    "credit_card_number, cash_amounts, length, delta, radius, country_code, excp",
    [("1111 2222 3333 4444",[112.10, 11.23], 1, 1, 10.0, 'US', does_not_raise())
    ,("1111 2222 3333 44",[-12.00], -1, 1, 1.0, 'IE', pytest.raises(Exception))]
)    
def test_generate_atm_withdrawal(credit_card_number: str, cash_amounts: list, length: int, \
                                 delta: int, radius: float, country_code, excp):
    with excp:
        synthetic_data.generate_atm_withdrawal(credit_card_number, cash_amounts, length, delta, radius, country_code)


def test_generate_list_credit_card_numbers():
    credit_card = synthetic_data.generate_list_credit_card_numbers()
    assert(type(credit_card[0]['cc_num']) == str)


@pytest.mark.parametrize(
    "cc_num, provider, expires, age",
    [("4720347042991709", "visa", "07/27", 95 ),
    ("4720347042991709", "visa", "07/27", 95),
    ("4720347042991709", "visa", "07/27", 95),
    pytest.param("4720347042991709", "visa", "07/27", 195, marks=pytest.mark.xfail(strict=True))
    ]
)
def test_create_credit_cards_as_df(cc_num: str, provider: str, expires: str, age: int):
    cards = synthetic_data.create_credit_cards_as_df([{'cc_num': cc_num, 'provider' : provider, 'expires': expires, 'age': age}])
    card = cards.iloc[0]
    assert (type(card['cc_num']) == numpy.int64)
    assert (type(card['provider']) == str)
    assert (type(card['expires']) == str)
    assert (type(card['age']) == numpy.int64)
    assert ((card['age'] > 0) and (card['age'] < 120))
 