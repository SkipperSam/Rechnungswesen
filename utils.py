import os
from datetime import date

DATA_DIR = "data"
RECHNUNGSNUMMER_FILE = os.path.join(DATA_DIR, "rechnungsnummer.txt")

def get_next_rechnungsnummer():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(RECHNUNGSNUMMER_FILE):
        num = 1
    else:
        with open(RECHNUNGSNUMMER_FILE, "r") as f:
            try:
                num = int(f.read().strip()) + 1
            except:
                num = 1
    with open(RECHNUNGSNUMMER_FILE, "w") as f:
        f.write(str(num))
    jahr = date.today().year
    return f"{jahr}{num:04d}"