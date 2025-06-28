# shared/crud_targeting.py

from sqlalchemy.orm import Session
from shared import models, schemas


def get_targeting_for_campaign(db: Session, campaign_id: int) -> list[schemas.TargetingRule]:
    targeting_entries = db.query(models.TargetingRule).filter_by(campaign_id=campaign_id).all()
    return [schemas.TargetingRule.from_orm(entry) for entry in targeting_entries]


def add_targeting_rule(db: Session, rule: schemas.TargetingRuleCreate) -> schemas.TargetingRule:
    db_rule = models.TargetingRule(
        campaign_id=rule.campaign_id,
        targeting_type=rule.targeting_type,
        targeting_value=rule.targeting_value
    )
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return schemas.TargetingRule.from_orm(db_rule)


def delete_targeting_rule(db: Session, rule_id: int) -> None:
    rule = db.query(models.TargetingRule).filter_by(id=rule_id).first()
    if rule:
        db.delete(rule)
        db.commit()
