from src.entities.customer import Customer, PhoneNumber
from src.repositories.retail_crm import RetailCRM
from src.request import RequestModel
from src.response import ResponseFailure, ResponseModel, ResponseSuccess

from .base_use_case import BaseUseCase


class AddCustomerUseCase(BaseUseCase):
    class Request(RequestModel):
        first_name: str
        last_name: str
        email: str
        phones: list[PhoneNumber]

    class Response(ResponseModel):
        id: int

    def __init__(self, retail_crm_repo: RetailCRM):
        self.retail_crm = retail_crm_repo

    async def execute(self, request: Request) -> ResponseSuccess | ResponseFailure:
        try:
            customer = Customer(
                first_name=request.first_name,
                last_name=request.last_name,
                email=request.email,
                phones=request.phones,
            )

            customer_id = await self.retail_crm.add_customer(customer)

            payload = self.Response(id=customer_id)
            return ResponseSuccess.build(
                payload=payload, status=ResponseSuccess.ResponseStatus.CREATED
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
