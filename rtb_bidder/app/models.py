from pydantic import BaseModel
from typing import Optional

from pydantic import BaseModel
from typing import Optional

class BidRequest(BaseModel):
    request_id: str
    imp_id: str
    site_domain: str
    site_page: Optional[str]
    user_country: Optional[str]
    user_language: Optional[str]
    device_type: Optional[str]
    banner_width: int
    banner_height: int
    floor_price: float

class BidResponse(BaseModel):
    request_id: str
    imp_id: str
    price: float
    ad_id: int
    campaign_id: int
    creative_url: str
    click_url: str
