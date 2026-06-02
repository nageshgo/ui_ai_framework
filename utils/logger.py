
import logging
import os

# os.makedirs("reports", exist_ok=True)
#
# logging.basicConfig(
#     filename="reports/framework.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )
#
# logger = logging.getLogger()
#
# import logging
# import os


class FrameworkLogger:

    @staticmethod
    def get_logger(name, file_name):

        os.makedirs(
            "logs",
            exist_ok=True
        )

        logger = logging.getLogger(name)

        if not logger.handlers:

            logger.setLevel(
                logging.INFO
            )

            handler = logging.FileHandler(
                f"logs/{file_name}"
            )

            formatter = logging.Formatter(

                "%(asctime)s | "
                "%(levelname)s | "
                "%(message)s"
            )

            handler.setFormatter(
                formatter
            )

            logger.addHandler(
                handler
            )

        return logger