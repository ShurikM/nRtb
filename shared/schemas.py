# shared/schemas.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CreativeBase(BaseModel):
    name: str
    width: int
    height: int
    banner_url: str
    click_url: str
    status: Optional[str] = "active"


class CreativeCreate(CreativeBase):
    pass


class Creative(CreativeBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TargetingRuleBase(BaseModel):
    targeting_type: str
    targeting_value: str

class TargetingRuleCreate(TargetingRuleBase):
    campaign_id: int

class TargetingRule(TargetingRuleBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class CampaignBase(BaseModel):
    name: str
    advertiser_id: str
    status: Optional[str] = "active"
    budget_total: float
    budget_daily: Optional[float]
    bid_price: float
    start_date: datetime
    end_date: datetime


class CampaignCreate(CampaignBase):
    pass


class Campaign(CampaignBase):
    id: int
    budget_spent: float
    created_at: datetime
    updated_at: datetime
    creatives: List[Creative] = []
    targeting_rules: List[TargetingRule] = []

    model_config = {
        "from_attributes": True
    }


class LoginPayload(BaseModel):
    username: str
    password: str
