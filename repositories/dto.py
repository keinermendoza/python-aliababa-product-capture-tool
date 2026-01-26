from pydantic import BaseModel
from datetime import datetime

class RequestForQuotationWithQuotationCount(BaseModel):
    id: int
    title: str
    quantity: int
    created: datetime
    is_discarted: bool
    ref_product_url: str | None
    product_image_url: str | None
    description: str | None
    quotation_count: int

    class Config:
        from_attributes = True

class ActiveRequestForQuotation(BaseModel):
    request_for_quotation_id: int

    class Config:
        from_attributes = True
