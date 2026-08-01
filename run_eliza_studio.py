"""
ELIZA Studio Launcher Script.
Boots the Studio backend server and serves the web interface on http://127.0.0.1:8000.
"""

import sys
from studio.server import run_studio_server

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_studio_server(port=port)
