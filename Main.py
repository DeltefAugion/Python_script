import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import sys
import os

class PythonNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Notepad")
        self.root.geometry("900x700")
        self.filename = None
      
        self.create_menu_bar()
        
        #  main frame
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
      
        editor_label = tk.Label(main_frame, text="Editor:", font=("Arial", 10, "bold"))
        editor_label.pack(anchor="w")
        
        self.text_editor = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            font=("Courier", 11),
            height=20,
            width=80
        )
        self.text_editor.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
      
        output_label = tk.Label(main_frame, text="Output:", font=("Arial", 10, "bold"))
        output_label.pack(anchor="w")
        
        self.output_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            font=("Courier", 10),
            height=10,
            width=80,
            bg="#f0f0f0"
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # knopf
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        run_button = tk.Button(button_frame, text="▶ Run Code", command=self.run_code, bg="#4CAF50", fg="white", padx=15, pady=8)
        run_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = tk.Button(button_frame, text="Clear Output", command=self.clear_output, bg="#2196F3", fg="white", padx=15, pady=8)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        clear_editor = tk.Button(button_frame, text="Clear Editor", command=self.clear_editor, bg="#FF9800", fg="white", padx=15, pady=8)
        clear_editor.pack(side=tk.LEFT, padx=5)

    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear", command=self.clear_editor)
        
        # Run menu
        run_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Execute Code", command=self.run_code, accelerator="Ctrl+R")
        run_menu.add_command(label="Clear Output", command=self.clear_output)
        
        # tastenkürzel
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-r>", lambda e: self.run_code())

    def new_file(self):
        self.text_editor.delete(1.0, tk.END)
        self.filename = None
        self.root.title("Python Notepad - Untitled")

    def open_file(self):
        self.filename = filedialog.askopenfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if self.filename:
            with open(self.filename, "r") as file:
                content = file.read()
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(1.0, content)
            self.root.title(f"Python Notepad - {os.path.basename(self.filename)}")

    def save_file(self):
        if self.filename:
            with open(self.filename, "w") as file:
                content = self.text_editor.get(1.0, tk.END)
                file.write(content)
            messagebox.showinfo("Success", "File saved successfully!")
        else:
            self.save_as_file()

    def save_as_file(self):
        self.filename = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if self.filename:
            with open(self.filename, "w") as file:
                content = self.text_editor.get(1.0, tk.END)
                file.write(content)
            self.root.title(f"Python Notepad - {os.path.basename(self.filename)}")
            messagebox.showinfo("Success", "File saved successfully!")

    def run_code(self):
        code = self.text_editor.get(1.0, tk.END)
        if not code.strip():
            messagebox.showwarning("Warning", "Please enter some code to run!")
            return
        
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Running code...\n" + "="*50 + "\n")
        
        try:
            # Code laufen
            exec_globals = {}
            exec(code, exec_globals)
            self.output_text.insert(tk.END, "\n✓ Code executed successfully!")
        except Exception as e:
            error_message = f"Error: {type(e).__name__}\n{str(e)}"
            self.output_text.insert(tk.END, error_message)
            self.output_text.config(fg="red")
        
        self.output_text.config(fg="black")

    def clear_output(self):
        self.output_text.delete(1.0, tk.END)

    def clear_editor(self):
        if messagebox.askyesno("Confirm", "Clear all text in editor?"):
            self.text_editor.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PythonNotepad(root)
    root.mainloop()
