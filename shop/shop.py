from dataclasses import dataclass
from datetime import datetime

from markdown import markdown


@dataclass
class Item:
    title: str
    desc: str
    images: list[str]
    buy: str
    price: str

    @property
    def desc_md(self):
        return markdown(self.desc)


@dataclass
class Category:
    name: str
    items: list[Item]


@dataclass
class Alert:
    title: str
    desc: str
    type: str = "success"
    start: str = 0
    end: str = "2030-01-01T00:00:00Z"

    @property
    def desc_md(self):
        return markdown(self.desc)


@dataclass
class Shop:
    start: str
    end: str
    intro: str
    categories: list[Category]
    alerts: list[Alert]

    @property
    def intro_md(self):
        return markdown(self.intro)
