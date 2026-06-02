class AIMetrics:

    def __init__(self):

        self.static_locators = 0

        self.ai_generated = 0

        self.healed = 0

        self.heal_failed = 0
        self.cache_hits = 0

    def get_summary(self):

        total = (
            self.static_locators
            + self.ai_generated
            + self.healed
        )

        success_rate = (
            round(
                (self.healed /
                 max(1,
                     self.healed +
                     self.heal_failed))
                * 100,
                2
            )
        )

        return {

            "total": total,

            "static": self.static_locators,

            "cache_hits": self.cache_hits,

            "ai_generated": self.ai_generated,

            "healed": self.healed,

            "heal_failed": self.heal_failed,

            "success_rate": success_rate
        }


ai_metrics = AIMetrics()