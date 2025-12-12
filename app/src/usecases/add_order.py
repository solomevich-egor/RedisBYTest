from src.entities import Order, Product
from src.repositories.retail_crm import RetailCRM
from src.request import RequestModel
from src.response import ResponseFailure, ResponseModel, ResponseSuccess

from .base_use_case import BaseUseCase


class AddOrderUseCase(BaseUseCase):
    class Request(RequestModel):
        customer_id: int
        items: list[Product]

    class Response(ResponseModel):
        id: int

    def __init__(self, retail_crm_repo: RetailCRM):
        self.retail_crm = retail_crm_repo

    async def execute(self, request: Request) -> ResponseSuccess | ResponseFailure:
        try:
            order = Order(
                customer_id=request.customer_id,
                items=request.items,
            )
            order_id = await self.retail_crm.add_order(order)

            payload = self.Response(id=order_id)
            return ResponseSuccess.build(
                payload=payload, status=ResponseSuccess.ResponseStatus.CREATED
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
