import unittest

from modules.event import Event, EventType


class TestEvent(unittest.TestCase):
    def test_event(self):
        event = Event(
            type=EventType.ACCOUNT_CREATED, account_id="1", payload={"Balance": 100}
        )
        self.assertEqual(event.type, EventType.ACCOUNT_CREATED)
        self.assertEqual(event.account_id, "1")
        self.assertEqual(event.payload, {"Balance": 100})

    def test_event_valid_charge(self):
        event = Event(
            type=EventType.ACCOUNT_CHARGE_RECEIVED,
            account_id="1",
            payload={"Amount": 100},
        )
        self.assertEqual(event.type, EventType.ACCOUNT_CHARGE_RECEIVED)
        self.assertEqual(event.account_id, "1")
        self.assertEqual(event.payload, {"Amount": 100})

    def test_event_valid_payment(self):
        event = Event(
            type=EventType.ACCOUNT_PAYMENT_RECEIVED,
            account_id="1",
            payload={"Amount": 100},
        )
        self.assertEqual(event.type, EventType.ACCOUNT_PAYMENT_RECEIVED)
        self.assertEqual(event.account_id, "1")
        self.assertEqual(event.payload, {"Amount": 100})

    def test_event_valid_recall_no_payload(self):
        event = Event(type=EventType.ACCOUNT_RECALLED, account_id="1", payload={})
        self.assertEqual(event.type, EventType.ACCOUNT_RECALLED)
        self.assertEqual(event.account_id, "1")
        self.assertEqual(event.payload, {})

    def test_event_invalid_payload(self):
        with self.assertRaises(ValueError):
            Event(type=EventType.ACCOUNT_CREATED, account_id="1", payload={})

    def test_event_account_charge_received_negative_amount(self):
        with self.assertRaises(ValueError):
            Event(
                type=EventType.ACCOUNT_CHARGE_RECEIVED,
                account_id="1",
                payload={"Amount": -100},
            )

    def test_event_account_payment_received_negative_amount(self):
        with self.assertRaises(ValueError):
            Event(
                type=EventType.ACCOUNT_PAYMENT_RECEIVED,
                account_id="1",
                payload={"Amount": -100},
            )

    def test_event_unknown_type(self):
        with self.assertRaises(ValueError):
            Event(type="UnknownType", account_id="1", payload={})
