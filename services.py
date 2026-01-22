from sqlalchemy import Engine, Row
from repository import SQLAlchemyRepository

def get_quotation_list_data(
        engine: Engine,
        request_for_quotation_id: int,
        query: str,
        fields_to_exclude: list[str] = None
    ):

    # REMOVE tuples WHERE column IS NOT NULL;
    # uses SET to filter only by allowed fields
    allowed_fields = {"seller_name", "cheapest_shipping_cost"}
    fields_to_process = set(fields_to_exclude)
    _fields_to_exclude = allowed_fields.intersection(fields_to_process)

    with engine.begin() as conn:
        repo = SQLAlchemyRepository(conn)
        request_for_quotation = repo.get_request_for_quotation_by_id(request_for_quotation_id)
        
        quotations = repo.filter_quotations(
            request_for_quotation_id,
            query,
            _fields_to_exclude
        )

        # get all available quotation status
        map_quotation_status_to_bootstrap_classes = {
            "just quoted": "secondary",
            "waiting for me": "warning",
            "need shipping quotation": "danger",
            "completed": "primary",
            "discarted": "info",
            "selected": "success",
        }

    return {"request": request_for_quotation, "quotations":quotations, "css_status":map_quotation_status_to_bootstrap_classes}
    

def get_quotation_edit_data(
        engine: Engine,
        quotation_id: int
    ):
    with engine.begin() as conn:
        repo = SQLAlchemyRepository(conn)
        quotation = repo.get_quotation_by_id(quotation_id)
        status = repo.get_quotation_status()

    return {"quotation": quotation, "status":status}

def update_quotation(
        engine: Engine,
        quotation_id: int,
        data: dict
    ):

    with engine.begin() as conn:
        repo = SQLAlchemyRepository(conn)
        quotation = repo.get_quotation_by_id(quotation_id)

        editable_fields = [
            "public_minimum_price",
            "public_minimum_quantity",
            "seller_name",
            "cheapest_shipping_company",
            "cheapest_shipping_cost",
            "unit_product_price_offered",
            "status_id",
        ]
        
        values_to_update = {}

        # fill the empty fields with old instance data
        for key in editable_fields:
            if not data.get(key):
                values_to_update[key] = quotation._mapping[key]
            else:
                values_to_update[key] = data[key]

        repo.update_quotation(quotation.id, values_to_update)