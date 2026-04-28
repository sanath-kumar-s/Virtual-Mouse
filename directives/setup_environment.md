# Directive: Setup Environment

## Goal
Prepare the local environment for developing and running the Hand Gesture Detector.

## Steps
1. **Clone the repository** (if not already done).
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```
3. **Activate the virtual environment**:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Verify camera access**:
   - Ensure your webcam is connected and not blocked by privacy settings.
6. **Initialize .env**:
   - Copy `.env.example` to `.env` and adjust values if necessary.

## Tools
- `requirements.txt`
- `.env.example`
