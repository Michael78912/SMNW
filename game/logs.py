"""logs the current running process of SMNW."""

import logging

def init():
    logging.basicConfig(level=logging.DEBUG,
                    filename="SMNW.log",
                    filemode="w",
                    format="%(name)s:%(asctime)s -- %(levelname)s -- %(message)s"
                    )
