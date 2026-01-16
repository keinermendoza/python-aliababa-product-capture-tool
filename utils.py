import re
import unicodedata

def slugify(text):
    # Normaliza acentos
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Minúsculas
    text = text.lower()
    
    # Reemplaza todo lo que no sea letra/número por guion
    text = re.sub(r'[^a-z0-9]+', '-', text)
    
    # Quita guiones al inicio o final
    text = text.strip('-')
    
    return text