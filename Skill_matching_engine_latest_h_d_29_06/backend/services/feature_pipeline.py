# feature_pipeline.py by drashti

from backend.services.data_cleaner import clean_skill_list
from backend.services.gemini_validator import validate_skills
from backend.services.employee_repository import (
    create_employee_profile,
    create_employee_skills,
    create_employee_features,
    create_employee_workload,
    get_employee_id
)

from backend.services.score_calculator import (
    calculate_technical_score,
    calculate_learning_score,
    calculate_adaptability_score
)


def process_employee(employee_data):

    print("TASK 4 PIPELINE STARTED")
    print("RAW DATA =", employee_data)

    # =====================================
    # STEP 1: MERGE ALL SKILLS
    # =====================================

    all_skills = (
        (employee_data.get("languages") or []) +
        (employee_data.get("frameworks") or []) +
        (employee_data.get("tools") or [])
    )

    # =====================================
    # STEP 2: CLEAN DATA
    # =====================================

    cleaned_skills = clean_skill_list(all_skills)

    print("CLEANED SKILLS =", cleaned_skills)

    # =====================================
    # STEP 3: GEMINI VALIDATION
    # =====================================

    validated = validate_skills(cleaned_skills)

    print("VALIDATION RESULT =", validated)

    languages = validated.get("languages", [])
    frameworks = validated.get("frameworks", [])
    tools = validated.get("tools", [])

    # =====================================
    # STEP 4: SAVE PROFILE
    # =====================================

    create_employee_profile({
    "emp_id": employee_data["emp_id"],
    "name": employee_data["name"],
    "email": employee_data["email"],
    "role": employee_data["role"],
    "experience": employee_data["experience"]
})

    employee_id = employee_data["emp_id"]

    # =====================================
    # STEP 5: SAVE SKILLS (FIXED)
    # =====================================

    def align(skills, ratings):
        skills = list(skills or [])
        ratings = list(ratings or [])
        min_len = min(len(skills), len(ratings))
        return skills[:min_len], ratings[:min_len]


    # Align all skill categories with ratings
    languages, lang_ratings = align(
        languages,
        employee_data.get("programming_ratings", [])
    )

    frameworks, fw_ratings = align(
        frameworks,
        employee_data.get("framework_ratings", [])
    )

    tools, tool_ratings = align(
        tools,
        employee_data.get("tools_and_ide_ratings", [])
    )

    print("FINAL LANG + RATINGS =", list(zip(languages, lang_ratings)))
    print("FINAL FW + RATINGS =", list(zip(frameworks, fw_ratings)))
    print("FINAL TOOLS + RATINGS =", list(zip(tools, tool_ratings)))

    create_employee_skills({
        "emp_id": employee_data["emp_id"],

        "programming_languages": languages,
        "programming_ratings": lang_ratings,

        "frameworks": frameworks,
        "framework_ratings": fw_ratings,

        "tools_and_ide": tools,
        "tools_and_ide_ratings": tool_ratings
    })

    # =====================================
    # STEP 6: CALCULATE SCORES
    # =====================================

    technical_score = calculate_technical_score(
        languages,
        frameworks,
        tools,
        employee_data["experience"]
    )

    learning_score = calculate_learning_score(
        languages,
        frameworks,
        tools
    )

    adaptability_score = calculate_adaptability_score(
        languages,
        frameworks,
        tools
    )

    execution_score = 50

    # =====================================
    # STEP 7: SAVE FEATURES
    # =====================================

    create_employee_features(
        emp_id=employee_id,
        technical_score=technical_score,
        learning_score=learning_score,
        adaptability_score=adaptability_score,
        execution_score=execution_score
    )

    # =====================================
    # STEP 8: CREATE DEFAULT WORKLOAD
    # =====================================

    create_employee_workload(employee_id)

    # =====================================
    # STEP 9: RETURN RESULT
    # =====================================

    return {
        "employee_id": employee_id,
        "languages": languages,
        "frameworks": frameworks,
        "tools": tools,
        "technical_score": technical_score,
        "learning_score": learning_score,
        "adaptability_score": adaptability_score,
        "execution_score": execution_score
    }