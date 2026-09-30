# =========================
# GPA Calculator
# =========================


def calculate_gpa(courses):
    """
    Calculate weighted GPA from a list of courses.

    Each course should contain:
    - grade
    - credits
    """

    if not courses:
        return 0

    total_points = 0
    total_credits = 0

    for course in courses:
        grade = course["grade"]
        credits = course["credits"]

        total_points += grade * credits
        total_credits += credits

    if total_credits == 0:
        return 0

    return total_points / total_credits