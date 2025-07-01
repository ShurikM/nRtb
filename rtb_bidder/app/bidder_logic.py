import random
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session
from shared import models

from .models import BidRequest, BidResponse  # assuming local models.py
from shared import models as db_models
from shared.protos import events_pb2, events_pb2_grpc
import grpc


def is_campaign_active(campaign: models.Campaign, now: datetime) -> bool:
    return campaign.status == "active" and campaign.start_date <= now <= campaign.end_date


def has_budget(campaign: models.Campaign) -> bool:
    return campaign.budget_total > campaign.budget_spent


def match_targeting(rules: list[models.TargetingRule],
                    geo: Optional[str] = None,
                    domain: Optional[str] = None,
                    language: Optional[str] = None,
                    device: Optional[str] = None) -> bool:
    checks = {
        "geo": geo,
        "domain": domain,
        "language": language,
        "device": device
    }
    for rule in rules:
        values = eval(rule.targeting_value)
        match_val = checks.get(rule.targeting_type)
        if match_val is not None and match_val not in values:
            return False
    return True


def select_campaign(db: Session, geo: str, domain: str, language: str, device: str) -> Optional[models.Campaign]:
    now = datetime.utcnow()
    campaigns = db.query(models.Campaign).all()

    eligible = []
    for c in campaigns:
        if not is_campaign_active(c, now):
            continue
        if not has_budget(c):
            continue
        if not match_targeting(c.targeting_rules, geo, domain, language, device):
            continue
        eligible.append(c)

    if eligible:
        return random.choice(eligible)
    return None


def select_creative(campaign: models.Campaign, width: int, height: int) -> Optional[models.Creative]:
    for creative in campaign.creatives:
        if creative.width == width and creative.height == height:
            return creative
    return None




def process_bid_request(db: Session, request: BidRequest) -> Optional[BidResponse]:
    campaign = select_campaign(db, request.user_country, request.site_domain,
                                request.user_language, request.device_type)
    if not campaign or campaign.bid_price < request.floor_price:
        return None

    creative = select_creative(campaign, request.banner_width, request.banner_height)
    if not creative:
        return None

    # Optional: log the bid request using gRPC
    try:
        channel = grpc.insecure_channel("localhost:50052")
        stub = events_pb2_grpc.EventLoggerStub(channel)
        stub.LogBidRequest(events_pb2.BidRequest(
            request_id=request.request_id,
            imp_id=request.imp_id,
            auction_id="",  # not yet implemented
            site_domain=request.site_domain,
            site_page=request.site_page or "",
            user_country=request.user_country or "",
            user_language=request.user_language or "",
            device_type=request.device_type or "",
            banner_width=request.banner_width,
            banner_height=request.banner_height,
            floor_price=request.floor_price
        ))
    except Exception:
        pass  # for now, log errors silently

    return BidResponse(
        request_id=request.request_id,
        imp_id=request.imp_id,
        price=float(campaign.bid_price),
        ad_id=creative.id,
        campaign_id=campaign.id,
        creative_url=creative.banner_url,
        click_url=creative.click_url
    )
