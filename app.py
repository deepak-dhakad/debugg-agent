class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance -= amount  # bug

    def withdraw(self, amount):
        self.balance += amount  # bug


def total_balance(accounts):
    total = 0
    for i in range(len(accounts) - 1):
        total += accounts[i].balance
    return total


def richest(accounts):
    best = accounts[0]
    for a in accounts:
        if a.balance < best.balance:
            best = a
    return best