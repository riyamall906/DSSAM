
def calculate_assessment_score(test_results):
    """Calculate the percentage of test cases passed."""

    total_tests = len(test_results)

    if total_tests == 0:
        return 0

    passed_tests = sum(
        1 for result in test_results
        if result.get("passed") is True
    )

    return round((passed_tests / total_tests) * 100, 2)


def calculate_skill_mastery(question_results):
    """Calculate difficulty-weighted mastery for each skill and topic."""

    difficulty_weights = {
        "Easy": 1,
        "Medium": 2,
        "Hard": 3
    }

    skill_scores = {}

    for result in question_results:
        key = f"{result['skill']} - {result['topic']}"

        weight = difficulty_weights.get(
            result["difficulty"], 1
        )

        score = result["score"]

        if key not in skill_scores:
            skill_scores[key] = {
                "weighted_score": 0,
                "total_weight": 0
            }

        skill_scores[key]["weighted_score"] += score * weight
        skill_scores[key]["total_weight"] += weight

    mastery = {}

    for skill, values in skill_scores.items():
        mastery[skill] = round(
            values["weighted_score"] / values["total_weight"],
            2
        )

    return mastery
