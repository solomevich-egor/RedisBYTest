from src.entities import Payment, PaymentStatus, PaymentType
from src.repositories.retail_crm import RetailCRM
from src.request import RequestModel
from src.response import ResponseFailure, ResponseModel, ResponseSuccess

from .base_use_case import BaseUseCase


class AddOrderPaymentUseCase(BaseUseCase):
    class Request(RequestModel):
        order_id: int
        type: PaymentType
        amount: float
        status: PaymentStatus

    class Response(ResponseModel):
        id: int

    def __init__(self, retail_crm_repo: RetailCRM):
        self.retail_crm = retail_crm_repo

    async def execute(self, request: Request) -> ResponseSuccess | ResponseFailure:
        try:
            payment = Payment(**request.dict())
            payment_id = await self.retail_crm.add_order_payment(payment)

            payload = self.Response(id=payment_id)
            return ResponseSuccess(
                payload=payload, status=ResponseSuccess.ResponseStatus.CREATED
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
