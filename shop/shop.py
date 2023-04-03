from dataclasses import dataclass

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

    @property
    def desc_md(self):
        return markdown(self.desc)


@dataclass
class Shop:
    intro: str
    categories: list[Category]
    alerts: list[Alert]

    @property
    def intro_md(self):
        return markdown(self.intro)
