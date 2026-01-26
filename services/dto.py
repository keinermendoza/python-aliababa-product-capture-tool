from pydantic import BaseModel
from datetime import datetime
from repositories.dto import (
    RequestForQuotationWithQuotationCount
)

class RequestForQuotationList(BaseModel):
    requests_with_quotations_count: list[RequestForQuotationWithQuotationCount]
    active_request_id: int

    class Config:
        from_attributes = True
