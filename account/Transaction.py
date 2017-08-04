class Transaction:

    def set(self, balance):
        self.balance = balance

    def credit(self, credit):
        self.balance -= credit

    def debit(self, debit):
        self.balance += debit

    def account(self):
        return self.balance
