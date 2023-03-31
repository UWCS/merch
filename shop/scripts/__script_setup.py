import os
import sys

import flask_migrate

parent = os.path.abspath(".")
sys.path.insert(1, parent)

from shop import app
from shop.database import db
from shop.models import *

_script_shop: str = None


def script_shop():
    global _script_shop
    if _script_shop is None:
        _script_shop = os.environ["SCRIPT_SHOP"]
        print("Current editing Shop:", _script_shop)
    return _script_shop
