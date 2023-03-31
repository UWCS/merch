import logging
import os
from collections import Counter, defaultdict
from datetime import datetime
from typing import Callable, Optional, Union

import sqlalchemy as sa
from sqlalchemy import ForeignKey, ForeignKeyConstraint, func
from sqlalchemy.orm import relationship

from shop.models.utils import auto_str

from ..database import Base, db


@auto_str
class Alert(Base):
    __tablename__ = "alerts"

    id = sa.Column(sa.Integer, primary_key=True)
    shop_id = sa.Column(sa.Integer, ForeignKey("shops.id"))
    name = sa.Column(sa.String)
    title = sa.Column(sa.String)
    text = sa.Column(sa.String)
    start_time = sa.Column(sa.DateTime, default=func.current_timestamp())
    end_time = sa.Column(sa.DateTime)

    __table_args__ = (sa.UniqueConstraint("name", "shop_id", name="unq_alerts_name"),)

    shop = relationship("Shop", back_populates="alerts_r")

    @property
    def visible(self) -> bool:
        now = datetime.now()
        return self.start_time < now and (not self.end_time or now < self.end_time)
