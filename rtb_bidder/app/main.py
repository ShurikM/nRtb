from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from shared.database import SessionLocal
from shared import models
from rtb_bidder.app import bidder_logic
import uvicorn
from models import BidRequest

app = FastAPI(title="RTB Bidder API", version="1.0")



@app.post("/bid")
def get_bid(request: BidRequest):
    db = SessionLocal()
    try:
        bid_response = bidder_logic.process_bid_request(db, request)
        if bid_response is None:
            return {"no_bid": True}
        return bid_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

if __name__ == "__main__":
    uvicorn.run("rtb_bidder.app.main:app", host="0.0.0.0", port=8080, reload=True)
