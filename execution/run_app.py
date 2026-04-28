import subprocess
import sys
import os

def run_application():
    """
    Deterministic execution script to launch the main Hand Gesture Detector application.
    """
    print("[EXECUTION] Launching Hand Gesture Detector...")
    
    # Ensure we are in the root directory
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root_dir)
    
    # Path to main.py
    main_path = os.path.join(root_dir, "main.py")
    
    if not os.path.exists(main_path):
        print(f"[ERROR] Could not find {main_path}")
        sys.exit(1)
        
    try:
        # Run main.py using the same python interpreter
        subprocess.run([sys.executable, main_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Application exited with error: {e}")
    except KeyboardInterrupt:
        print("\n[INFO] Application stopped by user.")

if __name__ == "__main__":
    run_application()
