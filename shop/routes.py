import glob
import logging
import os
import re
from datetime import datetime
from typing import Union

import yaml
from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from werkzeug.utils import secure_filename
from werkzeug.wrappers.response import Response

import shop.yamlparse
from shop.shop import Category, Item, Shop

FlaskResponse = Union[Response, str]

_shop: Shop = None
content_path = "shop/content.yaml"
last_edit = 0


def get_shop() -> Shop:
    global _shop
    global last_edit
    mtime = os.path.getmtime(content_path)
    if mtime > last_edit or _shop is None:
        f = open(content_path)
        raw = yaml.safe_load(f)

        _shop = shop.yamlparse.parse_dict_to_dataclasses(raw["shop"], Shop)
        last_edit = mtime
    return _shop


bp = Blueprint("shop", __name__)


@bp.route("/")
def menu() -> FlaskResponse:
    shop = get_shop()
    return render_template("menu.html", shop=shop)


# @bp.route("/item/<string:name>", methods=["GET"])
# def item(name: str) -> FlaskResponse:
#     """
#     Retrieve the page for a problem
#     """
#     shop = get_shop()
#     item = shop.get_item(item)
#     if not item or not item.visible:
#         return redirect(url_for("shop.submissions"))

#     return render_template("item.html", item=item, shop=shop)


# @bp.route("/poll", methods=["GET"])
# def poll() -> FlaskResponse:
#     shop = get_shop()

#     data = {"end_time": shop.end_time.timestamp() if shop.end_time else 0}
#     return jsonify(data)
