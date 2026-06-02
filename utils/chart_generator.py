import os
import matplotlib.pyplot as plt


class ChartGenerator:

    @staticmethod
    def generate_pass_fail_chart(
            passed,
            failed
    ):

        os.makedirs(
            "reports/charts",
            exist_ok=True
        )

        labels = [
            "Passed",
            "Failed"
        ]

        values = [
            passed,
            failed
        ]

        colors = [
            "#28a745",
            "#dc3545"
        ]

        plt.figure(
            figsize=(5, 5)
        )

        plt.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            colors=colors
        )

        plt.title(
            "Pass vs Fail"
        )

        chart_path = (
            "reports/charts/"
            "pass_fail_chart.png"
        )

        plt.savefig(
            chart_path,
            bbox_inches="tight"
        )

        plt.close()

        return (
            "charts/"
            "pass_fail_chart.png"
        )

    @staticmethod
    def generate_execution_time_chart(results):

        import os
        import matplotlib.pyplot as plt

        os.makedirs(
            "reports/charts",
            exist_ok=True
        )

        test_ids = [
            r["id"]
            for r in results
        ]

        durations = [
            r["duration"]
            for r in results
        ]

        plt.figure(
            figsize=(8, 5)
        )

        plt.bar(
            test_ids,
            durations
        )

        plt.title(
            "Execution Time Per Test"
        )

        plt.xlabel(
            "Test Cases"
        )

        plt.ylabel(
            "Duration (sec)"
        )

        chart_path = (
            "reports/charts/"
            "execution_time_chart.png"
        )

        plt.savefig(
            chart_path,
            bbox_inches="tight"
        )

        plt.close()

        return (
            "charts/"
            "execution_time_chart.png"
        )

    @staticmethod
    def generate_module_chart(results):

        import os
        import matplotlib.pyplot as plt

        os.makedirs(
            "reports/charts",
            exist_ok=True
        )

        module_stats = {}

        for r in results:

            module = r["module"]

            if module not in module_stats:
                module_stats[module] = {
                    "total": 0,
                    "passed": 0
                }

            module_stats[module]["total"] += 1

            if r["status"] == "PASSED":
                module_stats[module]["passed"] += 1

        modules = []

        pass_rates = []

        for module, data in module_stats.items():
            modules.append(module)

            pass_rates.append(

                round(
                    data["passed"]
                    / data["total"]
                    * 100,
                    2
                )

            )

        plt.figure(
            figsize=(8, 5)
        )

        plt.bar(
            modules,
            pass_rates,
            color=[
                "#28a745" if rate == 100
                else "#dc3545"
                for rate in pass_rates
            ]
        )

        plt.ylim(0, 100)

        plt.ylabel(
            "Pass Rate %"
        )

        plt.title(
            "Module Wise Pass Rate"
        )

        chart_path = (
            "reports/charts/"
            "module_pass_rate.png"
        )

        plt.savefig(
            chart_path,
            bbox_inches="tight"
        )

        plt.close()

        return (
            "charts/"
            "module_pass_rate.png"
        )

    @staticmethod
    def generate_ai_locator_chart(metrics):

        import os
        import matplotlib.pyplot as plt

        os.makedirs(
            "reports/charts",
            exist_ok=True
        )

        labels = [
            "Static",
            "AI Generated",
            "Healed"
        ]

        values = [

            metrics["static"],

            metrics["ai_generated"],

            metrics["healed"]
        ]

        plt.figure(
            figsize=(6, 6)
        )

        plt.pie(

            values,

            labels=labels,

            autopct="%1.1f%%"

        )

        plt.title(
            "AI Locator Distribution"
        )

        chart_path = (
            "reports/charts/"
            "ai_locator_distribution.png"
        )

        plt.savefig(
            chart_path,
            bbox_inches="tight"
        )

        plt.close()

        return (
            "charts/"
            "ai_locator_distribution.png"
        )
