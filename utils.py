import re
import unicodedata
import pyperclip
from string import Template

def slugify(text:str) -> str:
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

def copy_buyer_script_to_clipboard(buyer_address: str, buyer_name:str, product_name: str, quantity_requested: int)-> None:
    buyer_script = """
    Hi, my name is $buyer_name. I have a company in Brazil, with tax id and import license. 
    
    I am interested in the product $product_name, please send me the quotation for $quantity_requested pcs, I also need the freight costs using courier companies as DHL, Fedex or UPS, my address is $buyer_address.
    """
    template = Template(buyer_script)
    text = template.substitute(
        buyer_address=buyer_address.upper(),
        buyer_name=buyer_name,
        product_name=product_name.upper(),
        quantity_requested=quantity_requested,
    )
    pyperclip.copy(text)
