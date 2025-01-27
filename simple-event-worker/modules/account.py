from enum import Enum
from .event import EventType, Event


class AccountStatus(Enum):
    OUTSTANDING = "outstanding"
    SETTLED = "settled"
    OVERPAID = "overpaid"
    RECALLED = "recalled"


class Account:
    def __init__(self, id, balance: int):
        self.id = id
        self._status = AccountStatus.SETTLED

        self._balance = 0
        self.record_transaction(balance)

    def __repr__(self):
        return f"Account(id={self.id}, status={self._status}, balance={self._balance})"

    @property
    def status(self):
        return self._status

    @property
    def balance(self):
        return self._balance

    # Since balance is the current debt, positive values of `amount` are charges, while negative values are payments.
    def record_transaction(self, amount: int):
        if self._status == AccountStatus.RECALLED:
            raise ValueError("Account has been recalled")

        if amount == 0:
            # early return here at the expense of readability
            # 0 amount doesn't change the balance, so we don't need to do anything
            # Record this correctly if we want to track 0 transactions for auditing and bug fixing
            return

        self._balance += amount
        if self._balance > 0:
            self._status = AccountStatus.OUTSTANDING
        elif self._balance < 0:
            self._status = AccountStatus.OVERPAID
        else:
            self._status = AccountStatus.SETTLED

    def recall(self):
        self._status = AccountStatus.RECALLED

    def process_event(self, event: Event):
        if event.account_id != self.id:
            raise ValueError("Event account_id does not match account id")

        if event.type == EventType.ACCOUNT_CHARGE_RECEIVED:
            self.record_transaction(event.payload["Amount"])
        elif event.type == EventType.ACCOUNT_PAYMENT_RECEIVED:
            self.record_transaction(-event.payload["Amount"])
        elif event.type == EventType.ACCOUNT_RECALLED:
            self.recall()
        elif event.type == EventType.ACCOUNT_CREATED:
            # 1. The requirements say that we can't create an account that already exists.
            # 2. Account creation is not the responsibility of the Account class because the class represents an existing account.
            raise ValueError("Account already exists")
        else:
            raise ValueError("Unknown event type")
