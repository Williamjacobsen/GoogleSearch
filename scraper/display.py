"""Virtual display (Xvfb) management for headless servers."""

import os
import shutil
import subprocess
import time

from .config import XVFB_DISPLAY, XVFB_RESOLUTION


class VirtualDisplay:
    """Manages an Xvfb virtual display."""

    def __init__(self):
        self._proc = None
        self._original_display = os.environ.get("DISPLAY", "")

    def start(self) -> bool:
        """Start Xvfb if no DISPLAY is set. Returns True if started."""
        if self._original_display:
            return False
        if not shutil.which("Xvfb"):
            return False

        self._proc = subprocess.Popen(
            ["Xvfb", XVFB_DISPLAY, "-screen", "0", XVFB_RESOLUTION, "-ac"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        os.environ["DISPLAY"] = XVFB_DISPLAY
        time.sleep(0.5)
        return True

    def stop(self) -> None:
        """Stop Xvfb and restore DISPLAY."""
        if self._proc:
            self._proc.terminate()
            self._proc.wait()
            self._proc = None
        if self._original_display:
            os.environ["DISPLAY"] = self._original_display
        elif "DISPLAY" in os.environ:
            del os.environ["DISPLAY"]

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *_):
        self.stop()
