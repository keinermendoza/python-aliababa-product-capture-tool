from sqlalchemy import Row
import csv
from pathlib import Path
from utils import slugify

def write_quotations_csv(request_for_quotation_with_quotations: dict) -> str | None:
    dir_path = Path("csv")
    dir_path.mkdir(exist_ok=True)

    if not len(request_for_quotation_with_quotations["quotations"]):
        return

    request = request_for_quotation_with_quotations["request"]
    quotations = request_for_quotation_with_quotations["quotations"]
    
    filename = slugify(f"{request.title}_{request.created.strftime('%Y-%m-%d %H')}") + ".csv"
    path = dir_path / filename
    columns = quotations[0]._mapping.keys()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(quotation._mapping for quotation in quotations)

    return str(path)
