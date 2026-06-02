
import os
from datetime import datetime

def capture(page, name):

    os.makedirs("reports/screenshots", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    path = f"screenshots/{name}_{timestamp}.png"

    page.screenshot(path=path)

    return f"screenshots/{name}_{timestamp}.png"
