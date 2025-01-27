import unittest

from modules.account import Account, AccountStatus


class TestAccount(unittest.TestCase):
    def test_account_creation(self):
        account = Account("123", 100)
        self.assertEqual(account.id, "123")
        self.assertEqual(account.status, AccountStatus.OUTSTANDING)
        self.assertEqual(account.balance, 100)

    def test_account_charge(self):
        account = Account("123", 100)
        account.record_transaction(50)
        self.assertEqual(account.status, AccountStatus.OUTSTANDING)
        self.assertEqual(account.balance, 150)

    def test_account_payment(self):
        account = Account("123", 100)
        account.record_transaction(-50)
        self.assertEqual(account.status, AccountStatus.OUTSTANDING)
        self.assertEqual(account.balance, 50)

    def test_account_settled(self):
        account = Account("123", 100)
        account.record_transaction(-100)
        self.assertEqual(account.status, AccountStatus.SETTLED)
        self.assertEqual(account.balance, 0)

    def test_account_overpayment(self):
        account = Account("123", 100)
        account.record_transaction(-150)
        self.assertEqual(account.status, AccountStatus.OVERPAID)
        self.assertEqual(account.balance, -50)

    def test_account_recall(self):
        account = Account("123", 100)
        account.recall()
        self.assertEqual(account.status, AccountStatus.RECALLED)
        self.assertEqual(account.balance, 100)

    def test_account_invalid_recall(self):
        account = Account("123", 100)
        account.recall()
        with self.assertRaises(ValueError):
            account.record_transaction(50)

    def test_account_invalid_recall_payment(self):
        account = Account("123", 100)
        account.recall()
        with self.assertRaises(ValueError):
            account.record_transaction(-50)
