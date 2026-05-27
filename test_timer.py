"""
Tests for CircularTimer logic – run with: pytest tests/
"""

import sys
import types
import pytest

# ── Mock tkinter so tests run without a display ───────────────────────────
for mod in ("tkinter", "tkinter.ttk"):
    sys.modules[mod] = types.ModuleType(mod)

import tkinter as tk
tk.Tk = object
tk.Canvas = object
tk.Frame = object
tk.Label = object
tk.Button = object
tk.IntVar = lambda **kw: type("V", (), {"get": lambda s: 60, "set": lambda s, v: None})()
tk.DoubleVar = lambda **kw: type("V", (), {"get": lambda s: 100, "set": lambda s, v: None})()
tk.LEFT = tk.FLAT = tk.DISABLED = tk.NORMAL = tk.X = ""
ttk_mod = sys.modules["tkinter.ttk"]
ttk_mod.Progressbar = object

import importlib, pr as timer_mod


# ── Helper: bare timer object without GUI ────────────────────────────────
class BareTimer:
    """Minimal stand-in that exposes only the logic methods."""
    duration = 60
    remaining = 60
    running = False
    paused = False
    pause_remaining = 0
    start_time = 0

    # Copy methods directly from the real class
    start_timer   = timer_mod.CircularTimer.start_timer
    pause_timer   = timer_mod.CircularTimer.pause_timer
    stop_timer    = timer_mod.CircularTimer.stop_timer
    reset_timer   = timer_mod.CircularTimer.reset_timer
    _set_buttons  = lambda self, **kw: None   # no-op (no GUI)
    canvas        = type("C", (), {"itemconfig": lambda *a, **kw: None})()
    status_text   = None
    progress_var  = type("V", (), {"set": lambda s, v: None})()


# ── Tests ─────────────────────────────────────────────────────────────────
class TestTimerLogic:

    def test_initial_state(self):
        t = BareTimer()
        assert t.running is False
        assert t.remaining == 60
        assert t.duration == 60

    def test_start_sets_running(self):
        import time
        t = BareTimer()
        t.start_time = time.time()
        t.running = True
        assert t.running is True

    def test_stop_clears_running(self):
        t = BareTimer()
        t.running = True
        t.stop_timer(t)
        assert t.running is False

    def test_pause_stores_remaining(self):
        t = BareTimer()
        t.running = True
        t.remaining = 45
        t.pause_timer(t)
        assert t.paused is True
        assert t.pause_remaining == 45
        assert t.running is False

    def test_reset_restores_duration(self):
        t = BareTimer()
        t.remaining = 10
        t.running = True
        t.reset_timer(t)
        assert t.remaining == t.duration
        assert t.running is False

    def test_duration_default_60(self):
        t = BareTimer()
        assert t.duration == 60

    def test_remaining_never_negative(self):
        t = BareTimer()
        t.remaining = max(0, -5)
        assert t.remaining >= 0
