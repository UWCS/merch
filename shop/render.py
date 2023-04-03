import os
import shutil
import sys
from pipes import Template

import markdown
import yaml
import yamlparse
from jinja2 import Environment, FileSystemLoader, Template

import shop
from shop import Shop

rendered_content = dict()

env = Environment(
    loader=FileSystemLoader("templates"),
)
jinja_template = env.get_template("menu.html")

f = open("content.yaml", encoding="utf8")
raw = yaml.safe_load(f)

rendered_content["shop"] = yamlparse.parse_dict_to_dataclasses(raw["shop"], Shop)
print(rendered_content["shop"])

if os.path.exists("build"):
    shutil.rmtree("build")
os.makedirs("build")

with open(os.path.join("build", "index.html"), mode="w", encoding="utf8") as out_file:
    # Recursive render
    content = jinja_template.render(**rendered_content)
    while True:
        new_content = Template(content).render(**rendered_content)
        if new_content == content:
            break
        content = new_content

    out_file.write(content)

shutil.copytree("static", os.path.join("build", "static"))
