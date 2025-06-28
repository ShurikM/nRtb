from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException


def get_campaigns(db: Session):
    return db.query(models.Campaign).all()

def create_campaign(db: Session, campaign: schemas.CampaignCreate):
    db_campaign = models.Campaign(**campaign.dict())
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

def update_campaign(db: Session, campaign_id: int, campaign_data: schemas.CampaignCreate):
    db_campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    for field, value in campaign_data.dict().items():
        setattr(db_campaign, field, value)

    db.commit()
    db.refresh(db_campaign)
    return db_campaign

