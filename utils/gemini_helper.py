import json
import re

from google import genai

from config.settings import GEMINI_API_KEY


client = genai.Client(
    api_key=GEMINI_API_KEY
)


# =========================================================
# ENTERPRISE LOCATOR NORMALIZER
# =========================================================

def normalize_locator(locator):

    import re

    # ==========================================
    # BASIC CLEANUP
    # ==========================================

    locator = (
        locator
        .replace("getByRole", "get_by_role")
        .replace("getByText", "get_by_text")
        .replace("getByPlaceholder", "get_by_placeholder")
        .replace("getByLabel", "get_by_label")
        .replace("```python", "")
        .replace("```", "")
        .strip()
    )

    # ==========================================
    # FIX get_by_role(button, name=Login)
    # ==========================================

    locator = re.sub(
        r'get_by_role\((\w+),\s*name=(\w+)\)',
        lambda m: (
            f'get_by_role('
            f'"{m.group(1)}", '
            f'name="{m.group(2)}"'
            f')'
        ),
        locator
    )

    # ==========================================
    # FIX get_by_label(Username)
    # ==========================================

    locator = re.sub(
        r'get_by_label\((\w+)\)',
        lambda m: (
            f'get_by_label('
            f'"{m.group(1)}"'
            f')'
        ),
        locator
    )

    # ==========================================
    # FIX get_by_placeholder(Username)
    # ==========================================

    locator = re.sub(
        r'get_by_placeholder\((\w+)\)',
        lambda m: (
            f'get_by_placeholder('
            f'"{m.group(1)}"'
            f')'
        ),
        locator
    )

    # ==========================================
    # FIX get_by_text(Dashboard)
    # ==========================================

    locator = re.sub(
        r'get_by_text\((\w+)\)',
        lambda m: (
            f'get_by_text('
            f'"{m.group(1)}"'
            f')'
        ),
        locator
    )

    # ==========================================
    # FIX page.locator(...)
    # ==========================================

    if "locator(" in locator:

        match = re.search(
            r'locator\((.+)\)',
            locator
        )

        if match:

            selector = (
                match.group(1)
                .strip()
                .strip('"')
                .strip("'")
            )

            locator = (
                f'locator("{selector}")'
            )

    # ==========================================
    # FORCE page. PREFIX
    # ==========================================

    if not locator.startswith("page."):

        locator = f"page.{locator}"

    # ==========================================
    # FINAL CLEANUP
    # ==========================================

    locator = locator.replace(
        '""',
        '"'
    )

    print(
        f"Normalized Locator: {locator}"
    )

    return locator


# =========================================================
# ENTERPRISE LOCATOR GENERATOR
# =========================================================

def generate_locator(element_description):

    prompt = f"""
    You are an expert Python Playwright automation engineer.

    Generate ONLY ONE valid Python Playwright locator.

    STRICT RULES:
    - Return ONLY locator
    - No markdown
    - No explanation
    - No comments
    - No async
    - No await
    - Always start with page.
    - Always generate VALID PYTHON syntax
    - Never generate JavaScript Playwright syntax
    
    2. Use CORRECT semantic role

    Examples:
    - button -> buttons
    - link -> anchor tags
    - textbox -> inputs
    - checkbox -> checkboxes
    - menuitem -> menus
    
    IMPORTANT:
    Navigation menus in OrangeHRM are usually LINKS not BUTTONS.
    "Add Employee" is a LINK.
    "PIM" is a LINK.
    "Admin" is a LINK.
    
    VALID EXAMPLES:

    page.get_by_role(\"button\", name=\"Login\")

    page.get_by_text(\"Dashboard\")

    page.get_by_placeholder(\"Search\")

    page.get_by_label(\"Username\")

    page.locator(\"input[name='username']\")
    
    APPLICATION SPECIFIC RULES FOR ORANGEHRM:

    1. Left sidebar menus are LINKS
    2. Top navigation tabs are LINKS
    3. Save/Login are BUTTONS
    4. Username/password are TEXTBOXES
    5. Logout is usually TEXT
    6. User dropdown is DIV/SPAN clickable element
    
    Examples:
    
    PIM menu:
    page.get_by_role("link", name="PIM")
    
    Add Employee:
    page.get_by_role("link", name="Add Employee")
    
    Login:
    page.get_by_role("button", name="Login")
    
    Username:
    page.locator("input[name='username']")
    ELEMENT:
    {element_description}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    locator = normalize_locator(
        response.text.strip()
    )

    print(f"Normalized Locator: {locator}")

    return locator


# =========================================================
# ENTERPRISE TESTCASE GENERATOR
# =========================================================

def generate_test_script(task):

    prompt = f"""
    You are a senior Python Playwright automation engineer.

    Generate COMPLETE executable pytest testcase.

    STRICT RULES:
    - Sync Playwright only
    - No async
    - No await
    - No fixtures
    - No markdown
    - Return ONLY executable Python code

    FRAMEWORK:

    from utils.browser import BrowserManager
    from pages.login_page import LoginPage
    from config.settings import BASE_URL, USERNAME, PASSWORD
    from playwright.sync_api import expect

    browser = BrowserManager()

    page = browser.start()

    login_page = LoginPage(page)

    login_page.open(BASE_URL)

    login_page.login(USERNAME, PASSWORD)

    Scenario:
    {task}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    script = response.text.strip()

    script = (
        script
        .replace("```python", "")
        .replace("```", "")
        .replace("getByRole", "get_by_role")
        .replace("getByText", "get_by_text")
        .replace("getByPlaceholder", "get_by_placeholder")
        .replace("getByLabel", "get_by_label")
        .strip()
    )

    return script


# =========================================================
# ENTERPRISE SELF-HEALING LOCATOR GENERATOR
# =========================================================

def generate_healing_locator(element_description):

    prompt = f"""
    You are an enterprise self-healing Playwright AI engine.

    Generate ONE fallback locator.

    STRICT RULES:
    - Return ONLY locator
    - No markdown
    - No explanation
    - Always return VALID PYTHON Playwright syntax
    - Always start with page.
    - Never generate JavaScript syntax

    VALID EXAMPLES:

    page.get_by_text(\"Dashboard\")

    page.get_by_role(\"button\", name=\"Save\")

    page.get_by_placeholder(\"Search\")

    page.get_by_label(\"Username\")

    page.locator(\"input[name='username']\")

    ELEMENT:
    {element_description}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    locator = normalize_locator(
        response.text.strip()
    )

    print(f"Healed Locator: {locator}")

    return locator

def generate_test_steps(scenario):

    prompt = f"""
    You are an expert Playwright automation engineer.

    Convert testcase into JSON test steps.

    STRICT RULES:
    - Return ONLY JSON
    - No markdown
    - No explanation
    - No Python code

    VALID ACTIONS:
    - click
    - fill
    - verify

    VALID FORMAT:

    [
        {{
            "action": "click",
            "element": "PIM menu"
        }},
        {{
            "action": "verify",
            "element": "Employee List page"
        }}
    ]

    SCENARIO:
    {scenario}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = (
        response.text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return json.loads(text)