from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class RetailCRMConfig(BaseSettings):
    domain: str = Field(..., alias="RETAILCRM_DOMAIN")
    site: str = Field(..., alias="RETAILCRM_SITE")
    api_key: SecretStr = Field(..., alias="RETAILCRM_API_KEY")
