"""
ELIZA Companion & Studio Launcher Script.
Boots the ECOS Kernel and launches ELIZA Companion & Studio at http://127.0.0.1:8000.
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
    print("==================================================")
    print("  LAUNCHING ELIZA COMPANION & STUDIO v0.1")
    print("  The Conversational Client to the ECOS Kernel")
    print("==================================================")
    run_studio_server(port=port)
