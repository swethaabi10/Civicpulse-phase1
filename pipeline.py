import argparse

def run_pipeline(stage: str = "all"):
    stages = ["load", "checks", "warehouse", "measures"]
    to_run = stages if stage == "all" else [stage]
    for step in to_run:
        print(f"[CivicPulse] Running stage: {step}...")
    print("[CivicPulse] Pipeline execution complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CivicPulse Phase 1 Data Pipeline")
    parser.add_argument("--stage", default="all", help="Stage to run: all, load, checks, warehouse, measures")
    args = parser.parse_args()
    run_pipeline(args.stage)
