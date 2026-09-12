from typing import Optional

from fastapi import (
    APIRouter,
    HTTPException,
    Query
)

from backend.services.tree_service import (
    get_tree_details,
    get_all_trees,
    recommend_trees
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/trees",
    tags=["Tree Recommendation"]
)


# ============================================================
# STATUS
# ============================================================

@router.get("/status")
def tree_status():

    return {
        "status": "Tree Recommendation is working"
    }


# ============================================================
# ALL TREES
# ============================================================

@router.get("")
def all_trees():

    return get_all_trees()


# ============================================================
# TREE DETAILS
# ============================================================

@router.get("/details/{tree_name}")
def tree_details(
    tree_name: str
):

    result = get_tree_details(
        tree_name
    )

    if not result["success"]:

        raise HTTPException(
            status_code=404,
            detail=result["message"]
        )

    return result


# ============================================================
# TREE RECOMMENDATION
# ============================================================

@router.get("/recommend")
def tree_recommendation(

    soil: Optional[str] = Query(
        default="",
        description="Soil type"
    ),

    climate: Optional[str] = Query(
        default="",
        description="Climate condition"
    ),

    water: Optional[str] = Query(
        default="",
        description="Water availability"
    ),

    category: Optional[str] = Query(
        default="",
        description="Tree category"
    )
):

    result = recommend_trees(

        soil=soil or "",

        climate=climate or "",

        water=water or "",

        category=category or ""
    )


    # --------------------------------------------------------
    # Invalid request
    # --------------------------------------------------------

    if not result["success"]:

        raise HTTPException(
            status_code=400,
            detail=result["message"]
        )


    return result