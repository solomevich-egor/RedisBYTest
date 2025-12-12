import json
from datetime import date

import httpx
from src.configs import RetailCRMConfig
from src.entities import Customer, Order, Payment

from .exceptions import RetailCRMError


class RetailCRM:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.config = RetailCRMConfig()

    async def get_customers(
        self,
        *,
        name: str | None = None,
        email: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[dict]:
        url = f"https://{self.config.domain}/api/v5/customers"
        params = {
            "site": self.config.site,
        }

        if name:
            params["filter[name]"] = name
        if email:
            params["filter[email]"] = email
        if date_from:
            params["filter[dateFrom]"] = date_from.strftime("%Y-%m-%d")
        if date_to:
            params["filter[dateTo]"] = date_to.strftime("%Y-%m-%d")

        resp = (await self.client.get(url, params=params)).json()
        if not resp["success"]:
            raise RetailCRMError(resp)

        customer_info = resp.get("customers")
        return customer_info if customer_info else []

    async def add_customer(self, customer: Customer) -> int:
        url = f"https://{self.config.domain}/api/v5/customers/create"
        data = {
            "site": self.config.site,
            "customer": json.dumps(
                {
                    "firstName": customer.first_name,
                    "lastName": customer.last_name,
                    "email": customer.email,
                    "phones": [phone.dict() for phone in customer.phones],
                }
            ),
        }

        resp = (await self.client.post(url, data=data)).json()
        if not resp["success"]:
            raise RetailCRMError(resp)

        return resp["id"]

    async def get_orders(self, *, customer_id: int) -> list[dict]:
        url = f"https://{self.config.domain}/api/v5/orders"
        params = {"site": self.config.site, "filter[customerId]": customer_id}

        resp = (await self.client.get(url, params=params)).json()
        if not resp["success"]:
            raise RetailCRMError(resp)

        orders_info = resp.get("orders")
        return orders_info if orders_info else []

    async def add_order(self, order: Order):
        url = f"https://{self.config.domain}/api/v5/orders/create"
        data = {
            "site": self.config.site,
            "order": json.dumps(
                {
                    "customer": {"id": order.customer_id},
                    "items": [
                        {
                            "productName": product.product_name,
                            "initialPrice": product.initial_price,
                            "purchasePrice": product.purchase_price,
                        }
                        for product in order.items
                    ],
                }
            ),
        }

        resp = (await self.client.post(url, data=data)).json()
        if not resp["success"]:
            raise RetailCRMError(resp)

        return resp["id"]

    async def add_order_payment(self, payment: Payment) -> int:
        url = f"https://{self.config.domain}/api/v5/orders/payments/create"
        data = {
            "site": self.config.site,
            "payment": json.dumps(
                {
                    "order": {
                        "id": payment.order_id,
                    },
                    "type": payment.type,
                    "status": payment.status,
                    "amount": payment.amount,
                }
            ),
        }

        resp = (await self.client.post(url, data=data)).json()
        if not resp["success"]:
            raise RetailCRMError(resp)

        return resp.get("id")
