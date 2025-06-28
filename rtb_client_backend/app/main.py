
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from fastapi import FastAPI, Depends, Request, HTTPException
from shared.auth import verify_session
from shared.database import get_db
from shared import crud_campaign, schemas
from shared import auth


app = FastAPI()

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


@app.post("/login")
def login(payload: schemas.LoginPayload):
    if not auth.validate_credentials(payload.username, payload.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return auth.create_session_cookie_for_user(payload.username)