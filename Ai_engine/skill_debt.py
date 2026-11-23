
import networkx as nx


class SkillDebtAnalyzer:

    def __init__(self, skill_graph, decay=0.5):
        self.graph = skill_graph
        self.decay = decay

    def calculate_debt(self, mastery):

        debt = {}

        for skill in nx.topological_sort(self.graph):

            total_debt = 0.0

            parents = self.graph.predecessors(skill)

            for parent in parents:

                parent_mastery = mastery.get(parent, 0.0)

                weight = self.graph[parent][skill]["weight"]

                direct_debt = (1 - parent_mastery) * weight

                propagated_debt = debt[parent] * self.decay

                total_debt += direct_debt + propagated_debt

            debt[skill] = round(min(total_debt, 1.0), 2)

        return debt


if __name__ == "__main__":

    graph = nx.DiGraph()

    graph.add_edge("Programming Fundamentals", "Python", weight=0.9)
    graph.add_edge("Programming Fundamentals", "SQL", weight=0.8)
    graph.add_edge("Programming Fundamentals", "Data Structures", weight=0.9)
    graph.add_edge("Data Structures", "Algorithms", weight=1.0)

    mastery = {
        "Programming Fundamentals": 0.20,
        "Python": 0.87,
        "SQL": 0.45,
        "Data Structures": 0.57,
        "Algorithms": 0.12
    }

    analyzer = SkillDebtAnalyzer(graph, decay=0.5)

    debt = analyzer.calculate_debt(mastery)

    print("\nMulti-Level Skill Debt Report:\n")

    for skill, value in debt.items():
        print(skill, ":", value)
