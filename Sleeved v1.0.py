import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
import os
import random

SLEEVE_FILE = "sleeves.json"
STATE_FILE = "used_sleeves.json"

class CustomInputDialog(tk.Toplevel):
    def __init__(self, parent, title, prompt):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x120")
        self.resizable(False, False)
        self.value = None

        self.label = tk.Label(self, text=prompt, font=("Helvetica", 12))
        self.label.pack(pady=(10, 5))

        self.entry = tk.Entry(self, font=("Helvetica", 12))
        self.entry.pack(pady=5, padx=10, fill=tk.X)
        self.entry.focus()

        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack(pady=10)

        self.ok_btn = tk.Button(self.btn_frame, text="OK", width=10, command=self.on_ok)
        self.ok_btn.pack(side=tk.LEFT, padx=5)

        self.cancel_btn = tk.Button(self.btn_frame, text="Cancel", width=10, command=self.on_cancel)
        self.cancel_btn.pack(side=tk.LEFT, padx=5)

        self.bind("<Return>", lambda event: self.on_ok())
        self.bind("<Escape>", lambda event: self.on_cancel())

        self.transient(parent)
        self.grab_set()

        self.center_window(parent)

        self.wait_window()

    def center_window(self, parent):
        self.update_idletasks()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        width = self.winfo_width()
        height = self.winfo_height()

        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

    def on_ok(self):
        self.value = self.entry.get().strip()
        self.destroy()

    def on_cancel(self):
        self.value = None
        self.destroy()

def load_sleeves():
    if os.path.exists(SLEEVE_FILE):
        try:
            with open(SLEEVE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_sleeves(sleeves):
    with open(SLEEVE_FILE, "w") as f:
        json.dump(sleeves, f)

def load_used():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_used(used):
    with open(STATE_FILE, "w") as f:
        json.dump(used, f)

class SleevePickerApp:
    def __init__(self, master):
        self.master = master
        master.title("Sleeved V1.0")
        master.configure(bg="black")

        self.sleeves = load_sleeves()
        self.used = load_used()

        label_style = {"bg": "black", "fg": "white", "font": ("Helvetica", 12)}
        label_bold_style = {"bg": "black", "fg": "white", "font": ("Helvetica", 12, "bold")}
        title_style = {"bg": "black", "fg": "white", "font": ("Helvetica", 16, "bold")}

        self.title = tk.Label(master, text="🎲 Sleeved", **title_style)
        self.title.pack(pady=10)

        self.chosen_frame = tk.Frame(master, bg="black")
        self.chosen_frame.pack(pady=5)

        self.chosen_text_label = tk.Label(self.chosen_frame, text="Picked Sleeve:",
                                          bg="black", fg="white", font=("Helvetica", 14, "bold"))
        self.chosen_text_label.pack(side=tk.LEFT)

        self.left_heart_label = tk.Label(self.chosen_frame, text="💖", bg="black", fg="#FF69B4",
                                         font=("Courier New", 14, "bold"), padx=0, pady=0)
        self.left_heart_label.pack(side=tk.LEFT)

        self.chosen_label = tk.Label(self.chosen_frame, text="—",
                                     bg="black", fg="#FF69B4", font=("Courier New", 14, "bold"),
                                     padx=0, pady=0)
        self.chosen_label.pack(side=tk.LEFT)

        self.right_heart_label = tk.Label(self.chosen_frame, text="💖", bg="black", fg="#FF69B4",
                                          font=("Courier New", 14, "bold"), padx=0, pady=0)
        self.right_heart_label.pack(side=tk.LEFT)

        button_width = 18

        self.pick_button = tk.Button(master, text="Pick Random Sleeve", command=self.pick_sleeve,
                                     bg="#1e90ff", fg="white", font=("Helvetica", 12), width=button_width)
        self.pick_button.pack(pady=5)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_used,
                                      bg="#ff4500", fg="white", font=("Helvetica", 12), width=button_width)
        self.reset_button.pack(pady=5)

        self.add_button = tk.Button(master, text="➕ Add Sleeve", command=self.add_sleeve,
                                    bg="#32cd32", fg="white", font=("Helvetica", 12), width=button_width)
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(master, text="➖ Remove Sleeve", command=self.remove_sleeve,
                                       bg="#dc143c", fg="white", font=("Helvetica", 12), width=button_width)
        self.remove_button.pack(pady=5)

        self.instructions_button = tk.Button(master, text="Instructions", command=self.show_instructions,
                                             bg="#555555", fg="white", font=("Helvetica", 12), width=button_width)
        self.instructions_button.pack(pady=5)

        self.used_label = tk.Label(master, text="📝 Previously picked:", **label_bold_style)
        self.used_label.pack()
        self.used_text = scrolledtext.ScrolledText(master, height=10, width=45, wrap=tk.WORD,
                                                   bg="#121212", fg="white", insertbackground="white")
        self.used_text.pack(pady=5)

        self.remaining_label = tk.Label(master, text="⏳ Still in rotation:", **label_bold_style)
        self.remaining_label.pack()
        self.remaining_text = scrolledtext.ScrolledText(master, height=10, width=45, wrap=tk.WORD,
                                                        bg="#121212", fg="white", insertbackground="white")
        self.remaining_text.pack(pady=5)

        # Footer message at the bottom - font size bumped to 11 for better readability
        self.footer_label = tk.Label(master,
                                     text="Fleshcrack is real!!! Created with ChatGPT by Hot-Slice-3217",
                                     bg="black", fg="grey",
                                     font=("Helvetica", 11, "italic"))
        self.footer_label.pack(pady=(10, 5))

        self.flashing = False
        self.flash_on = True
        self.flash_job = None

        self.update_display("")

    def show_instructions(self):
        instructions = (
            "How to use Sleeved:\n\n"
            "• Use 'Pick Random Sleeve' to select a sleeve randomly.\n"
            "• 'Reset' clears the list of previously picked sleeves.\n"
            "• 'Add Sleeve' lets you add new sleeve names to your collection.\n"
            "• 'Remove Sleeve' deletes a sleeve from your collection.\n\n"
            "Sleeves you pick won't repeat until all have been used.\n"
            "Enjoy!"
        )
        messagebox.showinfo("Instructions", instructions)

    def flash_label(self):
        fg_color_on = "#FF69B4"
        fg_color_off = "black"

        if self.flash_on:
            self.left_heart_label.config(fg=fg_color_on)
            self.right_heart_label.config(fg=fg_color_on)
        else:
            self.left_heart_label.config(fg=fg_color_off)
            self.right_heart_label.config(fg=fg_color_off)

        self.flash_on = not self.flash_on
        self.flash_job = self.master.after(500, self.flash_label)

    def stop_flashing(self):
        if self.flash_job:
            self.master.after_cancel(self.flash_job)
            self.flash_job = None
        self.left_heart_label.config(fg="black")
        self.right_heart_label.config(fg="black")
        self.flashing = False

    def pick_sleeve(self):
        if not self.sleeves:
            messagebox.showwarning("No Sleeves", "Your sleeve list is empty! Please add sleeves first.")
            return

        available = [s for s in self.sleeves if s not in self.used]
        if not available:
            messagebox.showinfo("Info", "✅ All sleeves have been picked! Resetting the list.")
            self.used = []
            available = self.sleeves.copy()
        chosen = random.choice(available)
        self.used.append(chosen)
        save_used(self.used)
        self.update_display(chosen)

    def reset_used(self):
        if messagebox.askyesno("Reset", "Are you sure you want to reset the previously picked list?"):
            self.used = []
            save_used(self.used)
            self.update_display("")

    def add_sleeve(self):
        dlg = CustomInputDialog(self.master, "Add Sleeve", "Enter the name of the sleeve you want to add:")
        new_sleeve = dlg.value
        if new_sleeve:
            if new_sleeve in self.sleeves:
                messagebox.showwarning("Duplicate", "That sleeve already exists.")
            else:
                self.sleeves.append(new_sleeve)
                save_sleeves(self.sleeves)
                messagebox.showinfo("Added", f"'{new_sleeve}' has been added.")
                self.update_display("")

    def remove_sleeve(self):
        dlg = CustomInputDialog(self.master, "Remove Sleeve", "Enter the name of the sleeve you want to remove:")
        rem_sleeve = dlg.value
        if rem_sleeve:
            if rem_sleeve not in self.sleeves:
                messagebox.showwarning("Not found", "That sleeve is not in the list.")
            else:
                self.sleeves.remove(rem_sleeve)
                if rem_sleeve in self.used:
                    self.used.remove(rem_sleeve)
                save_sleeves(self.sleeves)
                save_used(self.used)
                messagebox.showinfo("Removed", f"'{rem_sleeve}' has been removed.")
                self.update_display("")

    def update_display(self, chosen):
        if chosen:
            self.chosen_label.config(text=chosen)
            if not self.flashing:
                self.flashing = True
                self.flash_on = True
                self.flash_label()
        else:
            self.chosen_label.config(text="—")
            self.stop_flashing()

        self.used_text.delete("1.0", tk.END)
        for s in self.used:
            self.used_text.insert(tk.END, f"• {s}\n")

        self.remaining_text.delete("1.0", tk.END)
        remaining = [s for s in self.sleeves if s not in self.used]
        for s in remaining:
            self.remaining_text.insert(tk.END, f"• {s}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = SleevePickerApp(root)
    root.mainloop()
