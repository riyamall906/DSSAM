
import copy

class WhatIfAnalyzer:

    def __init__(self, simulator):
        self.simulator = simulator

    def compare_learning_plans(
        self,
        current_mastery,
        target_mastery,
        skill_debt,
        uncertainty,
        current_hours,
        new_hours
    ):

        # Current learning plan
        
        random_state = copy.deepcopy(
        self.simulator.rng.bit_generator.state
        )
        
        current_plan = self.simulator.estimate_learning_time(
            current_mastery=current_mastery,
            target_mastery=target_mastery,
            hours_per_week=current_hours,
            skill_debt=skill_debt,
            uncertainty=uncertainty
        )

        # New learning plan
        
        self.simulator.rng.bit_generator.state = copy.deepcopy(
        random_state
        )
        
        new_plan = self.simulator.estimate_learning_time(
            current_mastery=current_mastery,
            target_mastery=target_mastery,
            hours_per_week=new_hours,
            skill_debt=skill_debt,
            uncertainty=uncertainty
        )

        days_saved = (
            current_plan["average_days"]
            - new_plan["average_days"]
        )

        return {
            "current_plan": current_plan,
            "new_plan": new_plan,
            "days_saved": round(days_saved, 2)
        }


if __name__ == "__main__":

    from route_simulator import RouteSimulator

    simulator = RouteSimulator(simulations=500)

    analyzer = WhatIfAnalyzer(simulator)

    result = analyzer.compare_learning_plans(
        current_mastery=0.1273,
        target_mastery=0.80,
        skill_debt=0.78,
        uncertainty=0.20,
        current_hours=10,
        new_hours=20
    )

    print("\n========== WHAT-IF ANALYSIS ==========")

    print("\nCurrent Plan (10 hours/week):")
    print(result["current_plan"])

    print("\nNew Plan (15 hours/week):")
    print(result["new_plan"])

    print("\nEstimated Days Saved:",
          result["days_saved"])
