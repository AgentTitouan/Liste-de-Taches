import os
import tkinter as tk
from tkinter import PhotoImage

class ToDoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Liste de tâches")
        self.master.configure(bg="grey")
        
        self.tasks = []
        self.current_task_index = tk.IntVar()
        
        self.task_entry = tk.Entry(master, bg="#e0e0e0", bd=2, relief=tk.SOLID, font=("Helvetica", 12))
        self.task_entry.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="ew")
        
        script_dir = os.path.dirname(__file__)
        
        add_icon = PhotoImage(file=os.path.join(script_dir, "add_icon.png"))
        add_icon = add_icon.subsample(10, 10)
        remove_icon = PhotoImage(file=os.path.join(script_dir, "remove_icon.png"))
        remove_icon = remove_icon.subsample(10, 10)
        complete_icon = PhotoImage(file=os.path.join(script_dir, "complete_icon.png"))
        complete_icon = complete_icon.subsample(10, 10)
        
        self.add_button = tk.Button(master, text="Ajouter", command=self.add_task, image=add_icon, compound=tk.LEFT, bg="#4caf50", fg="white", bd=0, relief=tk.FLAT, font=("Helvetica", 12))
        self.add_button.image = add_icon
        self.add_button.grid(row=0, column=1, padx=10, pady=0, sticky="ew")
        
        self.task_listbox = tk.Listbox(master, bg="#e0e0e0", bd=2, relief=tk.SOLID, font=("Helvetica", 12))
        self.task_listbox.grid(row=1, column=0, columnspan=2, padx=(20, 10), pady=10, sticky="nsew")
        self.task_listbox.bind('<<ListboxSelect>>', self.update_button_state)
        
        self.remove_button = tk.Button(master, text="Supprimer", command=self.remove_task, image=remove_icon, compound=tk.LEFT, bg="#f44336", fg="white", bd=0, relief=tk.FLAT, font=("Helvetica", 12))
        self.remove_button.image = remove_icon
        self.remove_button.grid(row=2, column=0, padx=(20, 10), pady=(10, 20), sticky="ew")
        
        self.complete_button = tk.Button(master, text="Tâche Terminée", command=self.complete_task, state=tk.DISABLED, image=complete_icon, compound=tk.LEFT, bg="#2196f3", fg="white", bd=0, relief=tk.FLAT, font=("Helvetica", 12))
        self.complete_button.image = complete_icon
        self.complete_button.grid(row=2, column=1, padx=(10, 20), pady=(10, 20), sticky="ew")
        
        self.navigation_bar = tk.Scale(master, from_=0, to=0, orient=tk.HORIZONTAL, variable=self.current_task_index, command=self.navigate_tasks, bg="#e0e0e0", bd=0, relief=tk.FLAT)
        self.navigation_bar.grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        
        for i in range(2):
            master.columnconfigure(i, weight=1)
            master.rowconfigure(i, weight=1)
        
        self.load_tasks()

        master.protocol("WM_DELETE_WINDOW", self.save_tasks_on_close)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append((task, False))
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
            self.navigation_bar.config(to=len(self.tasks) - 1)
            self.task_listbox.itemconfig(tk.END, bg="#ff474c")
            self.save_tasks()

    def remove_task(self):
        selected_task = self.task_listbox.curselection()
        if selected_task:
            index = selected_task[0]
            del self.tasks[index]
            self.task_listbox.delete(index)
            self.complete_button.config(state=tk.DISABLED)
            self.navigation_bar.config(to=len(self.tasks) - 1)
            self.save_tasks()

    def update_button_state(self, event):
        selected_task = self.task_listbox.curselection()
        if selected_task:
            index = selected_task[0]
            _, completed = self.tasks[index]
            if completed:
                self.complete_button.config(text="Tâche Non Terminée", command=self.undo_task, state=tk.NORMAL)
            else:
                self.complete_button.config(text="Tâche Terminée", command=self.complete_task, state=tk.NORMAL)
        else:
            self.complete_button.config(state=tk.DISABLED)

    def complete_task(self):
        selected_task = self.task_listbox.curselection()
        if selected_task:
            index = selected_task[0]
            task, _ = self.tasks[index]
            self.tasks[index] = (task, True)
            self.task_listbox.itemconfig(index, bg="lightgreen")
            self.complete_button.config(state=tk.DISABLED)
            self.save_tasks()

    def undo_task(self):
        selected_task = self.task_listbox.curselection()
        if selected_task:
            index = selected_task[0]
            task, _ = self.tasks[index]
            self.tasks[index] = (task, False)
            self.task_listbox.itemconfig(index, bg="#ff474c")
            self.complete_button.config(state=tk.DISABLED)
            self.save_tasks()

    def navigate_tasks(self, event=None):
        index = self.current_task_index.get()
        self.task_listbox.selection_clear(0, tk.END)
        self.task_listbox.selection_set(index)
        self.task_listbox.see(index)

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task, completed in self.tasks:
                file.write(f"{task},{completed}\n")

    def load_tasks(self):
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r") as file:
                for line in file:
                    task, completed = line.strip().split(",")
                    self.tasks.append((task, completed == "True"))
                    self.task_listbox.insert(tk.END, task)
                    if completed == "True":
                        index = self.task_listbox.size() - 1
                        self.task_listbox.itemconfig(index, bg="lightgreen")
                    else:
                        index = self.task_listbox.size() - 1
                        self.task_listbox.itemconfig(index, bg="#ff474c")

    def save_tasks_on_close(self):
        self.save_tasks()
        self.master.destroy()

def main():
    root = tk.Tk()
    app = ToDoApp(root)
    
    window_width = 600
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = int((screen_width/2) - (window_width/2))
    y_coordinate = int((screen_height/2) - (window_height/2))
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
    
    root.mainloop()

if __name__ == "__main__":
    main()
