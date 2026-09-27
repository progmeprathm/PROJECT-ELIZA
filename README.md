# E.L.I.Z.A. Companion (Desktop Edition)

This is the **Consumer / Daily Use** branch of the E.L.I.Z.A. cognitive operating system. 

It implements the "Human E.L.I.Z.A." product philosophy: hiding the complex multi-agent engineering underneath a beautiful, seamless chat interface. Users interact with E.L.I.Z.A. through outcomes ("What would you like to get done?") rather than cognitive infrastructure.

## Features
- **Human E.L.I.Z.A. UI:** An outcome-focused chat interface with an Omnibar.
- **Local Settings Modal:** Allows the user to input API keys locally in the browser.
- **Offline Mode:** Includes a toggle to force "Local Compute Only" (Ollama).
- **Single-Tenant Backend:** The server dynamically injects API keys passed from the browser headers into the execution environment.

## How to Run

1. Open a terminal in this directory (`Eliza-Desktop`).
2. Run the studio server:
```bash
python run_eliza_studio.py
```
3. Open your browser and navigate to `http://127.0.0.1:8000`
4. Click the **Settings** gear icon in the top right to configure your API Keys or enable Local Offline Mode.
