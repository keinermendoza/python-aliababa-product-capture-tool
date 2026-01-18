from sqlalchemy import func, select, insert, update, Connection
from sqlalchemy.exc import IntegrityError
from schema import (
    quotations_table,
    request_for_quotations_table,
    active_request_for_quotations_table
) 

class SQLAlchemyRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def check_if_active_request_for_quotation_exists(self):
        """
        Check if a singleton instance exists in the active request table.
        
        The table manages a single record referencing the currently active 
        request quotation to determine whether to perform an insert or an update.
        """
        stmt = select(active_request_for_quotations_table.c.request_for_quotation_id)
        result = self.conn.execute(stmt)
        return result.first()

    def change_active_request_for_quotation(self, request_for_quotation_id: int):
        """
        Change the active request for quotation that new entries will be associated with.
        
        Raises exeception If the request quotation ID does not exist.
        """
        self.conn.execute(select(request_for_quotations_table).where(request_for_quotations_table.c.id==request_for_quotation_id)).one()
        self.set_active_request_for_quotation_id(request_for_quotation_id)

    def get_active_request_for_quotation_id(self) -> int | None:
        """
        Retrieve the ID of the 'active' request quotation.
        """
        if active_request_cotation := self.check_if_active_request_for_quotation_exists():
            return active_request_cotation.request_for_quotation_id
        
    def set_active_request_for_quotation_id(self, request_for_quotation_id: int):
        """
        Set the 'active' request quotation ID.
        """
        stmt = update(active_request_for_quotations_table).values(request_for_quotation_id=request_for_quotation_id)
        if not self.check_if_active_request_for_quotation_exists():
            stmt = insert(active_request_for_quotations_table).values(request_for_quotation_id=request_for_quotation_id)
        self.conn.execute(stmt)

    def store_request_for_quotation(self, title: str, quantity: int) -> int:
        """
        Store a new request quotation instance and return its primary key.
        """
        stmt = insert(request_for_quotations_table).values(title=title, quantity=quantity)
        result = self.conn.execute(stmt)
        return result.inserted_primary_key[0]

    def get_request_for_quotations_with_quotations_count(self):
        """
        Retrieve all request quotations along with the count of their associated quotations.
        """
        stmt = select(
            request_for_quotations_table.c.id,
            request_for_quotations_table.c.title,
            request_for_quotations_table.c.quantity,
            request_for_quotations_table.c.created,
            func.count(quotations_table.c.id).label("cotation_count")
        ).outerjoin(quotations_table, quotations_table.c.request_for_quotation_id == request_for_quotations_table.c.id).group_by(
            request_for_quotations_table.c.id
        )
        result = self.conn.execute(stmt)
        return result.fetchall()

    def get_request_for_quotation_by_id(self, request_for_quotation_id: int):
        """
        Retrieve a request quotation by ID.
        Raises exception if the request cotation does not exists
        """
        return self.conn.execute(
            select(request_for_quotations_table).where(request_for_quotations_table.c.id==request_for_quotation_id)
        ).one()

    def get_request_for_quotation_with_related_quotations_by_id(self, request_for_quotation_id: int) -> dict:
        """
        Retrieve a single request quotation and all its associated child quotations.
        """
        request_for_quotation = self.get_request_for_quotation_by_id(request_for_quotation_id)

        quotations = self.conn.execute(
            select(quotations_table).where(
                quotations_table.c.request_for_quotation_id==request_for_quotation_id
            ).order_by(quotations_table.c.id.desc())
        ).fetchall()

        return {"request": request_for_quotation, "cotations":quotations}

    def store_quotation(self, quotation_data):
        """
        Store an individual quotation associated with the currently active request.

        Raises: If no active request is active or if data integrity is violated.
        """
        if active_request_for_quotation_id := self.get_active_request_for_quotation_id():
            try:
                self.conn.execute(
                    insert(quotations_table).values(
                        company_name=quotation_data["company_name"],
                        company_url=quotation_data["company_url"],
                        product_name=quotation_data["product_name"],
                        product_url=quotation_data["product_url"],
                        public_minimum_price=quotation_data["price_offered"],
                        public_minimum_quantity=quotation_data["minimum_quantity"],
                        request_for_quotation_id=active_request_for_quotation_id
                    )
                )

            except KeyError as e:
                raise Exception(f"data dosen't acomplish the required contract") 
            except IntegrityError as e:
                raise Exception("you have already registered this porduct at this request for quotation")
            return True
        raise Exception("you must to generate a request for quotation before to store individual quotations")