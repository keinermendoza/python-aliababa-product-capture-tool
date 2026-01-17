from sqlalchemy import Row
import csv
from pathlib import Path
from utils import slugify

def write_cotations_csv(request_cotation_with_cotations: dict) -> str | None:
    dir_path = Path("csv")
    dir_path.mkdir(exist_ok=True)

    if not len(request_cotation_with_cotations["cotations"]):
        return

    request = request_cotation_with_cotations["request"]
    cotations = request_cotation_with_cotations["cotations"]
    
    filename = slugify(f"{request.title}_{request.created.strftime('%Y-%m-%d %H')}") + ".csv"
    path = dir_path / filename
    columns = cotations[0]._mapping.keys()
    print("COLUMNS ######", columns)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(cotation._mapping for cotation in cotations)

    return str(path)
