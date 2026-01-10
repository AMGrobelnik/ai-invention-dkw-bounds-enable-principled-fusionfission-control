"""DKW Controller Implementation."""
import json
import numpy as np
from dataclasses import dataclass, field

@dataclass
class DKWController:
    """DKW-guided fusion/fission controller."""
    epsilon_target: float = 0.10
    delta: float = 0.05
    min_samples: int = 100
    hysteresis: float = 0.05

    samples: list = field(default_factory=list)
    current_state: str = "fission"

    def dkw_epsilon(self, n: int) -> float:
        """Compute DKW epsilon for n samples."""
        if n < 2:
            return 1.0
        return np.sqrt(np.log(2 / self.delta) / (2 * n))

    def add_observation(self, error: float) -> None:
        """Add error observation for calibration."""
        self.samples.append(error)

    def decide(self) -> str:
        """Make fusion/fission decision with DKW guarantee."""
        n = len(self.samples)
        if n < self.min_samples:
            return self.current_state

        epsilon = self.dkw_epsilon(n)
        empirical_error = np.mean(self.samples[-self.min_samples:])
        error_upper_bound = empirical_error + epsilon

        if self.current_state == "fusion":
            if error_upper_bound > self.epsilon_target + self.hysteresis:
                self.current_state = "fission"
        else:
            if error_upper_bound < self.epsilon_target - self.hysteresis:
                self.current_state = "fusion"

        return self.current_state


def run_experiment(data_path: str):
    """Run DKW controller experiment."""
    with open(data_path) as f:
        data = json.load(f)

    controller = DKWController()
    results = {"baseline": [], "proposed": []}

    for example in data:
        # Simulate error occurrence based on difficulty
        error = np.random.random() < example["difficulty"]
        controller.add_observation(float(error))
        decision = controller.decide()

        results["proposed"].append({
            "id": example["id"],
            "decision": decision,
            "error": error,
        })
        results["baseline"].append({
            "id": example["id"],
            "decision": "fission",  # Always conservative
            "error": error,
        })

    return results


if __name__ == "__main__":
    results = run_experiment("../dataset_001/data_out.json")
    with open("method_out.json", "w") as f:
        json.dump(results, f, indent=2)
