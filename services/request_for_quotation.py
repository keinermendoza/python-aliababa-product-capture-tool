from sqlalchemy import Engine, Row
from repository import SQLAlchemyRepository
from repositories.request_for_quotation import RequestForQuotationRepository
from .dto import RequestForQuotationList

class RequestForQuotationServices:
    @staticmethod
    def store_request_for_quotation(engine: Engine, data:dict) -> None:
        title = data.get("title", None)
        quantity = data.get("quantity", None)
        ref_product_url = data.get("ref_product_url", None)
        product_image_url = data.get("product_image_url", None)
        description = data.get("product_image_url", None)
        is_discarted = data.get("product_image_url", None)


        with engine.begin() as conn:
            repo = SQLAlchemyRepository(conn)
            request_for_quotations_id = repo.store_request_for_quotation(
                title=title,
                quantity=quantity,
                ref_product_url=ref_product_url,
                product_image_url=product_image_url,
                description=description,
                is_discarted=is_discarted
            )
            repo.set_active_request_for_quotation_id(request_for_quotations_id)

    @staticmethod
    def get_list_with_quotations_count(engine: Engine) -> RequestForQuotationList:
        with engine.begin() as conn:
            repo = RequestForQuotationRepository(conn)
            active_request_id = repo.get_active_request_for_quotation_id()
            requests_with_quotations_count = repo.get_list_with_quotations_count()

            return RequestForQuotationList(requests_with_quotations_count=requests_with_quotations_count, active_request_id=active_request_id)
    
    @staticmethod
    def get_request_for_quotation_by_id(engine: Engine, request_for_quotation_id: int):
        with engine.begin() as conn:
            repo = SQLAlchemyRepository(conn)
            return repo.get_request_for_quotation_by_id(request_for_quotation_id)

    @staticmethod
    def update_request_for_quotation(engine: Engine, request_for_quotation_id: int, data:dict):
        with engine.begin() as conn:
            SQLAlchemyRepository(conn).update_request_for_quotation(request_for_quotation_id=request_for_quotation_id, values_to_update=data)