from datetime import date

from src.entities.customer import Customer, PhoneNumber
from src.repositories.retail_crm import RetailCRM
from src.request import RequestModel
from src.response import ResponseFailure, ResponseModel, ResponseSuccess

from .base_use_case import BaseUseCase


class GetCustomersUseCase(BaseUseCase):
    class Request(RequestModel):
        name: str | None = None
        email: str | None = None
        date_from: date | None = None
        date_to: date | None = None

    class Response(ResponseModel):
        customers: list[Customer]

    def __init__(self, repo: RetailCRM):
        self.retail_crm = repo

    async def execute(self, request: Request) -> ResponseSuccess | ResponseFailure:
        try:
            resp = await self.retail_crm.get_customers(**request.dict())

            customers = [
                Customer(
                    id=customer.get("id"),
                    first_name=customer.get("firstName"),
                    last_name=customer.get("lastName"),
                    email=customer.get("email"),
                    phones=[
                        PhoneNumber(number=phone.get("number"))
                        for phone in customer.get("phones")
                    ],
                    created_at=customer.get("createdAt"),
                    site=customer.get("site"),
                )
                for customer in resp
            ]

            payload = self.Response(customers=customers)
            return ResponseSuccess.build(
                payload=payload, status=ResponseSuccess.ResponseStatus.SUCCESS
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
