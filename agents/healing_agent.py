
class HealingAgent:

    def heal_locator(self, page, text):

        try:
            locator = page.locator(f"text={text}")

            if locator.count() > 0:
                return locator

        except Exception as e:
            print(f"Healing failed: {e}")

        return None
