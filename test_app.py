from app import BankAccount, total_balance, richest


def test_bank_account_init():
    account = BankAccount("John")
    assert account.owner == "John"
    assert account.balance == 0


def test_deposit():
    account = BankAccount("Jane", 100)
    account.deposit(50)
    # Expected correct behavior: 100 + 50 = 150
    assert account.balance == 150


def test_withdraw():
    account = BankAccount("Bob", 200)
    account.withdraw(100)
    # Expected correct behavior: 200 - 100 = 100
    assert account.balance == 100

def test_total_balance_basic():
    accounts = [
        BankAccount("A", 100),
        BankAccount("B", 200),
        BankAccount("C", 300)
    ]
    # Expected: 600
    assert total_balance(accounts) == 600


def test_total_balance_single():
    accounts = [BankAccount("Only", 500)]
    assert total_balance(accounts) == 500


def test_richest_basic():
    accounts = [
        BankAccount("A", 100),
        BankAccount("B", 500),
        BankAccount("C", 300)
    ]
    assert richest(accounts).owner == "B"


def test_richest_last():
    accounts = [
        BankAccount("A", 100),
        BankAccount("B", 200),
        BankAccount("C", 1000)
    ]
    assert richest(accounts).owner == "C"

def test_deposit_withdraw_flow():
    account = BankAccount("Mike")
    account.deposit(200)
    account.withdraw(50)
    # Expected: 150
    assert account.balance == 150