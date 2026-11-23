
from skill_analyzer import SkillAnalyzer
from skill_graph import SkillGraph
from skill_debt import SkillDebtAnalyzer
from route_simulator import RouteSimulator
from learning_routes import LearningRouteGenerator
from what_if import WhatIfAnalyzer

# 1. SKILL MASTERY ANALYSIS

analyzer = SkillAnalyzer()

skills = [
    "Programming Fundamentals",
    "Python",
    "SQL",
    "Data Structures",
    "Algorithms"
]

for skill in skills:
    analyzer.add_skill(skill)

submissions = [
    ("Python", True),
    ("Python", True),
    ("SQL", False),
    ("SQL", True),
    ("Data Structures", True),
    ("Algorithms", False)
]

for skill, correct in submissions:
    analyzer.update_mastery(skill, correct)

# Convert mastery percentages into values between 0 and 1
mastery = {
    skill: value / 100
    for skill, value in analyzer.get_all_mastery().items()
}

uncertainty = {
    skill: value / 100
    for skill, value in analyzer.get_all_uncertainty().items()
}

print("\n========== SKILL MASTERY ==========")

for skill, value in mastery.items():
    print(skill, ":", round(value * 100, 2), "%")

print("\n========== MASTERY UNCERTAINTY ==========")

for skill, value in uncertainty.items():
    print(skill, ":", round(value * 100, 2), "%")


# 2. SKILL DEPENDENCY GRAPH

skill_graph = SkillGraph()

for skill in skills:
    skill_graph.add_skill(skill)

skill_graph.add_dependency("Programming Fundamentals", "Python", 0.9)
skill_graph.add_dependency("Programming Fundamentals", "SQL", 0.8)
skill_graph.add_dependency("Programming Fundamentals", "Data Structures", 0.9)
skill_graph.add_dependency("Data Structures", "Algorithms", 1.0)


# 3. SKILL DEBT ANALYSIS

debt_analyzer = SkillDebtAnalyzer(skill_graph.graph)

debt = debt_analyzer.calculate_debt(mastery)

print("\n========== SKILL DEBT ==========")

for skill, value in debt.items():
    print(skill, ":", value)


# 4. MONTE CARLO SIMULATION

simulator = RouteSimulator(simulations=500)

simulation_result = simulator.estimate_learning_time(
    current_mastery=mastery["Algorithms"],
    target_mastery=0.80,
    hours_per_week=10,
    skill_debt=debt["Algorithms"],
    uncertainty=uncertainty["Algorithms"]
)

print("\n========== LEARNING TIME ESTIMATION ==========")

print("Average Days:", simulation_result["average_days"])
print("Lower Range:", simulation_result["lower_range"])
print("Upper Range:", simulation_result["upper_range"])


# 5. LEARNING ROUTE GENERATION

route_generator = LearningRouteGenerator(
    mastery,
    debt,
    skill_graph.graph
)

routes = route_generator.generate_routes()

print("\n========== RECOMMENDED LEARNING ROUTES ==========")

for route_name, route_skills in routes.items():

    print("\n" + route_name)

    for index, skill in enumerate(route_skills, start=1):
        print(index, ".", skill)


# 6. WHAT-IF ANALYSIS

what_if_analyzer = WhatIfAnalyzer(simulator)

what_if_result = what_if_analyzer.compare_learning_plans(
    current_mastery=mastery["Algorithms"],
    target_mastery=0.80,
    skill_debt=debt["Algorithms"],
    uncertainty=uncertainty["Algorithms"],
    current_hours=10,
    new_hours=15
)

print("\n========== WHAT-IF ANALYSIS ==========")

print("\nCurrent Plan (10 hours/week):")
print(what_if_result["current_plan"])

print("\nNew Plan (15 hours/week):")
print(what_if_result["new_plan"])

print("\nEstimated Days Saved:",
      what_if_result["days_saved"])


print("\n========== DSSAM AI ANALYSIS COMPLETED ==========")