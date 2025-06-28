 # shared/models.py
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
    targeting_rules = relationship("TargetingRule", back_populates="campaign")

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

class TargetingRule(Base):
    __tablename__ = "campaign_targeting"

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"))
    targeting_type = Column(String(50), nullable=False)
    targeting_value = Column(Text, nullable=False)

    campaign = relationship("Campaign", back_populates="targeting_rules")

class BidRequest(Base):
    __tablename__ = "bid_requests"

    id = Column(Integer, primary_key=True)
    request_id = Column(String(100), unique=True, nullable=False)
    imp_id = Column(String(100), nullable=False)
    auction_id = Column(String(100))
    site_domain = Column(String(255))
    site_page = Column(Text)
    user_country = Column(String(10))
    user_language = Column(String(10))
    device_type = Column(String(20))
    banner_width = Column(Integer)
    banner_height = Column(Integer)
    floor_price = Column(DECIMAL(6, 4))
    timestamp = Column(DateTime, default=datetime.utcnow)
    processed = Column(String(5), default="false")  # or use Boolean if needed


class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True)
    bid_request_id = Column(Integer, ForeignKey("bid_requests.id"))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    creative_id = Column(Integer, ForeignKey("creatives.id"))
    bid_price = Column(DECIMAL(6, 4), nullable=False)
    won = Column(String(5), default="false")  # or use Boolean
    win_price = Column(DECIMAL(6, 4))
    timestamp = Column(DateTime, default=datetime.utcnow)


class Impression(Base):
    __tablename__ = "impressions"

    id = Column(Integer, primary_key=True)
    bid_id = Column(Integer, ForeignKey("bids.id"))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    creative_id = Column(Integer, ForeignKey("creatives.id"))
    cost = Column(DECIMAL(6, 4))
    timestamp = Column(DateTime, default=datetime.utcnow)


class Click(Base):
    __tablename__ = "clicks"

    id = Column(Integer, primary_key=True)
    impression_id = Column(Integer, ForeignKey("impressions.id"))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    creative_id = Column(Integer, ForeignKey("creatives.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
