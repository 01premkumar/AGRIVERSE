import json
from pathlib import Path
from typing import Any


# ============================================================
# DATABASE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_PATH = (
    BASE_DIR
    / "knowledge_base"
    / "trees"
    / "tree_database.json"
)


# ============================================================
# LOAD DATABASE
# ============================================================

def load_tree_database() -> dict[str, Any]:

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Tree database not found: {DATABASE_PATH}"
        )

    try:
        with open(
            DATABASE_PATH,
            "r",
            encoding="utf-8"
        ) as file:
            database = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid tree database JSON: {error}"
        )

    if not isinstance(database, dict):
        raise ValueError(
            "Tree database must contain a JSON object."
        )

    return database


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(value: Any) -> str:

    if value is None:
        return ""

    return " ".join(
        str(value).strip().lower().split()
    )


# ============================================================
# MATCH TEXT
# ============================================================

def text_matches(
    search_text: str,
    values: Any
) -> bool:

    search = normalize_text(search_text)

    if not search:
        return False

    if isinstance(values, list):

        for item in values:

            value = normalize_text(item)

            if (
                search in value
                or value in search
            ):
                return True

        return False

    value = normalize_text(values)

    return (
        search in value
        or value in search
    )


# ============================================================
# GET TREE DETAILS
# ============================================================

def get_tree_details(
    tree_name: str
):

    database = load_tree_database()

    tree_key = normalize_text(tree_name)

    if not tree_key:

        return {
            "success": False,
            "tree": tree_name,
            "message": "Tree name is required."
        }


    # --------------------------------------------------------
    # Find tree
    # --------------------------------------------------------

    matched_name = None
    tree_data = None

    for name, data in database.items():

        if normalize_text(name) == tree_key:

            matched_name = name
            tree_data = data
            break


    # --------------------------------------------------------
    # Tree not found
    # --------------------------------------------------------

    if matched_name is None:

        return {
            "success": False,
            "tree": tree_name,
            "message": (
                "Tree information is not "
                "available yet."
            )
        }


    # --------------------------------------------------------
    # Validate data
    # --------------------------------------------------------

    if not isinstance(tree_data, dict):

        return {
            "success": False,
            "tree": matched_name,
            "message": (
                "Invalid tree information "
                "for this tree."
            )
        }


    # --------------------------------------------------------
    # Return details
    # --------------------------------------------------------

    return {
        "success": True,
        "tree": matched_name,
        "category": tree_data.get(
            "category",
            ""
        ),
        "soil": tree_data.get(
            "soil",
            []
        ),
        "climate": tree_data.get(
            "climate",
            []
        ),
        "water_requirement": tree_data.get(
            "water_requirement",
            ""
        ),
        "uses": tree_data.get(
            "uses",
            []
        ),
        "guidance": tree_data.get(
            "guidance",
            []
        )
    }


# ============================================================
# GET ALL TREES
# ============================================================

def get_all_trees():

    database = load_tree_database()

    trees = []

    for name, data in database.items():

        if not isinstance(data, dict):
            continue

        trees.append({
            "tree": name,
            "category": data.get(
                "category",
                ""
            ),
            "water_requirement": data.get(
                "water_requirement",
                ""
            ),
            "uses": data.get(
                "uses",
                []
            )
        })


    return {
        "success": True,
        "count": len(trees),
        "trees": trees
    }


# ============================================================
# RECOMMEND TREES
# ============================================================

def recommend_trees(
    soil: str = "",
    climate: str = "",
    water: str = "",
    category: str = ""
):

    database = load_tree_database()

    soil_text = normalize_text(soil)
    climate_text = normalize_text(climate)
    water_text = normalize_text(water)
    category_text = normalize_text(category)


    # --------------------------------------------------------
    # Check filters
    # --------------------------------------------------------

    filters_provided = any([
        soil_text,
        climate_text,
        water_text,
        category_text
    ])

    if not filters_provided:

        return {
            "success": False,
            "count": 0,
            "recommendations": [],
            "message": (
                "Please provide at least one "
                "recommendation criterion: "
                "soil, climate, water or category."
            )
        }


    recommendations = []


    # --------------------------------------------------------
    # Process each tree
    # --------------------------------------------------------

    for name, data in database.items():

        if not isinstance(data, dict):
            continue

        score = 0
        matched_criteria = []


        # ----------------------------------------------------
        # SOIL MATCH
        # ----------------------------------------------------

        tree_soils = data.get(
            "soil",
            []
        )

        if soil_text and text_matches(
            soil_text,
            tree_soils
        ):

            score += 2
            matched_criteria.append(
                "soil"
            )


        # ----------------------------------------------------
        # CLIMATE MATCH
        # ----------------------------------------------------

        tree_climates = data.get(
            "climate",
            []
        )

        if climate_text and text_matches(
            climate_text,
            tree_climates
        ):

            score += 2
            matched_criteria.append(
                "climate"
            )


        # ----------------------------------------------------
        # WATER MATCH
        # ----------------------------------------------------

        tree_water = data.get(
            "water_requirement",
            ""
        )

        if water_text and text_matches(
            water_text,
            tree_water
        ):

            score += 2
            matched_criteria.append(
                "water"
            )


        # ----------------------------------------------------
        # CATEGORY MATCH
        # ----------------------------------------------------

        tree_category = data.get(
            "category",
            ""
        )

        if category_text and text_matches(
            category_text,
            tree_category
        ):

            score += 3
            matched_criteria.append(
                "category"
            )


        # ----------------------------------------------------
        # ADD MATCHED TREE
        # ----------------------------------------------------

        if score > 0:

            recommendations.append({

                "tree": name,

                "category": data.get(
                    "category",
                    ""
                ),

                "score": score,

                "matched_criteria":
                    matched_criteria,

                "water_requirement":
                    data.get(
                        "water_requirement",
                        ""
                    ),

                "soil":
                    data.get(
                        "soil",
                        []
                    ),

                "climate":
                    data.get(
                        "climate",
                        []
                    ),

                "uses":
                    data.get(
                        "uses",
                        []
                    ),

                "guidance":
                    data.get(
                        "guidance",
                        []
                    )
            })


    # --------------------------------------------------------
    # SORT BY SCORE
    # --------------------------------------------------------

    recommendations.sort(
        key=lambda item: (
            -item["score"],
            item["tree"].lower()
        )
    )


    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    return {
        "success": True,
        "count": len(
            recommendations
        ),
        "recommendations":
            recommendations
    }