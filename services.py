from datetime import date
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from schema import (
    cotations_table,
    request_cotations_table,
    selected_request_cotation
) 

class RequestCotationDosentExist(Exception):
    pass

def save_cotation_in_db(data: dict) -> dict:
    request_cotation_id = get_current_request_cotation_id()
    store_cotation(request_cotation_id, data)
    return {
        "title": "Rodillo de masageador de belleza",
        "date": date.today()
    }

def get_current_request_cotation_id():
    try:
        # select request_cotation_id from selected_cotation
        # return id: int
        id = 1
    except Exception:
        raise RequestCotationDosentExist("por favor cree una RequestCotation antes de intentar salvar cotaciones individuales")
    return id 

def store_cotation(request_cotation_id, cotation_data):
    # insert into cotations (request_cotation_id, )
    insert(cotations_table).values(
        company_name=cotation_data["company_name"],
        company_url=cotation_data["company_url"],
        product_name=cotation_data["product_name"],
        product_url=cotation_data["product_url"],
        public_minimum_price=cotation_data["public_minimum_price"],
        public_minimum_quantity=cotation_data["public_minimum_quantity"],
        request_cotation_id=request_cotation_id
    )
