import glob
import logging
import os
import re
from datetime import datetime
from typing import Union

from flask import (Blueprint, jsonify, redirect, render_template, request,
                   send_from_directory, session, url_for)
from werkzeug.utils import secure_filename
from werkzeug.wrappers.response import Response

FlaskResponse = Union[Response, str]

from .database import db
from .models import *
# from .adapters import GameUIAdapter
from .session import SHOP_SESSION_KEY, USERNAME_SESSION_KEY


def get_shop() -> Shop:
    name = session.get(SHOP_SESSION_KEY)
    if name is None:
        return db.session.query(Shop).first()
    else:
        return db.session.query(Shop).where(Shop.name == name).first()


bp = Blueprint("shop", __name__)


@bp.route("/")
def menu() -> FlaskResponse:
    shop = get_shop()
    return render_template("menu.html", shop=shop, items=shop.items)


@bp.route("/item/<string:name>", methods=["GET"])
def item(name: str) -> FlaskResponse:
    """
    Retrieve the page for a problem
    """
    shop = get_shop()
    item = shop.get_item(item)
    if not item or not item.visible:
        return redirect(url_for("shop.submissions"))

    return render_template("item.html", item=item, shop=shop)


@bp.route("/poll", methods=["GET"])
def poll() -> FlaskResponse:
    shop = get_shop()

    data = {"end_time": shop.end_time.timestamp() if shop.end_time else 0}
    return jsonify(data)
