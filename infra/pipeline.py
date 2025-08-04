import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_pipeline():
    """Simple workflow orchestration"""
    print("Starting CO₂ Forecast MLOps Pipeline")
    print("=" * 50)

    steps = [
        ("Data Processing", "make prepare-data"),
        ("Model Training", "make train-model"),
        ("Model Validation", "make train-cv"),
        ("API Health Check", "make test-api"),
        ("Monitoring", "pipenv run python monitoring/monitor.py"),
    ]

    results = {}

    for step_name, command in steps:
        print(f"\nRunning: {step_name}")
        print(f"Command: {command}")

        try:
            start_time = datetime.now()
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            if result.returncode == 0:
                print(f"SUCCESS: {step_name} completed successfully ({duration:.1f}s)")
                results[step_name] = "SUCCESS"
            else:
                print(f"FAILED: {step_name} failed ({duration:.1f}s)")
                print(f"Error: {result.stderr}")
                results[step_name] = "FAILED"

        except subprocess.TimeoutExpired:
            print(f"TIMEOUT: {step_name} timed out")
            results[step_name] = "TIMEOUT"
        except Exception as e:
            print(f"ERROR: {step_name} error: {e}")
            results[step_name] = "ERROR"

    # Summary
    print("\n" + "=" * 50)
    print("Pipeline Summary")
    print("=" * 50)

    for step_name, status in results.items():
        status_prefix = {
            "SUCCESS": "SUCCESS",
            "FAILED": "FAILED",
            "TIMEOUT": "TIMEOUT",
            "ERROR": "ERROR",
        }
        print(f"{status_prefix[status]}: {step_name}: {status}")

    success_count = sum(1 for status in results.values() if status == "SUCCESS")
    total_count = len(results)
    print(f"\nOverall: {success_count}/{total_count} steps completed successfully")

    return results


if __name__ == "__main__":
    run_pipeline()
