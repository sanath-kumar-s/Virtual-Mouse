# Project Directives (SOPs)

This directory contains Standard Operating Procedures (SOPs) for the Hand Gesture Detector project, following the 3-layer architecture defined in `AGENT.md`.

## Available Directives

| Directive | Goal | Tool |
|-----------|------|------|
| [Run App](run_hand_gesture_system.md) | Launch the main tracking system | `execution/run_app.py` |
| [Calibrate](calibrate_system.md) | Calibrate gesture sensitivity | `execution/calibrate.py` |
| [Setup Env](setup_environment.md) | Initialize development environment | N/A |

## Philosophy
Each directive explains **what** to do in natural language, while the `execution/` scripts handle the **how** deterministically.
If a script fails, the agent should:
1. Fix the script.
2. Verify it works.
3. Update the directive if necessary (self-annealing).
