import tkinter as tk
from tkinter import END
from comments_generation_wordnet_rulebased import translate_chat

BG_COLOR = "#F4F7FB"
HEADER_BG = "#1E5F74"
INPUT_BG = "#EAF3F8"
BUTTON_BG = "#29AB87"
BUTTON_TEXT = "#FFFFFF"
TEXT_COLOR = "#1F2933"
ACCENT_COLOR = "#29AB87"

FONT = ("Helvetica", 12)
FONT_BOLD = ("Helvetica", 12, "bold")


class CustomText(tk.Text):
    """Text widget with a simple highlight helper."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def highlight_pattern(self, pattern, tag, start="1.0", end="end", regexp=False):
        start_index = self.index(start)
        end_index = self.index(end)
        self.mark_set("matchStart", start_index)
        self.mark_set("matchEnd", start_index)
        self.mark_set("searchLimit", end_index)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd", "searchLimit", count=count, regexp=regexp)
            if index == "":
                break
            if count.get() == 0:
                break
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", f"{index}+{count.get()}c")
            self.tag_add(tag, "matchStart", "matchEnd")


class ChatApplication:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Eskom Automated Response")
        self.window.geometry("520x620")
        self.window.configure(bg=BG_COLOR)
        self.window.minsize(420, 520)
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        header = tk.Label(
            self.window,
            bg=HEADER_BG,
            fg=BUTTON_TEXT,
            text="Eskom Automated Response",
            font=FONT_BOLD,
            pady=12,
        )
        header.pack(fill="x")

        self.text_widget = CustomText(
            self.window,
            wrap="word",
            bg="#FFFFFF",
            fg=TEXT_COLOR,
            font=FONT,
            padx=10,
            pady=10,
            spacing1=6,
            spacing2=4,
            spacing3=6,
        )
        self.text_widget.pack(fill="both", expand=True, padx=10, pady=(10, 0))
        self.text_widget.configure(cursor="arrow", state="disabled")
        self.text_widget.tag_configure("user_tag", foreground=ACCENT_COLOR, font=FONT_BOLD)
        self.text_widget.tag_configure("bot_tag", foreground="#1E5F74", font=FONT_BOLD)

        scrollbar = tk.Scrollbar(self.text_widget, orient="vertical", command=self.text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_widget.configure(yscrollcommand=scrollbar.set)

        bottom_frame = tk.Frame(self.window, bg=BG_COLOR, padx=10, pady=10)
        bottom_frame.pack(fill="x")

        self.msg_entry = tk.Entry(
            bottom_frame,
            bg=INPUT_BG,
            fg=TEXT_COLOR,
            font=FONT,
            insertbackground=TEXT_COLOR,
        )
        self.msg_entry.pack(side="left", fill="x", expand=True, ipady=8)
        self.msg_entry.focus_set()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        send_button = tk.Button(
            bottom_frame,
            text="Send",
            font=FONT_BOLD,
            bg=BUTTON_BG,
            fg=BUTTON_TEXT,
            activebackground="#1C9C7A",
            activeforeground=BUTTON_TEXT,
            width=12,
            command=lambda: self._on_enter_pressed(None),
        )
        send_button.pack(side="left", padx=(10, 0), ipady=8)

        clear_button = tk.Button(
            bottom_frame,
            text="Clear",
            font=FONT_BOLD,
            bg="#D9E2EC",
            fg=TEXT_COLOR,
            activebackground="#C9D5E3",
            activeforeground=TEXT_COLOR,
            width=10,
            command=self._clear_chat,
        )
        clear_button.pack(side="right", ipady=8)

        self._show_welcome_message()

    def _show_welcome_message(self):
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", "Eskom-Responder: Hello! Type a message about loadshedding, outages, power, or billing and I will respond.\n\n", "bot_tag")
        self.text_widget.configure(state="disabled")
        self.text_widget.see("end")

    def _clear_chat(self):
        self.text_widget.configure(state="normal")
        self.text_widget.delete("1.0", "end")
        self.text_widget.configure(state="disabled")
        self._show_welcome_message()

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get().strip()
        self._insert_message(msg, "You")

    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.msg_entry.delete(0, END)

        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", f"{sender}: {msg}\n\n", "user_tag")

        response = translate_chat(msg)
        self.text_widget.insert("end", f"Eskom-Responder: {response}\n\n", "bot_tag")
        self.text_widget.configure(state="disabled")
        self.text_widget.see("end")


if __name__ == "__main__":
    app = ChatApplication()
    app.run()