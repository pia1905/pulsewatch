from fastapi import APIRouter, HTTPException

from services.market_data import get_market_data


router = APIRouter(
    prefix="/api/market",
    tags=["Market"]
)


@router.get("/{symbol}")
def get_market(symbol: str):
    """
    Get the latest market information.
    """

    data = get_market_data(symbol)

    if data is None:
        raise HTTPException(
            status_code=404,
            detail=f"Market data unavailable for '{symbol.upper()}'"
        )

    return data