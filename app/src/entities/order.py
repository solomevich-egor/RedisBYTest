from enum import StrEnum

from pydantic import BaseModel


class Product(BaseModel):
    id: int | None = None
    product_name: str
    initial_price: float
    purchase_price: float


class Order(BaseModel):
    id: int | None = None
    customer_id: int
    items: list[Product]


class PaymentType(StrEnum):
    CASH = "cash"
    BANK_CARD = "bank-card"
    E_MONEY = "e-money"
    BANK_TRANSFER = "bank-transfer"
    CREDIT = "credit"


class PaymentStatus(StrEnum):
    NOT_PAID = "not-paid"
    INVOICE = "invoice"
    WAIT_APPROVED = "wait-approved"
    PAYMENT_START = "payment-start"
    CANCELED = "canceled"
    CREDIT_CHECK = "credit-check"
    CREDIT_APPROVED = "credit-approved"
    FAIL = "fail"
    PAID = "paid"
    RETURNED = "returned"


class DeliveryType(StrEnum):
    COURIER = "courier"
    SELF_DELIVERY = "self-delivery"


class Payment(BaseModel):
    id: int | None = None
    order_id: int
    type: PaymentType
    amount: float
    status: PaymentStatus
