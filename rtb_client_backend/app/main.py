# rtb_client_backend/app/main.py

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from shared.auth import verify_session
from shared.database import get_db
from shared import crud_campaign, crud_targeting, schemas
from shared import auth

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/campaigns", response_model=list[schemas.Campaign])
def read_campaigns(request: Request, db=Depends(get_db), _=Depends(verify_session)):
    return crud_campaign.get_campaigns(db)

@app.post("/campaigns", response_model=schemas.Campaign)
def add_campaign(campaign: schemas.CampaignCreate, request: Request, db=Depends(get_db), _=Depends(verify_session)):
    return crud_campaign.create_campaign(db, campaign)

@app.put("/campaigns/{campaign_id}", response_model=schemas.Campaign)
def update_campaign(
    campaign_id: int,
    campaign: schemas.CampaignCreate,
    request: Request,
    db=Depends(get_db),
    _=Depends(verify_session)
):
    return crud_campaign.update_campaign(db, campaign_id, campaign)

@app.get("/campaigns/{campaign_id}/targeting", response_model=list[schemas.TargetingRule])
def get_targeting_rules(campaign_id: int, request: Request, db=Depends(get_db), _=Depends(verify_session)):
    return crud_targeting.get_targeting_rules(db, campaign_id)

@app.post("/campaigns/{campaign_id}/targeting", response_model=schemas.TargetingRule)
def add_targeting_rule(campaign_id: int, rule: schemas.TargetingRuleCreate, request: Request, db=Depends(get_db), _=Depends(verify_session)):
    return crud_targeting.add_targeting_rule(db, campaign_id, rule)

@app.delete("/targeting/{rule_id}")
def delete_targeting_rule(rule_id: int, request: Request, db=Depends(get_db), _=Depends(verify_session)):
    crud_targeting.delete_targeting_rule(db, rule_id)
    return {"status": "deleted"}

@app.post("/login")
def login(payload: schemas.LoginPayload):
    if not auth.validate_credentials(payload.username, payload.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return auth.create_session_cookie_for_user(payload.username)
