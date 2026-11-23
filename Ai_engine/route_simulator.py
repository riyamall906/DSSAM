
import numpy as np


class RouteSimulator:

    def __init__(self, simulations=500, seed=42):
        if simulations < 1:
            raise ValueError("Simulations must be at least 1")

        self.simulations = simulations
        self.rng = np.random.default_rng(seed)

    def estimate_learning_time(
        self,
        current_mastery,
        target_mastery,
        hours_per_week,
        skill_debt=0.0,
        uncertainty=0.0
    ):
        
        if hours_per_week <= 0:
            raise ValueError("Hours per week must be greater than zero")

        if not 0 <= current_mastery <= 1:
            raise ValueError("Current mastery must be between 0 and 1")

        if not 0 <= target_mastery <= 1:
            raise ValueError("Target mastery must be between 0 and 1")

        if not 0 <= skill_debt <= 1:
            raise ValueError("Skill debt must be between 0 and 1")

        if not 0 <= uncertainty <= 1:
            raise ValueError("Uncertainty must be between 0 and 1")

        mastery_gap = target_mastery - current_mastery

        if mastery_gap <= 0:
            return {
                "average_days": 0.0,
                "lower_range": 0.0,
                "upper_range": 0.0
            }

        results = []

        for _ in range(self.simulations):

            base_progress = self.rng.uniform(0.03, 0.08)

            study_efficiency = hours_per_week / (
                hours_per_week + 5
            )

            weekly_progress = base_progress * study_efficiency

            debt_factor = 1 + skill_debt

            uncertainty_factor = self.rng.uniform(
                1 - 0.2 * uncertainty,
                1 + 0.2 * uncertainty
            )

            adjusted_progress = (
                weekly_progress / debt_factor
            ) * uncertainty_factor

            weeks_needed = mastery_gap / adjusted_progress

            study_days = (weeks_needed * 7) / hours_per_week

            results.append(study_days)

        return {
            "average_days": round(float(np.mean(results)), 2),
            "lower_range": round(float(np.percentile(results, 10)), 2),
            "upper_range": round(float(np.percentile(results, 90)), 2)
        }


if __name__ == "__main__":

    simulator = RouteSimulator(simulations=500)

    result = simulator.estimate_learning_time(
       current_mastery=0.40,
       target_mastery=0.80,
       hours_per_week=10,
       skill_debt=0.50,
       uncertainty=0.20
    )

    print("\n========== LEARNING TIME ESTIMATION ==========")

    print("Average Days:", result["average_days"])
    print("Lower Range:", result["lower_range"])
    print("Upper Range:", result["upper_range"])
