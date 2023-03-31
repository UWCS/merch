import os
import typing
from typing import Optional

import sqlalchemy as sa
from sqlalchemy import ForeignKey, ForeignKeyConstraint, UniqueConstraint, func
from sqlalchemy.orm import relationship

from shop.models.utils import Status, Visibility, auto_str

if typing.TYPE_CHECKING:
    from shop.models.submission import *

from ..database import Base, db


@auto_str
class Item(Base):
    __tablename__ = "problems"

    id = sa.Column(sa.Integer, primary_key=True)
    shop_id = sa.Column(sa.Integer, ForeignKey("shops.id"))
    visibility = sa.Column(
        sa.Enum(Visibility),
        nullable=False,
        default=Visibility.OPEN,
        server_default="OPEN",
    )
    name = sa.Column(sa.String)
    url = sa.Column(sa.String)
    description = sa.Column(sa.String)
    image_url = sa.Column(sa.String)
    __table_args__ = (sa.UniqueConstraint("name", "shop_id", name="unq_problems_name"),)

    shop = relationship("Shop", back_populates="items")

    @property
    def visible(self) -> Visibility:
        return min(self.visibility, self.shop.visible)

    @property
    def open(self) -> bool:
        return self.visible == Visibility.OPEN
