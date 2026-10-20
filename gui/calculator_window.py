import tkinter as tk
from tkinter import messagebox

from core.calculator_logic import CalculatorLogic


class CalculatorWindow:
    """Builds and manages the calculator GUI."""

    BACKGROUND = "#111827"
    PANEL = "#1F2937"
    DISPLAY_BG = "#0B1220"
    TEXT = "#F9FAFB"
    MUTED = "#9CA3AF"
    BLUE = "#2563EB"
    BLUE_HOVER = "#1D4ED8"
    BUTTON = "#374151"
    BUTTON_HOVER = "#4B5563"
    ORANGE = "#EA580C"
    GREEN = "#059669"
    RED = "#DC2626"

    def __init__(self, root):
        self.root = root
        self.logic = CalculatorLogic()
        self.history = []

        self.root.title("Naveen's Advanced Calculator")
        self.root.geometry("900x650")
        self.root.minsize(600, 500)
        self.root.configure(bg=self.BACKGROUND)

        self.expression = tk.StringVar()

        self._create_widgets()
        self._bind_keyboard()

    def _create_widgets(self):
        # Main layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)

        calculator = tk.Frame(
            self.root,
            bg=self.BACKGROUND,
            padx=18,
            pady=18,
        )
        calculator.grid(row=0, column=0, sticky="nsew")
        calculator.grid_columnconfigure(0, weight=1)
        calculator.grid_rowconfigure(2, weight=1)

        history_panel = tk.Frame(
            self.root,
            bg=self.PANEL,
            padx=12,
            pady=18,
        )
        history_panel.grid(row=0, column=1, sticky="nsew")
        history_panel.grid_columnconfigure(0, weight=1)
        history_panel.grid_rowconfigure(1, weight=1)

        # Title
        tk.Label(
            calculator,
            text="ADVANCED CALCULATOR",
            font=("Segoe UI", 17, "bold"),
            bg=self.BACKGROUND,
            fg=self.TEXT,
        ).grid(row=0, column=0, sticky="w", pady=(0, 12))

        # Display
        display_frame = tk.Frame(
            calculator,
            bg=self.DISPLAY_BG,
            padx=12,
            pady=10,
        )
        display_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 14),
        )
        display_frame.grid_columnconfigure(0, weight=1)

        self.display = tk.Entry(
            display_frame,
            textvariable=self.expression,
            font=("Consolas", 23),
            bg=self.DISPLAY_BG,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat",
            justify="right",
            bd=0,
        )
        self.display.grid(row=0, column=0, sticky="ew", ipady=12)

        tk.Label(
            calculator,
            text="Scientific mode • Trigonometry uses degrees",
            font=("Segoe UI", 9),
            bg=self.BACKGROUND,
            fg=self.MUTED,
        ).grid(row=2, column=0, sticky="nw", pady=(0, 8))

        # Buttons
        buttons_frame = tk.Frame(calculator, bg=self.BACKGROUND)
        buttons_frame.grid(row=3, column=0, sticky="nsew")

        for column in range(5):
            buttons_frame.grid_columnconfigure(column, weight=1, uniform="col")

        for row in range(6):
            buttons_frame.grid_rowconfigure(row, weight=1, uniform="row")

        buttons = [
            ("sin(", 0, 0, self.BUTTON),
            ("cos(", 0, 1, self.BUTTON),
            ("tan(", 0, 2, self.BUTTON),
            ("sqrt(", 0, 3, self.BUTTON),
            ("C", 0, 4, self.RED),

            ("log(", 1, 0, self.BUTTON),
            ("ln(", 1, 1, self.BUTTON),
            ("(", 1, 2, self.BUTTON),
            (")", 1, 3, self.BUTTON),
            ("⌫", 1, 4, self.ORANGE),

            ("7", 2, 0, self.PANEL),
            ("8", 2, 1, self.PANEL),
            ("9", 2, 2, self.PANEL),
            ("/", 2, 3, self.BLUE),
            ("%", 2, 4, self.BLUE),

            ("4", 3, 0, self.PANEL),
            ("5", 3, 1, self.PANEL),
            ("6", 3, 2, self.PANEL),
            ("*", 3, 3, self.BLUE),
            ("**", 3, 4, self.BLUE),

            ("1", 4, 0, self.PANEL),
            ("2", 4, 1, self.PANEL),
            ("3", 4, 2, self.PANEL),
            ("-", 4, 3, self.BLUE),
            ("pi", 4, 4, self.BLUE),

            ("0", 5, 0, self.PANEL),
            (".", 5, 1, self.PANEL),
            ("e", 5, 2, self.BLUE),
            ("+", 5, 3, self.BLUE),
            ("=", 5, 4, self.GREEN),
        ]

        for label, row, column, color in buttons:
            button = tk.Button(
                buttons_frame,
                text=label,
                font=("Segoe UI", 12, "bold"),
                bg=color,
                fg=self.TEXT,
                activebackground=self.BUTTON_HOVER,
                activeforeground=self.TEXT,
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda value=label: self._on_button_click(value),
            )
            button.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=3,
                pady=3,
                ipadx=2,
                ipady=5,
            )

            hover_color = (
                self.BLUE_HOVER
                if color == self.BLUE
                else self.BUTTON_HOVER
            )

            button.bind(
                "<Enter>",
                lambda event, widget=button, hover=hover_color:
                    widget.configure(bg=hover),
            )
            button.bind(
                "<Leave>",
                lambda event, widget=button, original=color:
                    widget.configure(bg=original),
            )

        # History panel
        tk.Label(
            history_panel,
            text="HISTORY",
            font=("Segoe UI", 14, "bold"),
            bg=self.PANEL,
            fg=self.TEXT,
        ).grid(row=0, column=0, sticky="w", pady=(0, 12))

        self.history_list = tk.Listbox(
            history_panel,
            bg=self.DISPLAY_BG,
            fg=self.TEXT,
            selectbackground=self.BLUE,
            font=("Consolas", 10),
            relief="flat",
            bd=0,
            activestyle="none",
        )
        self.history_list.grid(row=1, column=0, sticky="nsew")

        self.history_list.bind(
            "<Double-Button-1>",
            self._reuse_history,
        )

        tk.Button(
            history_panel,
            text="Clear History",
            font=("Segoe UI", 10, "bold"),
            bg=self.BUTTON,
            fg=self.TEXT,
            activebackground=self.BUTTON_HOVER,
            relief="flat",
            cursor="hand2",
            command=self._clear_history,
        ).grid(row=2, column=0, sticky="ew", pady=(12, 0), ipady=8)

        tk.Label(
            history_panel,
            text="Double-click a result to reuse it.",
            font=("Segoe UI", 8),
            bg=self.PANEL,
            fg=self.MUTED,
            wraplength=160,
        ).grid(row=3, column=0, sticky="w", pady=(10, 0))

    def _bind_keyboard(self):
        self.display.bind("<Return>", self._calculate_event)
        self.display.bind("<KP_Enter>", self._calculate_event)
        self.display.bind("<Escape>", self._clear_event)

    def _on_button_click(self, value):
        if value == "C":
            self._clear()
        elif value == "⌫":
            current = self.expression.get()
            self.expression.set(current[:-1])
        elif value == "=":
            self._calculate()
        else:
            self.display.insert(tk.INSERT, value)
            self.display.focus_set()

    def _calculate_event(self, event=None):
        self._calculate()
        return "break"

    def _clear_event(self, event=None):
        self._clear()
        return "break"

    def _calculate(self):
        expression = self.expression.get().strip()

        if not expression:
            return

        try:
            result = self.logic.calculate(expression)

            if isinstance(result, float) and result.is_integer():
                result = int(result)

            result_text = str(result)

            self.history.insert(
                0,
                f"{expression} = {result_text}",
            )
            self.history_list.insert(
                0,
                f"{expression} = {result_text}",
            )

            self.expression.set(result_text)
            self.display.icursor(tk.END)

        except (ValueError, ArithmeticError) as error:
            messagebox.showerror(
                "Calculation Error",
                str(error),
                parent=self.root,
            )

    def _clear(self):
        self.expression.set("")
        self.display.focus_set()

    def _clear_history(self):
        self.history.clear()
        self.history_list.delete(0, tk.END)

    def _reuse_history(self, event=None):
        selection = self.history_list.curselection()

        if not selection:
            return

        history_item = self.history_list.get(selection[0])

        if " = " in history_item:
            result = history_item.rsplit(" = ", 1)[1]
            self.expression.set(result)
            self.display.icursor(tk.END)
            self.display.focus_set()