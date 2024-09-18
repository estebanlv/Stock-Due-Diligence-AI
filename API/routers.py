from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from business_analyst import get_business_dd
from technical_analyst import get_technical_dd
from hf_manager import get_hf_due_diligence
import json

router = APIRouter()

class DueDiligenceResponse(BaseModel):
    DD: dict

@router.post("/due_diligence/{ticker}", response_model=DueDiligenceResponse)
async def get_due_diligence(ticker: str):
    """
    Generate and return a due diligence report for the given stock ticker.
    """
    try:
        business_dd_report = get_business_dd(ticker)
        technical_dd_report = get_technical_dd(ticker)
        final_dd = get_hf_due_diligence(ticker, business_dd_report, technical_dd_report)
        final_dd_dict = json.loads(final_dd)
        return DueDiligenceResponse(DD=final_dd_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating due diligence: {str(e)}")
