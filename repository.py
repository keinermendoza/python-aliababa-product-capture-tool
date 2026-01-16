from sqlalchemy import func, select, insert, update, Connection
from sqlalchemy.exc import IntegrityError
from schema import (
    cotations_table,
    request_cotations_table,
    selected_request_cotation_table
) 
def get_selected_request_cotation(conn: Connection):
    """
    selected request cotation must to manage a single instance
    referencing wich is the active request cotation.
    Help to differentiate when it's necessary create or update the single instance 
    """
    stmt = select(selected_request_cotation_table.c.request_cotation_id)
    result = conn.execute(stmt)
    return result.first()

def get_selected_request_cotation_id(conn: Connection) -> int | None:
    if selected_request_cotation := get_selected_request_cotation(conn):
        return selected_request_cotation.request_cotation_id
    
def set_selected_request_cotation_id(conn:Connection, request_cotation_id: int):
    stmt = update(selected_request_cotation_table).values(request_cotation_id=request_cotation_id)
    if not get_selected_request_cotation(conn):
        stmt = insert(selected_request_cotation_table).values(request_cotation_id=request_cotation_id)
    conn.execute(stmt)

def store_request_cotation(conn:Connection, title: str) -> int:
    stmt = insert(request_cotations_table).values(title=title)
    result = conn.execute(stmt)
    return result.inserted_primary_key[0]

def get_request_cotations_with_cotations_count(conn:Connection):
    stmt = select(
        request_cotations_table.c.id,
        request_cotations_table.c.title,
        request_cotations_table.c.created,
        func.count(cotations_table.c.id).label("cotation_count")
    ).outerjoin(cotations_table, cotations_table.c.request_cotation_id == request_cotations_table.c.id).group_by(
        request_cotations_table.c.id
    )
    result = conn.execute(stmt)
    return result.fetchall()

def get_request_cotation_with_related_cotations(conn: Connection, request_cotation_id: int) -> dict:
    request_cotation = conn.execute(
        select(request_cotations_table).where(request_cotations_table.c.id==request_cotation_id)
    ).one()

    cotations = conn.execute(
        select(cotations_table).where(cotations_table.c.request_cotation_id==request_cotation_id)
    ).fetchall()

    return {"request": request_cotation, "cotations":cotations}

def store_cotation(conn, cotation_data):
    if selected_request_cotation_id := get_selected_request_cotation_id(conn):
        try:
            conn.execute(
                insert(cotations_table).values(
                    company_name=cotation_data["company_name"],
                    company_url=cotation_data["company_url"],
                    product_name=cotation_data["product_name"],
                    product_url=cotation_data["product_url"],
                    public_minimum_price=cotation_data["price_offered"],
                    public_minimum_quantity=cotation_data["minimum_quantity"],
                    request_cotation_id=selected_request_cotation_id
                )
            )

        except KeyError as e:
            raise Exception(f"data dosen't acomplish the required contract") 
        except IntegrityError as e:
            raise Exception("you have already registered this porduct at this request cotation")
        return True
    raise Exception("you must to generate a request cotation before to store individual cotations")