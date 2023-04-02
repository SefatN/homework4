import unittest
from io import StringIO
from unittest.mock import patch
from shop import display_items, get_user_choice, get_additional_money, buy_item, InsufficientFundsError, shop


class TestShop(unittest.TestCase):

    def test_display_items(self):
        items = {"bread": 50, "chips": 80, "milk": 120}
        expected_output = "Here are the available items:- \n" \
                          "bread: £50\n" \
                          "chips: £80\n" \
                          "milk: £120\n"
        with patch('sys.stdout', new=StringIO()) as fake_output:
            display_items(items)
            self.assertEqual(fake_output.getvalue(), expected_output)

    def test_get_user_choice_valid_choice(self):
        items = {"bread": 50, "chips": 80, "milk": 120}
        with patch('builtins.input', return_value='bread'):
            self.assertEqual(get_user_choice(items), 'bread')

    def test_get_user_choice_invalid_choice(self):
        items = {"bread": 50, "chips": 80, "milk": 120}
        with patch('builtins.input', return_value='juice\nbread'):
            self.assertEqual(get_user_choice(items), 'bread')

    def test_get_additional_money_valid_input(self):
        with patch('builtins.input', return_value='50'):
            self.assertEqual(get_additional_money(), 50)

    def test_get_additional_money_invalid_input(self):
        with patch('builtins.input', side_effect=['abcd\n50']):
            self.assertEqual(get_additional_money(), 50)

    def test_buy_item_valid_purchase(self):
        items = {"bread": 50, "chips": 80, "milk": 120}
        customer_money = 100
        with patch('builtins.input', return_value='bread'):
            self.assertEqual(buy_item('bread', customer_money, items), (50, 0))

    def test_buy_item_insufficient_funds(self):
        items = {"bread": 50, "chips": 80, "milk": 120}
        customer_money = 20
        with patch('builtins.input', side_effect=['50', '0']):
            with self.assertRaises(InsufficientFundsError):
                buy_item('bread', customer_money, items)

    def test_shop(self):
        items = {"bread": 50, "chips": 80, "milk": 120}
        customer_money = 100
        with patch('builtins.input', side_effect=['milk', '50', 'exit']):
            with patch('sys.stdout', new=StringIO()) as fake_output:
                shop()
                self.assertIn(f"You have £{customer_money-120} left.", fake_output.getvalue())

if __name__ == '__main__':
    unittest.main()
