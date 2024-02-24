import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess


def update_input_field(*args):
    selection = glob_pattern.get()
    if selection == "Custom":
        input_dir.config(state="normal")
        input_dir.delete(0, tk.END)
    else:
        input_dir.config(state="disabled")
        input_dir.delete(0, tk.END)
        input_dir.insert(0, selection)


def run_pyamihtmlx():
    input_path = (
        input_dir.get() if glob_pattern.get() == "Custom" else glob_pattern.get()
    )
    command = f'pyamihtmlx IPCC --input "{input_path}" --query "{query.get()}" --output {output_file.get()}'
    if xpath.get():
        command += " --xpath _NOREFS"
    try:
        subprocess.run(command, check=True, shell=True, text=True, capture_output=True)
        messagebox.showinfo("Success", "Command executed successfully")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to execute command. {e.stderr}")


app = tk.Tk()
app.title("PyAMIHTMLX GUI")
app.geometry("500x300")

# Styling
style = ttk.Style(app)
style.theme_use("clam")

# Improve spacing and organization
main_frame = ttk.Frame(app, padding="10 10 10 10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Dropdown for prebuilt glob patterns
patterns = [
    "cleaned_content/wg1/**/html_with_ids.html",
    "cleaned_content/**/html_with_ids.html",
    "Custom",
]
ttk.Label(main_frame, text="Select Pattern:").grid(
    column=0, row=0, sticky=(tk.W), pady=5
)
glob_pattern = tk.StringVar(app)
glob_pattern.set(patterns[0])  # Default value
glob_pattern.trace("w", update_input_field)
dropdown = ttk.Combobox(
    main_frame, textvariable=glob_pattern, values=patterns, state="readonly", width=50
)
dropdown.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=5)

# Custom Input Directory
ttk.Label(main_frame, text="Or Custom Input Directory:").grid(
    column=0, row=1, sticky=tk.W, pady=5
)
input_dir = ttk.Entry(main_frame, state="disabled", width=53)
input_dir.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=5)

# Query Input
ttk.Label(main_frame, text="Query:").grid(column=0, row=2, sticky=tk.W, pady=5)
query = ttk.Entry(main_frame, width=53)
query.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=5)

# Output File Input
ttk.Label(main_frame, text="Output File:").grid(column=0, row=3, sticky=tk.W, pady=5)
output_file = ttk.Entry(main_frame, width=53)
output_file.grid(column=1, row=3, sticky=(tk.W, tk.E), pady=5)

# Additional Flags
ttk.Label(main_frame, text="Additional Flags:").grid(
    column=0, row=4, sticky=tk.W, pady=5
)
xpath = tk.IntVar()
ttk.Checkbutton(
    main_frame, text="Remove References (--xpath _NOREFS)", variable=xpath
).grid(column=1, row=4, sticky=tk.W, pady=5)

# Run Command Button
ttk.Button(main_frame, text="Run Command", command=run_pyamihtmlx).grid(
    column=1, row=5, sticky=tk.E, pady=10
)

# Grid configuration for resizing
for child in main_frame.winfo_children():
    child.grid_configure(padx=5, pady=2)
main_frame.columnconfigure(1, weight=1)

app.mainloop()
