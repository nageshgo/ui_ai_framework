from datetime import datetime
import os

from matplotlib import pyplot as plt

from utils.ai_metrics import ai_metrics
from utils.chart_generator import ChartGenerator
from utils.failure_analytics import FailureAnalytics
from utils.history_manager import HistoryManager
from utils.pdf_report import PDFReportGenerator


class ReportManager:

    def __init__(
            self,
            browser="Chromium",
            environment="QA",
            framework="Playwright + Gemini AI",
            execution_mode="AI Dynamic"
    ):

        self.results = []

        self.start_time = datetime.now()

        self.browser = browser

        self.environment = environment

        self.framework = framework

        self.execution_mode = execution_mode

    def add_result(
            self,
            testcase_id,
            scenario,
            module,
            status,
            duration,
            error="",
            screenshot="",
            steps=None,
            locator_history=None,
            healing_history=None
    ):

        self.results.append({

            "id": testcase_id,

            "scenario": scenario,
            "module": module,

            "status": status,

            "duration": round(duration, 2),

            "error": error,

            "screenshot": screenshot,

            "steps": steps or [],
            "locator_history":
                locator_history or [],
            "healing_history":
                healing_history or []

        })

    def generate_html_report(self):

        end_time = datetime.now()

        passed = len([
            r for r in self.results
            if r["status"] == "PASSED"
        ])

        failed = len([
            r for r in self.results
            if r["status"] == "FAILED"
        ])

        total = len(self.results)

        pass_rate = (
            round((passed / total) * 100, 2)
            if total > 0
            else 0
        )

        HistoryManager.save_run(

            total=total,

            passed=passed,

            failed=failed,

            pass_rate=pass_rate,

            execution_time=round(
                (
                        end_time -
                        self.start_time
                ).total_seconds(),
                2
            ),

            ai_metrics=
            ai_metrics.get_summary()
        )

        top_failures = (
            FailureAnalytics
            .get_top_failures()
        )

        history = (
            HistoryManager.load_history()
        )

        labels = [
            f"Run {i + 1}"
            for i in range(
                len(history)
            )
        ]
        pass_rates = [
            h["pass_rate"]
            for h in history
        ]
        execution_times = [

            h["execution_time"]

            for h in history
        ]
        # =====================================
        # PASS RATE TREND CHART
        # =====================================

        if history:

            plt.figure(
                figsize=(8, 4)
            )

            plt.plot(

                labels,

                pass_rates,

                marker="o"
            )

            plt.title(
                "Pass Rate Trend"
            )

            plt.xlabel(
                "Execution Runs"
            )

            plt.ylabel(
                "Pass Rate %"
            )

            plt.grid(True)

            plt.tight_layout()

            pass_rate_chart_path = (
                "reports/pass_rate_trend.png"
            )

            plt.savefig(
                pass_rate_chart_path
            )

            plt.close()

        else:

            pass_rate_chart_path = ""

        # =====================================
        # EXECUTION TIME TREND CHART
        # =====================================

        if history:

            plt.figure(
                figsize=(8, 4)
            )

            plt.plot(

                labels,

                execution_times,

                marker="o"
            )

            plt.title(
                "Execution Time Trend"
            )

            plt.xlabel(
                "Execution Runs"
            )

            plt.ylabel(
                "Duration (sec)"
            )

            plt.grid(True)

            plt.tight_layout()

            execution_chart_path = (
                "reports/execution_time_trend.png"
            )

            plt.savefig(
                execution_chart_path
            )

            plt.close()

        else:

            execution_chart_path = ""

        history_rows = ""

        for idx, run in enumerate(
                reversed(history[-10:]),
                start=1
        ):
            history_pass_rate = run.get(
                "pass_rate",
                0
            )

            color = (
                "green"
                if history_pass_rate >= 80
                else "orange"
                if history_pass_rate  >= 50
                else "red"
            )

            history_rows += f"""
            <tr>

                <td>Run {idx}</td>

                <td>{run.get('timestamp', '-')}</td>

                <td>
                    <span style="
                    color:{color};
                    font-weight:bold;
                    ">
                    {history_pass_rate}%
                    </span>
                </td>

                <td>
                    {run.get(
                'failed',
                0
            )}
                </td>

                <td>
                    {run.get(
                'execution_time',
                0
            )} sec
                </td>

                <td>
                    {run.get(
                'ai_generated',
                0
            )}
                </td>

                <td>
                    {run.get(
                'healed',
                0
            )}
                </td>

            </tr>
            """
        failure_rows = ""

        for element, count in top_failures:
            failure_rows += f"""
            <tr>
                <td>{element}</td>
                <td>{count}</td>
            </tr>
            """

        failure_html = f"""
        <h2>
        Top Failed Elements
        </h2>

        <table
        style="
        width:50%;
        margin-bottom:30px;
        ">

        <tr
        style="
        background:#e74c3c;
        color:white;
        font-weight:bold;
        ">
            <th>Element</th>
            <th>Failures</th>
        </tr>

        {failure_rows}

        </table>
        """

        metrics = ai_metrics.get_summary()

        smart_locators = 0
        generic_locators = 0

        for result in self.results:

            for heal in result.get(
                    "healing_history",
                    []
            ):

                if heal.get(
                        "locator_type"
                ) == "SMART":

                    smart_locators += 1

                else:

                    generic_locators += 1

        ai_locator_chart = (
            ChartGenerator
            .generate_ai_locator_chart(
                metrics
            )
        )
        chart_path = (
            ChartGenerator
            .generate_pass_fail_chart(
                passed,
                failed
            )
        )
        execution_chart = (
            ChartGenerator
            .generate_execution_time_chart(
                self.results
            )
        )
        module_chart = (
            ChartGenerator
            .generate_module_chart(
                self.results
            )
        )

        dashboard_html = f"""
        <div class="dashboard">

            <div class="card total-card">
                <div class="card-value">
                    {total}
                </div>
                <div class="card-label">
                    Total Tests
                </div>
            </div>

            <div class="card pass-card">
                {passed}
                <div class="card-label">
                    Passed
                </div>
            </div>

            <div class="card fail-card">
                {failed}
                <div class="card-label">
                    Failed
                </div>
            </div>

            <div class="card rate-card">
                {pass_rate}%
                <div class="card-label">
                    Pass Rate
                </div>
            </div>
            <div class="card blue">
                <h1>
                    {metrics['cache_hits']}
                </h1>
                <p>Cache Hits</p>
            </div>

        </div>
        """
        ai_dashboard_html = f"""
        <h2 style="margin-top:40px;">
        AI Locator Analytics
        </h2>

        <div class="dashboard">

            <div class="card total-card">
                {metrics["static"]}
                <div class="card-label">
                    Static Locators
                </div>
            </div>

            <div class="card pass-card">
                {metrics["ai_generated"]}
                <div class="card-label">
                    AI Generated
                </div>
            </div>

            <div class="card rate-card">
                {metrics["healed"]}
                <div class="card-label">
                    Healed
                </div>
            </div>

            <div class="card fail-card">
                {metrics["heal_failed"]}
                <div class="card-label">
                    Heal Failed
                </div>
            </div>

        </div>

        <div style="
            text-align:center;
            font-size:22px;
            font-weight:bold;
            margin-top:20px;
            color:#28a745;
        ">
        Healing Success Rate :
        {metrics["success_rate"]}%
        </div>
        """

        print("\n===== LOCATOR QUALITY =====")

        print(
            "SMART:",
            smart_locators
        )

        print(
            "GENERIC:",
            generic_locators
        )

        print("==========================")
        locator_quality_html = f"""
        <h2>AI Locator Quality</h2>

        <div class="dashboard">

            <div class="total-card">
                <div class="card-value">
                    {smart_locators}
                </div>
                <div class="card-label">
                    Smart Locators
                </div>
            </div>

            <div class="fail-card">
                <div class="card-value">
                    {generic_locators}
                </div>
                <div class="card-label">
                    Generic Locators
                </div>
            </div>

        </div>
        """

        trend_html = f"""
        <h2>
        Execution Trend History
        </h2>

        <h3>
        Pass Rate Trend
        </h3>

        <img
        src="pass_rate_trend.png"
        style="
        width:900px;
        border:1px solid #ddd;
        border-radius:10px;
        margin-bottom:20px;
        ">

        <h3>
        Execution Time Trend
        </h3>

        <img
        src="execution_time_trend.png"
        style="
        width:900px;
        border:1px solid #ddd;
        border-radius:10px;
        ">
        """

        history_html = f"""
        <h2>
        Recent Execution History
        </h2>

        <table
        style="
        width:100%;
        border-collapse:collapse;
        margin-bottom:30px;
        ">

        <tr
        style="
        background:#2c3e50;
        color:white;
        font-weight:bold;
        ">

        <th>Run</th>

        <th>Date</th>

        <th>Pass Rate</th>
        <th>Failed</th>
        <th>Execution Time</th>

        <th>AI Generated</th>

        <th>Healed</th>

        </tr>

        {history_rows}

        </table>
        """

        chart_html = f"""
        <div style="
            text-align:center;
            margin-top:30px;
            margin-bottom:30px;
        ">

            <h2>
                Execution Statistics
            </h2>

            <img
                src="{chart_path}"
                width="350"
            >

        </div>
        """
        execution_chart_html = f"""
        <div style="
            text-align:center;
            margin-top:40px;
        ">

            <h2>
                Test Execution Time
            </h2>

            <img
                src="{execution_chart}"
                width="700"
            >

        </div>
        """
        module_chart_html = f"""
        <div style="
            text-align:center;
            margin-top:40px;
        ">

            <h2>
                Module Wise Pass Rate
            </h2>

            <img
                src="{module_chart}"
                width="700"
            >

        </div>
        """
        ai_locator_chart_html = f"""
        <div style="
            text-align:center;
            margin-top:40px;
        ">

            <h2>
                AI Locator Distribution
            </h2>

            <img
                src="{ai_locator_chart}"
                width="400"
            >

        </div>
        """

        html = f"""
        <html>

        <head>
            <meta charset="UTF-8">
            <title>
                AI Automation Report
            </title>

            <style>

                body {{
                    font-family: Arial;
                    margin: 30px;
                }}

                table {{
                    border-collapse: collapse;
                    width: 100%;
                }}

                th {{
                    background-color: #f2f2f2;
                }}

                th, td {{
                    border: 1px solid #ddd;
                    padding: 10px;
                    text-align: left;
                    vertical-align: top;
                }}

                .pass {{
                    color: green;
                    font-weight: bold;
                }}

                .fail {{
                    color: red;
                    font-weight: bold;
                }}

                .steps {{
                    font-size: 13px;
                    line-height: 1.6;
                }}
                
                pre {{
            white-space: pre-wrap;
            word-break: break-word;
            font-size: 12px;
            margin: 5px 0;
            
        }}

            img {{
        
            transition: 0.3s;
        
        }}
        
        img:hover {{
        
            transform: scale(1.05);
        
        }}
                    .dashboard {{
                display:flex;
                gap:20px;
                margin:20px 0;
            }}
            
            .card {{
                flex:1;
                padding:10px;
                border-radius:10px;
                color:white;
                text-align:center;
                font-size:20px;
                font-weight:bold;
                min-height:80px;
            }}
            
            .total-card {{
                background:#007bff;
            }}
            
            .pass-card {{
                background:#28a745;
            }}
            
            .fail-card {{
                background:#dc3545;
            }}
            
            .rate-card {{
                background:#fd7e14;
            }}
            
            .card-label {{
                font-size:16px;
                margin-top:10px;
            }}
            
                        .success {{
                background:#28a745;
            }}
            
            .danger {{
                background:#dc3545;
            }}
            
            .dashboard {{
                display: flex;
                gap: 20px;
                margin: 20px 0;
            }}
            
            .total-card,
            .pass-card,
            .fail-card,
            .rate-card {{
                flex: 1;
                min-width: 180px;
                text-align: center;
                padding: 20px;
                border-radius: 8px;
                color: white;
            }}
            
            .card-value {{
                font-size: 36px;
                font-weight: bold;
            }}
            
            .card-label {{
                font-size: 18px;
                margin-top: 10px;
            }}
            </style>

        </head>

        <body>

        <h1>
            AI Automation Execution Report
        </h1>
        {dashboard_html}
        {ai_dashboard_html}
        {ai_locator_chart_html} 
        {chart_html}
        {execution_chart_html}
        {module_chart_html}
        {trend_html}
        {history_html}
        {failure_html}
        {locator_quality_html}
        <h3>
            Started : {self.start_time}
        </h3>

        <h3>
            Finished : {end_time}
        </h3>

        <hr>

        <h2>
        Execution Information
        </h2>
        
        <table style="width:50%; margin-bottom:20px;">
        
        <tr>
            <td><b>Framework</b></td>
            <td>{self.framework}</td>
        </tr>
        
        <tr>
            <td><b>Browser</b></td>
            <td>{self.browser}</td>
        </tr>
        
        <tr>
            <td><b>Environment</b></td>
            <td>{self.environment}</td>
        </tr>
        
        <tr>
            <td><b>Execution Mode</b></td>
            <td>{self.execution_mode}</td>
        </tr>
        
        </table>
        
        <hr>

        <table>

            <tr>

                <th>ID</th>

                <th>Scenario</th>

                <th>Status</th>

                <th>Duration (sec)</th>

                <th>Error</th>

                <th>Execution Steps</th>
                
                <th>Locators Used</th>
                <th>Healing History</th>
                <th style="width:300px;">
                    Screenshot
                </th>

            </tr>
        """

        for result in self.results:
            print("\n================================")

            print(
                "REPORT HEALING HISTORY:"
            )

            print(
                result.get(
                    "healing_history",
                    []
                )
            )

            print("================================")
            css = (
                "pass"
                if result["status"] == "PASSED"
                else "fail"
            )

            # ======================================
            # EXECUTION STEPS
            # ======================================

            steps_html = "<br>".join([

                f"STEP {step['step']} : "
                f"{step['action'].upper()} "
                f"→ {step['element']} "
                f"({step['status']}) "
                f"[{step.get('duration', 0)} sec]"

                for step in result["steps"]

            ])

            # ======================================
            # LOCATOR HISTORY
            # ======================================

            locator_html = "".join([

                f"""
                <div style="
                    margin-bottom:15px;
                    padding:8px;
                    border-bottom:1px solid #ddd;
                ">

                <b>Element:</b>
                {item['element']}

                <br><br>

                <b>Locator:</b>

                <pre style="
                    background:#f8f8f8;
                    padding:8px;
                    border-radius:4px;
                    overflow:auto;
                ">
        {item['locator']}
                </pre>

                </div>
                """

                for item in result["locator_history"]

            ])
            healing_html = "".join([

                f"""
                <div style="
                    margin-bottom:12px;
                    padding:8px;
                    border-bottom:1px solid #ddd;
                ">

                <b>Element:</b>
                {h.get('element', '-')}

                <br><br>

                <b>Locator:</b>

                <pre style="
                    background:#f8f8f8;
                    padding:8px;
                    border-radius:4px;
                ">
            {h.get('healed_locator', '-')}
                </pre>

                <span style="
                    color:green;
                    font-weight:bold;
                ">
                    {h.get('status', '-')}
                </span>

                </div>
                """

                for h in result.get(
                    "healing_history",
                    []
                )

            ])
            # ======================================
            # COLLAPSIBLE ERROR
            # ======================================

            error_html = "-"

            if result["error"]:
                short_error = (
                    result["error"]
                    .replace("\n", " ")
                    [:120]
                )

                error_html = f"""
                <details>

                    <summary style="
                        color:red;
                        cursor:pointer;
                        font-weight:bold;
                    ">
                        {short_error}...
                    </summary>

                    <pre style="
                        max-height:300px;
                        overflow:auto;
                        background:#f8f8f8;
                        padding:10px;
                        border:1px solid #ddd;
                    ">
        {result["error"]}
                    </pre>

                </details>
                """

            # ======================================
            # SCREENSHOT
            # ======================================

            if result["screenshot"]:

                screenshot_html = f"""

                <a href="{result['screenshot']}"
                   target="_blank">

                    <img
                        src="{result['screenshot']}"
                        width="250"
                        style="
                            border:1px solid #ccc;
                            border-radius:5px;
                        "
                    >

                    <br>

                    View Full Screenshot

                </a>

                """

            else:

                screenshot_html = "-"

            # ======================================
            # TABLE ROW
            # ======================================

            html += f"""

            <tr>

                <td>
                    {result['id']}
                </td>

                <td>
                    {result['scenario']}
                </td>

                <td class="{css}">
                    {result['status']}
                </td>

                <td>
                    {result['duration']}
                </td>

                <td>
                    {error_html}
                </td>

                <td class="steps">
                    {steps_html}
                </td>

                <td>
                    {locator_html}
                </td>
                <td>
                    {healing_html}
                </td>
                <td>
                    {screenshot_html}
                </td>
                
            </tr>

            """

        html += """

        </table>

        </body>

        </html>

        """

        os.makedirs(
            "reports",
            exist_ok=True
        )

        report_path = (
            "reports/ai_execution_report.html"
        )

        with open(
                report_path,
                "w",
                encoding="utf-8"
        ) as file:

            file.write(html)

        print(
            f"\nHTML Report Generated:"
            f"\n{report_path}"
        )

        PDFReportGenerator.generate(
            self.results,
            report_path
        )