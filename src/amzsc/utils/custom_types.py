from typing import Union

from selenium.webdriver import Chrome, Remote


class CustomTypes:
    DRIVER_TYPE = Union[Chrome, Remote]
