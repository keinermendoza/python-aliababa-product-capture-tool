from typing import NamedTuple
import csv
from pathlib import Path
from utils import slugify



def write_cotations_csv(request_cotation: NamedTuple, row: dict) -> None:
    row.update({
        "seller":"",
        "real_price":"",
        "quantity_coted":""
    })
    
    dir_path = Path("csv")
    dir_path.mkdir(exist_ok=True)
    
    filename = slugify(f"{request_cotation.title}_{request_cotation.created.strftime('%Y-%m-%d %H')}") + ".csv"
    path = dir_path / filename

    if not row:
        return

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writeheader()
        writer.writerow(row)
