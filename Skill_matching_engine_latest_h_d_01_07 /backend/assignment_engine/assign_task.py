from typing import List, Dict


class AssignmentDecisionEngine:

    def __init__(self):
        self.MIN_SKILL_MATCH = 70
        self.MAX_ACTIVE_TASKS = 5

    def assign_employee(self, task: Dict, candidates: List[Dict]):

        eligible_candidates = []

        for emp in candidates:

            # -------------------------
            # Business Rule 1: Employee on Leave
            # -------------------------
            if emp.get("on_leave", False):
                continue

            # -------------------------
            # Business Rule 2: Check Available Hours
            # -------------------------
            if emp["available_hours"] < task["estimated_hours"]:
                continue

            # -------------------------
            # Business Rule 3: Maximum Active Tasks
            # -------------------------
            if emp["active_tasks"] >= self.MAX_ACTIVE_TASKS:
                continue

            # -------------------------
            # Business Rule 4: Minimum Skill Match
            # -------------------------
            if emp["skill_match"] < self.MIN_SKILL_MATCH:
                continue

            # -------------------------
            # Calculate Final Decision Score
            # -------------------------
            decision_score = (
                emp["skill_match"] * 0.70 +
                emp["resource_score"] * 0.30
            )

            emp["decision_score"] = round(decision_score, 2)

            eligible_candidates.append(emp)

        # -------------------------
        # No Eligible Employee
        # -------------------------
        if len(eligible_candidates) == 0:
            return {
                "status": "No Employee Found"
            }

        # -------------------------
        # Sort by Decision Score
        # -------------------------
        eligible_candidates.sort(
            key=lambda x: x["decision_score"],
            reverse=True
        )

        # -------------------------
        # Select Assigned Employee
        # -------------------------
        assigned_employee = eligible_candidates[0]

        # -------------------------
        # Select Backup Employee
        # -------------------------
        backup_employee = (
            eligible_candidates[1]
            if len(eligible_candidates) > 1
            else None
        )

        # -------------------------
        # Return Final Result
        # -------------------------
        return {
            "status": "Assigned",
            "assigned_employee": assigned_employee,
            "backup_employee": backup_employee,
            "all_rankings": eligible_candidates
        }