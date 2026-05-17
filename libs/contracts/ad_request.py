from typing import Optional

from pydantic import BaseModel, Field

class AdDecisionRequest(BaseModel):
    viewer_id: str = Field(..., description="Unique viewer identifier")
    session_id: str = Field(..., description="Current playback session identifier")
    content_id: str = Field(..., description="OTT or live sports content identifier")
    placement_id: str = Field(..., description="Ad placement identifier")
    ad_break_id: str = Field(..., description="Ad break identifier")
    device: str = Field(..., description="Device type such as ctv, mobile, or web")
    geo: str = Field(..., description="Viewer geography or region")
    user_agent: Optional[str] = Field(None, description="Optional user agent string")