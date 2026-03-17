import tkinter as tk
from tkinter import ttk

from screenshot import capture_screen
from ocr import extract_text
from ai import explain_text

import threading


class App:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Screen Explainer")
        self.root.geometry("1200x700")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # окно можно растягивать
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        # верхняя панель
        top = ttk.Frame(self.root)
        top.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        self.capture_btn = ttk.Button(top, text="Capture Screen", command=self.capture)
        self.capture_btn.pack(side="left", padx=5)

        self.explain_btn = ttk.Button(top, text="Explain", command=self.explain)
        self.explain_btn.pack(side="left", padx=5)

        self.lang_var = tk.StringVar(value="RU")

        lang_menu = ttk.Combobox(
            top,
            textvariable=self.lang_var,
            values=["RU", "EN"],
            state="readonly",
            width=5
        )
        lang_menu.pack(side="left", padx=10)

        # основной контейнер
        main = ttk.Frame(self.root)
        main.grid(row=1, column=0, sticky="nsew")

        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        # -------- OCR TEXT --------
        left_frame = ttk.Frame(main)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ttk.Label(left_frame, text="Text from Screen").pack(anchor="w")

        self.text_box = tk.Text(left_frame, wrap="word")
        self.text_box.pack(fill="both", expand=True)

        scrollbar1 = ttk.Scrollbar(left_frame, command=self.text_box.yview)
        scrollbar1.pack(side="right", fill="y")

        self.text_box.config(yscrollcommand=scrollbar1.set)

        # -------- AI EXPLANATION --------
        right_frame = ttk.Frame(main)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ttk.Label(right_frame, text="AI Explanation").pack(anchor="w")

        self.explain_box = tk.Text(right_frame, wrap="word")
        self.explain_box.pack(fill="both", expand=True)

        scrollbar2 = ttk.Scrollbar(right_frame, command=self.explain_box.yview)
        scrollbar2.pack(side="right", fill="y")

        self.explain_box.config(yscrollcommand=scrollbar2.set)

        # -------- STATUS --------
        self.status = ttk.Label(self.root, text="Ready")
        self.status.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.progress = ttk.Progressbar(self.root, mode="indeterminate")
        self.progress.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

    def capture(self):
        self.start_loading("Capturing + OCR...")

        thread = threading.Thread(target=self.run_capture)
        thread.daemon = True
        thread.start()

    def run_capture(self):
        try:
            image = capture_screen()
            text = extract_text(image)
        except Exception as e:
            text = f"Error:\n{str(e)}"

        self.root.after(0, lambda: self.finish_capture(text))

    def finish_capture(self, text):
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", text)

        self.stop_loading()

    def explain(self):
        text = self.text_box.get("1.0", "end").strip()

        if not text:
            self.status.config(text="No text to explain")
            return

        self.start_loading("Generating explanation...")

        lang = self.lang_var.get()

        thread = threading.Thread(
            target=self.run_explain,
            args=(text, lang)
        )

        thread.daemon = True
        thread.start()

    def run_explain(self, text, lang):
        try:
            explanation = explain_text(text, lang)
        except Exception as e:
            explanation = f"Error:\n{str(e)}"

        self.root.after(0, lambda: self.finish_explain(explanation))

    def finish_explain(self, explanation):

        self.explain_box.delete("1.0", "end")
        self.explain_box.insert("1.0", explanation)

        self.stop_loading()

    def start_loading(self, text="Processing..."):
        self.status.config(text=text)
        self.progress.start(10)

        self.capture_btn.config(state="disabled")
        self.explain_btn.config(state="disabled")

    def stop_loading(self):
        self.progress.stop()
        self.status.config(text="Ready")

        self.capture_btn.config(state="normal")
        self.explain_btn.config(state="normal")

    def run(self):

        self.root.mainloop()

    def on_close(self):
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass