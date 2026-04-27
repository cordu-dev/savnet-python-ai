from pathlib import Path

students = [
    {"student_id": 1, "score": 5},
    {"student_id": 2, "score": 5},
    {"student_id": 3, "score": 5},
    {"student_id": 4, "score": 5},
    {"student_id": 5, "score": 9},
    {"student_id": 6, "score": 6},
    {"student_id": 7, "score": 8},
    {"student_id": 8, "score": 6},
    {"student_id": 9, "score": 7},
    {"student_id": 10, "score": 3},
    {"student_id": 11, "score": 5},
    {"student_id": 12, "score": 4},
    {"student_id": 13, "score": 6},
    {"student_id": 14, "score": 5},
    {"student_id": 15, "score": 7},
    {"student_id": 16, "score": 8},
    {"student_id": 17, "score": 9},
    {"student_id": 18, "score": 7},
]

TEAM_SIZE = 3
OUTPUT_FILE = Path(__file__).with_name("homogeneous_teams_output.txt")


def build_homogeneous_teams(student_list, team_size):
    sorted_students = sorted(student_list, key=lambda student: (student["score"], student["student_id"]))
    teams = []

    for index in range(0, len(sorted_students), team_size):
        team = sorted_students[index:index + team_size]
        teams.append(team)

    return teams


def describe_team(team, team_number):
    scores = [student["score"] for student in team]
    student_ids = [student["student_id"] for student in team]
    minimum_score = min(scores)
    maximum_score = max(scores)
    average_score = sum(scores) / len(scores)
    score_range = maximum_score - minimum_score

    if score_range == 0:
        reason = "This team is very homogeneous because all students gave themselves the same score."
    elif score_range == 1:
        reason = "This team is homogeneous because the students have very close self-evaluations."
    elif score_range == 2:
        reason = "This team is still fairly homogeneous because the score difference is small."
    else:
        reason = "This team is less homogeneous than the others because the score spread is larger."

    lines = [
        f"Team {team_number}",
        f"  Students: {student_ids}",
        f"  Scores:   {scores}",
        f"  Average:  {average_score:.2f}",
        f"  Range:    {minimum_score} to {maximum_score} (spread = {score_range})",
        f"  Reason:   {reason}",
        "",
    ]

    return "\n".join(lines)


def build_report(teams):
    lines = [
        "Homogeneous teams based on self-score",
        "=" * 40,
        f"Total students: {len(students)}",
        f"Team size: {TEAM_SIZE}",
        f"Number of teams: {len(teams)}",
        "",
    ]

    for team_number, team in enumerate(teams, start=1):
        lines.append(describe_team(team, team_number))

    return "\n".join(lines)


teams = build_homogeneous_teams(students, TEAM_SIZE)
report = build_report(teams)

print(report)

with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
    output_file.write(report)

print(f"\nReport saved to: {OUTPUT_FILE}")
