import subprocess
import os
import tkinter as tk
from tkinter import messagebox, ttk

def get_command_type(cmd):
    result = subprocess.run(['bash', '-c', f'type {cmd}'], capture_output=True, text=True)
    if result.returncode != 0:
        return None, None
    output = result.stdout.strip()
    cmd_type = None
    location = None

    if "is a shell builtin" in output:
        cmd_type = "Shell Built-in"
    elif "is an alias" in output:
        cmd_type = "Alias"
    elif "is a function" in output:
        cmd_type = "Shell Function"
    elif "is a keyword" in output:
        cmd_type = "Shell Keyword"
    elif "is" in output and "/" in output:
        cmd_type = "External Command"
        location = output.split(" is ")[-1]
    return cmd_type, location

def is_executable(path):
    return os.access(path, os.X_OK)

def detect_language(path):
    try:
        real_path = os.path.realpath(path)
        result = subprocess.run(["file", real_path], capture_output=True, text=True)
        desc = result.stdout.lower()

        if "python script" in desc:
            return "Python"
        elif "perl script" in desc:
            return "Perl"
        elif "ruby script" in desc:
            return "Ruby"
        elif "shell script" in desc or "bash script" in desc:
            return "Bash"
        elif "javascript" in desc:
            return "JavaScript"
        elif "php script" in desc:
            return "PHP"
        elif "ascii text" in desc and ".py" in real_path:
            return "Python (by extension)"
        elif "elf" in desc:
            return "Compiled Binary (C/C++/Go)"
        else:
            return "Unknown"
    except:
        return "Unknown"

def inspect_command():
    cmd = entry.get().strip()
    if not cmd:
        messagebox.showerror("Error", "Please enter a command.")
        return

    cmd_type, location = get_command_type(cmd)
    if not cmd_type:
        messagebox.showerror("Not Found", f"Command '{cmd}' not found.")
        return

    type_var.set(cmd_type)
    location_var.set(location if location else "N/A")

    if location and os.path.isfile(location):
        exec_var.set("Yes" if is_executable(location) else "No")
        lang_var.set(detect_language(location))
    else:
        exec_var.set("Not a file")
        lang_var.set("N/A")

# --- GUI Code ---
root = tk.Tk()
root.title("🔧 Kali Command Inspector")
root.geometry("500x300")
root.resizable(False, False)

style = ttk.Style()
style.configure("TLabel", font=("Consolas", 11))
style.configure("TButton", font=("Consolas", 11))

tk.Label(root, text="Enter Command:", font=("Consolas", 12, "bold")).pack(pady=10)
entry = tk.Entry(root, font=("Consolas", 12), width=30)
entry.pack()

tk.Button(root, text="Check Command", command=inspect_command).pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

type_var = tk.StringVar()
location_var = tk.StringVar()
exec_var = tk.StringVar()
lang_var = tk.StringVar()

labels = [
    ("📌 Type", type_var),
    ("📍 Location", location_var),
    ("⚙ Executable", exec_var),
    ("🧠 Language", lang_var)
]

for text, var in labels:
    ttk.Label(frame, text=text + ":", width=12).grid(sticky="w", row=labels.index((text, var)), column=0, padx=5, pady=4)
    ttk.Label(frame, textvariable=var, width=45, anchor="w").grid(row=labels.index((text, var)), column=1, padx=5, pady=4)

root.mainloop()
