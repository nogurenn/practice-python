import sys

# Let's use ijson to parse the JSON file in a streaming fashion.
# stdlib has no tokenizer for JSON, so handling json.raw_decode requires managing a lot of edge cases.
# For example, json.raw_decode fails if the buffered data is not an exact JSON value (e.g. extra whitespace, commas, etc.).
# ijson is a good library for this purpose.
import ijson
from modules.account import Account
from modules.event import Event, EventType


def main() -> int:
    accounts = {}
    with open("events.json", "r") as f:
        for json_event in ijson.items(f, "item"):
            try:
                event = Event(
                    type=json_event["Type"],
                    account_id=json_event["AccountID"],
                    payload=json_event["Payload"],
                )
                if event.type == EventType.ACCOUNT_CREATED:
                    if event.account_id in accounts:
                        print(
                            f"Account {event.account_id} already exists but received another ACCOUNT_CREATED event"
                        )
                        return 1
                    accounts[event.account_id] = Account(
                        id=event.account_id, balance=event.payload["Balance"]
                    )
                else:
                    accounts[event.account_id].process_event(event)
            except ValueError as e:
                print(f"Error processing event: {e}")
                return 1

    for account in accounts.values():
        print(
            f"{account.id}: {{ Status: {account.status.value}, Balance: {account.balance} }}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
