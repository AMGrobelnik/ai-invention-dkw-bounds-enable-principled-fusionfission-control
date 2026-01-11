"""Dataset collection script for DKW benchmark."""
import json
from datasets import load_dataset

def collect_data():
    """Collect benchmark data for DKW controller evaluation."""
    # Load HuggingFace dataset
    ds = load_dataset("gsm8k", "main", split="test[:200]")

    data = []
    for i, example in enumerate(ds):
        data.append({
            "id": f"example_{i:03d}",
            "question": example["question"],
            "answer": example["answer"],
            "difficulty": len(example["question"]) / 100,  # Simple proxy
        })

    return data

if __name__ == "__main__":
    data = collect_data()
    with open("data_out.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Collected {len(data)} examples")
