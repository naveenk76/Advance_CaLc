import tkinter as tk

from gui.calculator_window import CalculatorWindow


def main():
    root = tk.Tk()
    CalculatorWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()