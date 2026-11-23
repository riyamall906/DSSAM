
class LearningRouteGenerator:

    def __init__(self, mastery, skill_debt, graph):
        self.mastery = mastery
        self.skill_debt = skill_debt
        self.graph = graph

        self.project_priority = {
            "Programming Fundamentals": 0.6,
            "Python": 1.0,
            "SQL": 0.9,
            "Data Structures": 0.8,
            "Algorithms": 0.7
        }

    def calculate_priority(self, skill, route_type):

        mastery = self.mastery.get(skill, 0.0)
        debt = self.skill_debt.get(skill, 0.0)

        if route_type == "fastest":
            return mastery * 0.5 + (1 - debt) * 0.5

        elif route_type == "foundation":
            return debt * 0.7 + (1 - mastery) * 0.3

        elif route_type == "project":
            return (
                self.project_priority.get(skill, 0.5) * 0.6
                + debt * 0.2
                + (1 - mastery) * 0.2
            )

        return 0.0

    def generate_route(self, route_type):

        remaining = set(self.graph.nodes)
        completed = []
        route = []

        while remaining:

            available = [
                skill for skill in remaining
                if all(
                    parent in completed
                    for parent in self.graph.predecessors(skill)
                )
            ]

            if not available:
                raise ValueError(
                    "Invalid dependency graph or circular dependency"
                )

            selected = sorted(
                available,
                key=lambda skill: (
                    -self.calculate_priority(skill, route_type),
                    skill
                )
            )[0]

            route.append(selected)
            completed.append(selected)
            remaining.remove(selected)

        return route

    def fastest_route(self):
        return self.generate_route("fastest")

    def strong_foundation_route(self):
        return self.generate_route("foundation")

    def project_oriented_route(self):
        return self.generate_route("project")

    def generate_routes(self):

        return {
            "Fastest Route": self.fastest_route(),
            "Strong Foundation Route": self.strong_foundation_route(),
            "Project-Oriented Route": self.project_oriented_route()
        }
