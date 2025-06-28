from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    advertiser_id = Column(String(100), nullable=False)
    status = Column(String(20), default="active")
    budget_total = Column(DECIMAL(10, 2), nullable=False)
    budget_daily = Column(DECIMAL(10, 2))
    budget_spent = Column(DECIMAL(10, 2), default=0)
    bid_price = Column(DECIMAL(6, 4), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    creatives = relationship("Creative", back_populates="campaign")

class Creative(Base):
    __tablename__ = "creatives"

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    banner_url = Column(Text, nullable=False)
    click_url = Column(Text, nullable=False)
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

    campaign = relationship("Campaign", back_populates="creatives")
