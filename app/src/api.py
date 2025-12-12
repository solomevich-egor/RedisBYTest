import httpx
from fastapi import APIRouter, Depends, HTTPException
from src.deps import get_client
from src.repositories import RetailCRM
from src.response import ResponseFailure
from src.usecases import (AddCustomerUseCase, AddOrderPaymentUseCase,
                          AddOrderUseCase, GetCustomersUseCase,
                          GetOrdersUseCase)

router = APIRouter()


@router.get("/customers", response_model=GetCustomersUseCase.Response)
async def get_users(
    request: GetCustomersUseCase.Request = Depends(),
    client: httpx.AsyncClient = Depends(get_client),
):
    retail_crm_repo = RetailCRM(client)
    use_case = GetCustomersUseCase(retail_crm_repo)

    response = await use_case.execute(request)
    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status.value, detail=response.err_msg)
    return response.payload


@router.post("/customers/create", response_model=AddCustomerUseCase.Response)
async def add_customer(
    request: AddCustomerUseCase.Request,
    client: httpx.AsyncClient = Depends(get_client),
):
    retail_crm_repo = RetailCRM(client)
    use_case = AddCustomerUseCase(retail_crm_repo)

    response = await use_case.execute(request)
    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status.value, detail=response.err_msg)
    return response.payload


@router.get("/orders", response_model=GetOrdersUseCase.Response)
async def get_orders(
    request: GetOrdersUseCase.Request = Depends(),
    client: httpx.AsyncClient = Depends(get_client),
):
    retail_crm_repo = RetailCRM(client)
    use_case = GetOrdersUseCase(retail_crm_repo)

    response = await use_case.execute(request)
    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status.value, detail=response.err_msg)
    return response.payload


@router.post("/orders/create", response_model=AddOrderUseCase.Response)
async def add_order(
    request: AddOrderUseCase.Request,
    client: httpx.AsyncClient = Depends(get_client),
):
    retail_crm_repo = RetailCRM(client)
    use_case = AddOrderUseCase(retail_crm_repo)

    response = await use_case.execute(request)
    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status.value, detail=response.err_msg)
    return response.payload


@router.post("/orders/payments/create", response_model=AddOrderPaymentUseCase.Response)
async def add_order_payment_method(
    request: AddOrderPaymentUseCase.Request,
    client: httpx.AsyncClient = Depends(get_client),
):
    retail_crm_repo = RetailCRM(client)
    use_case = AddOrderPaymentUseCase(retail_crm_repo)

    response = await use_case.execute(request)
    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status.value, detail=response.err_msg)
    return response.payload
