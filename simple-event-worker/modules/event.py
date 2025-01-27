from enum import Enum


class EventType(Enum):
    ACCOUNT_CREATED = "AccountCreated"
    ACCOUNT_RECALLED = "AccountRecalled"
    ACCOUNT_CHARGE_RECEIVED = "AccountChargeReceived"
    ACCOUNT_PAYMENT_RECEIVED = "AccountPaymentReceived"

    def __eq__(self, other):
        return self.value == other


class Event:
    def __init__(self, type: str, account_id: str, payload: dict):
        self.type = EventType(type)
        self.account_id = account_id
        self.payload = self._validate_payload(payload)

    def __repr__(self):
        return f"Event(type={self.type}, account_id={self.account_id}, payload={self.payload})"

    def _validate_payload(self, payload: dict) -> dict:
        if self.type == EventType.ACCOUNT_CREATED:
            if "Balance" not in payload:
                raise ValueError(
                    '"Balance" is required in payload for ACCOUNT_CREATED events'
                )
        elif self.type == EventType.ACCOUNT_CHARGE_RECEIVED:
            if "Amount" not in payload:
                raise ValueError(
                    '"Amount" is required in payload for ACCOUNT_CHARGE_RECEIVED events'
                )
            if payload["Amount"] < 0:
                raise ValueError("Amount in payload must be positive")
        elif self.type == EventType.ACCOUNT_PAYMENT_RECEIVED:
            if "Amount" not in payload:
                raise ValueError(
                    '"Amount" is required in payload for ACCOUNT_PAYMENT_RECEIVED events'
                )
            if payload["Amount"] < 0:
                raise ValueError("Amount in payload must be positive")
        elif self.type == EventType.ACCOUNT_RECALLED:
            pass  # no payload validation needed
        else:
            raise ValueError(f"Unknown event type: {self.type}")
        return payload
