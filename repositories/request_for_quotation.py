from sqlalchemy import func, select, insert, update, delete, or_, Connection, Row, Sequence
from sqlalchemy.exc import IntegrityError
from schema import (
    quotations_table,
    request_for_quotations_table,
    active_request_for_quotations_table,
    quotation_status_table
) 
from repositories.dto import (
    RequestForQuotationWithQuotationCount,
    ActiveRequestForQuotation,
)
class RequestForQuotationRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def get_list_with_quotations_count(self) -> list[RequestForQuotationWithQuotationCount]:
        """
        Retrieve all request quotations along with the count of their associated quotations.
        """
        stmt = select(
            request_for_quotations_table,
            func.count(quotations_table.c.id).label("quotation_count")
        ).outerjoin(quotations_table, quotations_table.c.request_for_quotation_id == request_for_quotations_table.c.id).group_by(
            request_for_quotations_table.c.id
        )
        result = self.conn.execute(stmt)
        request_rows: Sequence[Row] = result.fetchall()
        return [RequestForQuotationWithQuotationCount.model_validate(row) for row in request_rows]
    
    def get_active_request_for_quotation(self) -> ActiveRequestForQuotation:
        """
        Check if a singleton instance exists in the active request table.
        
        The table manages a single record referencing the currently active 
        request quotation to determine whether to perform an insert or an update.
        """
        stmt = select(active_request_for_quotations_table.c.request_for_quotation_id)
        result = self.conn.execute(stmt)
        return result.first()


    def get_active_request_for_quotation_id(self) -> int | None:
        """
        Retrieve the ID of the 'active' request quotation.
        """
        if active_request_for_quotation := self.get_active_request_for_quotation():
            return active_request_for_quotation.request_for_quotation_id