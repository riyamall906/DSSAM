
import networkx as nx


class SkillGraph:

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_skill(self, skill):
        self.graph.add_node(skill)

    def add_dependency(self, prerequisite, dependent, weight=1.0):
        self.graph.add_edge(
            prerequisite,
            dependent,
            weight=weight
        )

    def show_graph(self):
        print("\nSkill Dependency Graph:")

        for skill in self.graph.nodes:
            print("Skill:", skill)

        print("\nDependencies:")

        for source, target, data in self.graph.edges(data=True):
            print(
                source, "->", target,
                "| Weight:", data["weight"]
            )


if __name__ == "__main__":

    skill_graph = SkillGraph()

    skills = [
        "Programming Fundamentals",
        "Python",
        "SQL",
        "Data Structures",
        "Algorithms"
    ]

    for skill in skills:
        skill_graph.add_skill(skill)

    skill_graph.add_dependency("Programming Fundamentals", "Python", 0.9)
    skill_graph.add_dependency("Programming Fundamentals", "SQL", 0.8)
    skill_graph.add_dependency("Programming Fundamentals", "Data Structures", 0.9)
    skill_graph.add_dependency("Data Structures", "Algorithms", 1.0)

    skill_graph.show_graph()
