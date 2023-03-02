import dataclasses

from airtable import airtable

import purrfect_creations.core_types


@dataclasses.dataclass
class PurrfectCreationsAirtableClient(object):
    airtable_client: airtable.Airtable

    def get_orders(self) -> list[purrfect_creations.core_types.Order]:
        raw_orders = [o for o in self.airtable_client.iterate(table_name="Orders")]
        orders = [
            purrfect_creations.core_types.Order.from_json(order_json=o["fields"])
            for o in raw_orders
        ]
        return orders


def get_airtable_client(
    airtable_base: str, api_key: str
) -> PurrfectCreationsAirtableClient:
    at = airtable.Airtable(base_id=airtable_base, api_key=api_key)
    return PurrfectCreationsAirtableClient(airtable_client=at)
