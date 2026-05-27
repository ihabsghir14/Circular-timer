import tkinter as tk
from tkinter import ttk
import math
import time
import winsound  # Windows only – safely ignored on other OS


class CircularTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Circular Timer – Petrochemical Engineering")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4f8")

        # ── State ──────────────────────────────────────────────────────────
        self.running = False
        self.paused = False
        self.start_time = 0
        self.pause_remaining = 0
        self.duration = 60
        self.remaining = 60

        # ── Title label ────────────────────────────────────────────────────
        tk.Label(
            self.root, text="⏱  Circular Timer",
            font=("Arial", 16, "bold"), bg="#f0f4f8", fg="#2c3e50"
        ).pack(pady=(12, 0))

        # ── Duration selector ──────────────────────────────────────────────
        sel_frame = tk.Frame(self.root, bg="#f0f4f8")
        sel_frame.pack(pady=6)
        tk.Label(sel_frame, text="Duration:", font=("Arial", 10),
                 bg="#f0f4f8").pack(side=tk.LEFT, padx=4)
        self.duration_var = tk.IntVar(value=60)
        for sec in (30, 60, 90, 120):
            tk.Radiobutton(
                sel_frame, text=f"{sec}s", variable=self.duration_var,
                value=sec, command=self._on_duration_change,
                bg="#f0f4f8", activebackground="#f0f4f8"
            ).pack(side=tk.LEFT, padx=2)

        # ── Canvas ─────────────────────────────────────────────────────────
        self.canvas = tk.Canvas(
            self.root, width=400, height=360,
            bg="#f0f4f8", highlightthickness=0
        )
        self.canvas.pack()
        self._draw_clock_face()

        # ── Progress bar ───────────────────────────────────────────────────
        self.progress_var = tk.DoubleVar(value=100)
        self.progress = ttk.Progressbar(
            self.root, variable=self.progress_var,
            maximum=100, length=300, mode="determinate"
        )
        self.progress.pack(pady=4)

        # ── Buttons ────────────────────────────────────────────────────────
        btn_frame = tk.Frame(self.root, bg="#f0f4f8")
        btn_frame.pack(pady=8)

        btn_cfg = dict(font=("Arial", 11, "bold"), width=7,
                       relief=tk.FLAT, cursor="hand2")

        self.start_btn = tk.Button(
            btn_frame, text="▶  Start", bg="#27ae60", fg="white",
            command=self.start_timer, **btn_cfg)
        self.start_btn.pack(side=tk.LEFT, padx=4)

        self.pause_btn = tk.Button(
            btn_frame, text="⏸  Pause", bg="#f39c12", fg="white",
            command=self.pause_timer, **btn_cfg, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=4)

        self.stop_btn = tk.Button(
            btn_frame, text="⏹  Stop", bg="#e74c3c", fg="white",
            command=self.stop_timer, **btn_cfg, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=4)

        self.reset_btn = tk.Button(
            btn_frame, text="↺  Reset", bg="#3498db", fg="white",
            command=self.reset_timer, **btn_cfg)
        self.reset_btn.pack(side=tk.LEFT, padx=4)

        # ── Owner info ─────────────────────────────────────────────────────
        info_frame = tk.Frame(self.root, bg="#dce6f0", pady=6)
        info_frame.pack(fill=tk.X, pady=(4, 0))
        tk.Label(info_frame, text="👤 Ben Brahim Houssem Iheb",
                 font=("Arial", 11, "bold"), bg="#dce6f0", fg="#2c3e50").pack()
        tk.Label(info_frame, text="👤 Draoui Ahcene Borhene",
                 font=("Arial", 11, "bold"), bg="#dce6f0", fg="#2c3e50").pack()
        tk.Label(info_frame, text="👥 Team: Group 08",
                 font=("Arial", 10), bg="#dce6f0", fg="#555").pack()

        # ── Start loop ─────────────────────────────────────────────────────
        self._update_timer()

    # ── Drawing ─────────────────────────────────────────────────────────────
    def _draw_clock_face(self):
        cx, cy, r = 200, 175, 130

        # Tick marks
        for i in range(60):
            angle = math.radians(i * 6 - 90)
            r_outer = r
            r_inner = r - (8 if i % 5 == 0 else 4)
            lw = 2 if i % 5 == 0 else 1
            self.canvas.create_line(
                cx + r_inner * math.cos(angle), cy + r_inner * math.sin(angle),
                cx + r_outer * math.cos(angle), cy + r_outer * math.sin(angle),
                width=lw, fill="#7f8c8d"
            )

        # Outer ring
        self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            width=5, outline="#2c3e50"
        )

        # Colored arc (will be redrawn each tick)
        self.arc = self.canvas.create_arc(
            cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10,
            start=90, extent=360,
            style=tk.ARC, outline="#27ae60", width=8
        )

        # Hand
        self.hand = self.canvas.create_line(
            cx, cy, cx, cy - 110,
            width=4, fill="#e74c3c", capstyle=tk.ROUND
        )

        # Center dot
        self.canvas.create_oval(
            cx - 7, cy - 7, cx + 7, cy + 7,
            fill="#2c3e50", outline=""
        )

        # Time text
        self.time_text = self.canvas.create_text(
            cx, cy + 40, text="60",
            font=("Arial", 36, "bold"), fill="#2c3e50"
        )

        # Status text
        self.status_text = self.canvas.create_text(
            cx, cy + 80, text="Ready",
            font=("Arial", 12), fill="#7f8c8d"
        )

    # ── Controls ─────────────────────────────────────────────────────────────
    def start_timer(self):
        if not self.running:
            self.running = True
            self.paused = False
            if self.pause_remaining > 0:
                # Resume from pause
                self.start_time = time.time() - (self.duration - self.pause_remaining)
                self.pause_remaining = 0
            else:
                self.remaining = self.duration
                self.start_time = time.time()
            self._set_buttons(running=True)
            self.canvas.itemconfig(self.status_text, text="Running…", fill="#27ae60")

    def pause_timer(self):
        if self.running:
            self.running = False
            self.paused = True
            self.pause_remaining = self.remaining
            self._set_buttons(paused=True)
            self.canvas.itemconfig(self.status_text, text="Paused", fill="#f39c12")

    def stop_timer(self):
        self.running = False
        self.paused = False
        self.pause_remaining = 0
        self._set_buttons()
        self.canvas.itemconfig(self.status_text, text="Stopped", fill="#e74c3c")

    def reset_timer(self):
        self.running = False
        self.paused = False
        self.pause_remaining = 0
        self.remaining = self.duration
        self._redraw(self.duration)
        self._set_buttons()
        self.canvas.itemconfig(self.status_text, text="Ready", fill="#7f8c8d")
        self.progress_var.set(100)

    def _on_duration_change(self):
        self.duration = self.duration_var.get()
        self.reset_timer()

    # ── Button states ────────────────────────────────────────────────────────
    def _set_buttons(self, running=False, paused=False):
        self.start_btn.config(state=tk.DISABLED if running else tk.NORMAL)
        self.pause_btn.config(state=tk.NORMAL if running else tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL if (running or paused) else tk.DISABLED)

    # ── Update loop ──────────────────────────────────────────────────────────
    def _update_timer(self):
        if self.running and self.remaining > 0:
            elapsed = time.time() - self.start_time
            self.remaining = max(0, self.duration - elapsed)
            self._redraw(self.remaining)
            pct = (self.remaining / self.duration) * 100
            self.progress_var.set(pct)

            if self.remaining == 0:
                self._on_finish()

        self.root.after(100, self._update_timer)

    def _redraw(self, remaining):
        cx, cy, r = 200, 175, 120
        # Update arc
        extent = (remaining / self.duration) * 360
        color = "#27ae60" if remaining > self.duration * 0.4 else \
                "#f39c12" if remaining > self.duration * 0.15 else "#e74c3c"
        self.canvas.itemconfig(self.arc, extent=-extent, outline=color)

        # Update hand
        angle = (remaining / self.duration) * 360
        rad = math.radians(angle - 90)
        x = cx + 110 * math.cos(rad)
        y = cy + 110 * math.sin(rad)
        self.canvas.coords(self.hand, cx, cy, x, y)
        self.canvas.itemconfig(self.hand, fill=color)

        # Update text
        self.canvas.itemconfig(self.time_text, text=str(int(remaining)), fill=color)

    def _on_finish(self):
        self.running = False
        self._set_buttons()
        self.canvas.itemconfig(self.status_text, text="✅ Time's up!", fill="#e74c3c")
        self.canvas.itemconfig(self.time_text, text="0", fill="#e74c3c")
        self.progress_var.set(0)
        try:
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except Exception:
            pass  # Not on Windows – no sound, no crash


# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = CircularTimer(root)
    root.mainloop()
