
class SkillAnalyzer:

    def __init__(self, initial_mastery=0.2, learning_rate=0.1,
                 guess=0.2, slip=0.1):

        self.initial_mastery = initial_mastery
        self.learning_rate = learning_rate
        self.guess = guess
        self.slip = slip

        self.skills = {}

    def add_skill(self, skill_name):

        self.skills[skill_name] = {
            "mean": self.initial_mastery,
            "uncertainty": 0.25
        }

    def update_mastery(self, skill_name, correct):

        if skill_name not in self.skills:
            self.add_skill(skill_name)

        prior = self.skills[skill_name]["mean"]
        uncertainty = self.skills[skill_name]["uncertainty"]

        if correct:
            numerator = prior * (1 - self.slip)
            denominator = numerator + (1 - prior) * self.guess
        else:
            numerator = prior * self.slip
            denominator = numerator + (1 - prior) * (1 - self.guess)

        posterior = numerator / denominator

        new_mastery = (
            posterior + (1 - posterior) * self.learning_rate
        )

        new_uncertainty = uncertainty * 0.8

        self.skills[skill_name] = {
            "mean": new_mastery,
            "uncertainty": new_uncertainty
        }

        return round(new_mastery * 100, 2)

    def get_mastery(self, skill_name):

        if skill_name not in self.skills:
            return 0.0

        return round(self.skills[skill_name]["mean"] * 100, 2)

    def get_all_mastery(self):

        return {
            skill: round(data["mean"] * 100, 2)
            for skill, data in self.skills.items()
        }

    def get_all_uncertainty(self):

        return {
            skill: round(data["uncertainty"] * 100, 2)
            for skill, data in self.skills.items()
        }


if __name__ == "__main__":

    analyzer = SkillAnalyzer()

    skills = ["Python", "SQL", "Data Structures", "Algorithms"]

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

    print("\nFinal Skill Mastery:")

    for skill, mastery in analyzer.get_all_mastery().items():
        print(skill, ":", mastery, "%")

    print("\nMastery Uncertainty:")

    for skill, uncertainty in analyzer.get_all_uncertainty().items():
        print(skill, ":", uncertainty, "%")
