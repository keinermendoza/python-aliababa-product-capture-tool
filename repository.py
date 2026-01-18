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

    def check_if_selected_request_cotation_exists(self):
        """
        Check if a singleton instance exists in the selected request table.
        
        The table manages a single record referencing the currently active 
        request quotation to determine whether to perform an insert or an update.
        """
        stmt = select(active_request_for_quotations_table.c.request_for_quotation_id)
        result = self.conn.execute(stmt)
        return result.first()

    def change_selected_request_cotation(self, request_for_quotation_id: int):
        """
        Change the active request quotation that new entries will be associated with.
        
        Raises exeception If the request quotation ID does not exist.
        """
        self.conn.execute(select(request_for_quotations_table).where(request_for_quotations_table.c.id==request_for_quotation_id)).one()
        self.set_selected_request_cotation_id(request_for_quotation_id)

    def get_selected_request_cotation_id(self) -> int | None:
        """
        Retrieve the ID of the 'active' request quotation.
        """
        if selected_request_cotation := self.check_if_selected_request_cotation_exists():
            return selected_request_cotation.request_for_quotation_id
        
    def set_selected_request_cotation_id(self, request_for_quotation_id: int):
        """
        Set the 'active' request quotation ID.
        """
        stmt = update(active_request_for_quotations_table).values(request_for_quotation_id=request_for_quotation_id)
        if not self.check_if_selected_request_cotation_exists():
            stmt = insert(active_request_for_quotations_table).values(request_for_quotation_id=request_for_quotation_id)
        self.conn.execute(stmt)

    def store_request_cotation(self, title: str, quantity: int) -> int:
        """
        Store a new request quotation instance and return its primary key.
        """
        stmt = insert(request_for_quotations_table).values(title=title, quantity=quantity)
        result = self.conn.execute(stmt)
        return result.inserted_primary_key[0]

    def get_request_cotations_with_cotations_count(self):
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

    def get_request_cotation(self, request_for_quotation_id: int):
        """
        Retrieve a request quotation by ID.
        Raises exception if the request cotation does not exists
        """
        return self.conn.execute(
            select(request_for_quotations_table).where(request_for_quotations_table.c.id==request_for_quotation_id)
        ).one()

    def get_request_cotation_with_related_cotations(self, request_for_quotation_id: int) -> dict:
        """
        Retrieve a single request quotation and all its associated child quotations.
        """
        request_cotation = self.get_request_cotation(request_for_quotation_id)

        cotations = self.conn.execute(
            select(quotations_table).where(
                quotations_table.c.request_for_quotation_id==request_for_quotation_id
            ).order_by(quotations_table.c.id.desc())
        ).fetchall()

        return {"request": request_cotation, "cotations":cotations}

    def store_cotation(self, cotation_data):
        """
        Store an individual cuotation associated with the currently selected request.

        Raises: If no active request is selected or if data integrity is violated.
        """
        if selected_request_cotation_id := self.get_selected_request_cotation_id():
            try:
                self.conn.execute(
                    insert(quotations_table).values(
                        company_name=cotation_data["company_name"],
                        company_url=cotation_data["company_url"],
                        product_name=cotation_data["product_name"],
                        product_url=cotation_data["product_url"],
                        public_minimum_price=cotation_data["price_offered"],
                        public_minimum_quantity=cotation_data["minimum_quantity"],
                        request_for_quotation_id=selected_request_cotation_id
                    )
                )

            except KeyError as e:
                raise Exception(f"data dosen't acomplish the required contract") 
            except IntegrityError as e:
                raise Exception("you have already registered this porduct at this request cotation")
            return True
        raise Exception("you must to generate a request cotation before to store individual cotations")