import subprocess
import sys
from pathlib import Path

TOOLS = {
    "1": Path("GA_Teaching_Tool/teaching_tool.py"),
    "2": Path("ACO_Teaching_Tool/antsp/app.py"),
    "3": Path("CAPyle_releaseV2/release/main.py")
}

def main():
        script = TOOLS.get("3")

        if not script or not script.exists():
            print("Invalid selection or script not found.")
            return

        try:
            subprocess.run([sys.executable, str(script)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the script: {e}")
        except KeyboardInterrupt:
            print("\nExecution interrupted by user. Returning to menu.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user. Goodbye!")
        sys.exit(0)
