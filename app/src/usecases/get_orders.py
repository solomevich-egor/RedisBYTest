from src.entities import Order, Product
from src.repositories.retail_crm import RetailCRM
from src.request import RequestModel
from src.response import ResponseFailure, ResponseModel, ResponseSuccess

from .base_use_case import BaseUseCase


class GetOrdersUseCase(BaseUseCase):
    class Request(RequestModel):
        customer_id: int

    class Response(ResponseModel):
        orders: list[Order]

    def __init__(self, retail_crm_repo: RetailCRM):
        self.retail_crm = retail_crm_repo

    async def execute(self, request: Request) -> ResponseSuccess | ResponseFailure:
        try:
            resp = await self.retail_crm.get_orders(customer_id=request.customer_id)

            orders = [
                Order(
                    id=order["id"],
                    customer_id=order["customer"]["id"],
                    items=[
                        Product(
                            id=item["id"],
                            product_name=item["offer"]["displayName"],
                            initial_price=item["initialPrice"],
                            purchase_price=item["purchasePrice"],
                        )
                        for item in order.get("items")
                    ],
                )
                for order in resp
            ]

            payload = self.Response(orders=orders)
            return ResponseSuccess.build(
                payload=payload, status=ResponseSuccess.ResponseStatus.SUCCESS
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
