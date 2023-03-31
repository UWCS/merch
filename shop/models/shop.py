import logging
import os
from collections import Counter, defaultdict
from datetime import datetime
from typing import Callable, Optional, Union

import sqlalchemy as sa
from sqlalchemy import ForeignKey, ForeignKeyConstraint, func
from sqlalchemy.orm import relationship

from shop.models import utils
from shop.models.alert import Alert
from shop.models.item import Item
from shop.models.submission import Submission
from shop.models.team import Team
from shop.models.utils import Status, Visibility, auto_str

from ..database import Base, db


@auto_str
class Shop(Base):
    __tablename__ = "shops"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    start_time = sa.Column(sa.DateTime, default=func.current_timestamp())
    visibility = sa.Column(
        sa.Enum(Visibility),
        nullable=False,
        default=Visibility.OPEN,
        server_default="OPEN",
    )
    end_time = sa.Column(sa.DateTime)

    __table_args__ = (sa.UniqueConstraint("name", name="unq_shops_name"),)

    items = relationship(Item, back_populates="shop", order_by=Item.name)
    alerts_r = relationship(Alert, back_populates="shop", order_by=Alert.start_time)

    @property
    def alerts(self) -> list[Alert]:
        return [a for a in self.alerts_r if a.visible]

    @property
    def visible(self) -> Visibility:
        return self.visibility

    @property
    def open(self) -> bool:
        return self.visible == Visibility.OPEN

    def get_timestamp_str(self, time) -> str:
        return utils.time_str(time, datetime.now())

    @property
    def time_str(self) -> str:
        return utils.format_time_range(self.start_time, self.end_time, datetime.now())

    @property
    def category(self) -> str:
        now = datetime.now()
        if self.start_time and now < self.start_time:
            return "Upcoming"
        elif self.end_time and self.end_time < now:
            return "Archived"
        elif self.start_time and self.end_time:
            # If both exist, must be betweeen
            return "Active"
        else:
            return "Unknown"

    def get_item(self, name, visibility=Visibility.CLOSED) -> Optional[Item]:
        items = (
            db.session.query(Item)
            .where(Item.progcomp == self)
            .where(Item.name == name)
            .all()
        )
        return next((p for p in items if p.visible >= visibility), None)

    @property
    def visible_items(self) -> list[Item]:
        items = (
            db.session.query(Item)
            .where(Item.progcomp == self)
            .order_by(Item.name)
            .all()
        )
        return [p for p in items if p.visible]
