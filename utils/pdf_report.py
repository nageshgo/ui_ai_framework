import os

from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle, Image
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from utils.ai_metrics import ai_metrics


class PDFReportGenerator:

    @staticmethod
    def generate(
            results,
            report_path
    ):

        pdf_path = (
            report_path
            .replace(".html", ".pdf")
        )

        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=landscape(A4)
        )

        styles = (
            getSampleStyleSheet()
        )

        elements = []

        elements.append(

            Paragraph(
                "AI Automation Execution Report",
                styles["Title"]
            )
        )

        elements.append(
            Spacer(1, 20)
        )

        total = len(results)

        passed = len([
            r for r in results
            if r["status"] == "PASSED"
        ])

        failed = len([
            r for r in results
            if r["status"] == "FAILED"
        ])

        pass_rate = (
            round(
                passed * 100 / total,
                2
            )
            if total
            else 0
        )

        summary_data = [

            ["Metric", "Value"],

            ["Total Tests", total],

            ["Passed", passed],

            ["Failed", failed],

            ["Pass Rate", f"{pass_rate}%"]

        ]

        summary_table = Table(
            summary_data,
            colWidths=[200, 150]
        )

        summary_table.setStyle(

            TableStyle([

                (
                    'BACKGROUND',
                    (0, 0),
                    (-1, 0),
                    colors.lightblue
                ),

                (
                    'GRID',
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black
                )

            ])
        )

        elements.append(
            summary_table
        )
        elements.append(
            Paragraph(
                "AI Locator Analytics",
                styles["Heading2"]
            )
        )

        elements.append(
            Spacer(1, 10)
        )

        metrics = ai_metrics.get_summary()

        analytics_data = [

            ["Metric", "Value"],

            ["Static Locators",
             metrics["static"]],

            ["Cache Hits",
             metrics["cache_hits"]],

            ["AI Generated",
             metrics["ai_generated"]],

            ["Healed",
             metrics["healed"]],

            ["Heal Failed",
             metrics["heal_failed"]],

            ["Healing Success Rate",
             f"{metrics['success_rate']}%"]

        ]
        analytics_table = Table(
            analytics_data,
            colWidths=[250, 150]
        )

        analytics_table.setStyle(

            TableStyle([

                (
                    'BACKGROUND',
                    (0, 0),
                    (-1, 0),
                    colors.lightgreen
                ),

                (
                    'GRID',
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black
                )

            ])
        )

        elements.append(
            analytics_table
        )

        elements.append(
            Spacer(1, 20)
        )
        elements.append(
            Spacer(1, 20)
        )
        elements.append(
            Paragraph(
                "Execution Trend History",
                styles["Heading2"]
            )
        )

        elements.append(
            Spacer(1, 10)
        )

        trend_chart = (
            "reports/pass_rate_trend.png"
        )
        execution_chart = (
            "reports/execution_time_trend.png"
        )

        if os.path.exists(
                execution_chart
        ):
            elements.append(

                Paragraph(
                    "Execution Time Trend",
                    styles["Heading3"]
                )
            )

            elements.append(

                Image(
                    execution_chart,
                    width=450,
                    height=250
                )
            )

            elements.append(
                Spacer(1, 20)
            )

        if os.path.exists(
                trend_chart
        ):
            elements.append(

                Image(
                    trend_chart,
                    width=450,
                    height=250
                )
            )

            elements.append(
                Spacer(1, 20)
            )
        elements.append(

            Paragraph(
                "Test Execution Results",
                styles["Heading2"]
            )
        )

        table_data = [[

            "ID",
            "Scenario",
            "Status",
            "Duration"

        ]]

        for result in results:

            table_data.append([

                result["id"],

                Paragraph(
                    result["scenario"],
                    styles["BodyText"]
                ),
                result["status"],

                str(
                    result["duration"]
                )

            ])

        result_table = Table(
            table_data,
            colWidths=[
                60,
                320,
                80,
                80
            ]
        )

        result_table.setStyle(

            TableStyle([

                (
                    'BACKGROUND',
                    (0, 0),
                    (-1, 0),
                    colors.grey
                ),

                (
                    'TEXTCOLOR',
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),

                (
                    'GRID',
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black
                )

            ])
        )

        elements.append(
            result_table
        )

        doc.build(
            elements
        )

        print(
            f"\nPDF Report Generated:"
            f"\n{pdf_path}"
        )