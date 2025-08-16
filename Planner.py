
import tkinter as tk
from tkinter import simpledialog, messagebox
import json
from datetime import datetime, timedelta

DATA_FILE = "planner_full.json" #where file is stored

class NoteBookPlannerGUI:

    def start(self, root):

        self.root = root
        self.root.title("Notebook Planner")
        self.root.geometry("900x600") #size
        self.root.configure(bg ="#F0EDDC") #color shade
    
        self.data = self.load_data()
        self.current_date = datetime.now().strftime("%m/%d/%Y") # for date thats going to be on top
        self.ensure_date(self.current_date)

        self.add_queue = []
        self.undo_stack = []
        self.create_widgets()
        self.update_display()

    
    def load_data(self):

        try:

            with open(DATA_FILE, "r") as f:

                return json.load(f)
            
        except FileNotFoundError:

            return {}
        
    def save_data(self):

        with open(DATA_FILE, "w") as f:

            json.dump(self.data, f, indent = 1)

    def ensure_date(self, date):

        if date not in self.data:

            self.data[date] = {"notes": [], "tasks": [], "goals":[], "mood": 0} # notes, tasks, goals, moods for pop up window

    
    #UI for planner
    def create_widgets(self):

        #naviagation help
        nav_frame = tk.Frame(self.root, bg ="#f8f5e1")
        nav_frame.pack(pady = 10)

        tk.Button(nav_frame, text = "⬅️ Prev", font = ("Arial", 12), command = self.prev_day).pack(side = "left", padx = 5)
        
        self.date_label = tk.Label(nav_frame, text = "", font = ("Arial", 16, "bold"), bg = "#F2EFDF") #color shade
        self.date_label.pack(side = "left", padx = 10)
        tk.Button(nav_frame, text = "Next ➡️", font = ("Arial", 12), command = self.next_day).pack(side = "left", padx = 5)

       #main work

        main_frame = tk.Frame(self.root, bg = "#f8f5e1")
        main_frame.pack(fill = "both", expand = True, padx = 20, pady = 10)

        #notes 

        self.notes_canvas = self.create_ruled_section(main_frame, "Notes", 0, 0, "#fff8dc") #color shade
        self.notes_list = self.create_listbox_with_buttons(self.notes_canvas, self.add_note, section = "notes")


        self.tasks_canvas = self.create_ruled_section(main_frame, "Tasks", 0, 1, "#e0f7fa") #color shade
        self.tasks_list = self.create_listbox_with_buttons(self.tasks_canvas, self.add_task, self.complete_task, section = "tasks")

        self.goals_canvas = self.create_ruled_section(main_frame, "Goals", 1, 1, "#ffe0e0") #color shade
        self.goals_list = self.create_listbox_with_buttons(self.goals_canvas, self.add_goal, self.complete_goal, section = "goals")

        main_frame.grid_columnconfigure(0, weight = 1, uniform = "col")
        main_frame.grid_columnconfigure(1, weight = 1, uniform = "col")
        main_frame.grid_columnconfigure(0, weight = 1, uniform = "row")
        main_frame.grid_columnconfigure(1, weight = 1, uniform = "row")


    def create_ruled_section(self, parent,  title, row, col, color):

        frame = tk.Frame(parent, bg = color, bd= 2, relief = "flat")
        frame.grid(row = row, column = col, padx = 5, pady = 5, sticky = "ew")

        label = tk.Label(frame, text = title, font = ("Arial", 14, "bold"), bg = color)
        label.pack(pady = 5)

        return frame
    
    def create_listbox_with_buttons(self, parent_frame, add_cmd, complete_cmd = None, section = None):

        listbox = tk.Listbox(parent_frame, height = 12, width = 40, font = ("Arial", 11))
        listbox.pack(padx = 5, pady = 5, fill = "both", expand = True)

        listbox.bind("<Double-1>" , lambda e, lb = listbox, sec= section: self.edit_or_toggle(lb, sec))

        btn_frame = tk.Frame(parent_frame, bg = parent_frame["bg"])
        btn_frame.pack(pady = 5)

        tk.Button(btn_frame, text = "Add", command = add_cmd).pack(side = "left", padx = 3)

        if complete_cmd:

            tk.Button(btn_frame, text = "Complete", command = complete_cmd).pack(side = "left", padx = 3)
        
        tk.Button(btn_frame, text = "Delete", command = lambda lb = listbox, sec = section: self.delete_item(lb, sec)).pack(side = "left", padx = 3)
        tk.Button(btn_frame, text = "Undo", command = self.undo).pack(side = "left", padx = 3)
       

        return listbox
    

 
    #display the results
    def update_display(self):

        self.date_label.config(text = self.current_date)
        self.ensure_date(self.current_date)

        self.notes_list.delete(0, tk.END)
        
        for note in self.data[self.current_date]["notes"]:

            self.notes_list.insert(tk.END, note)

        self.tasks_list.delete(0, tk.END)
        
        for t in self.data[self.current_date]["tasks"]:

            status = "✓" if t["done"] else "x"
            self.tasks_list.insert(tk.END, "{} {}". format(t["task"], status))
        
        self.goals_list.delete(0, tk.END)

        for g in self.data[self.current_date]["goals"]:

            status = "✓" if g["completed"] else "x"
            self.goals_list.insert(tk.END, g["goal"] + " " + status) 

    
    #adding items

    def add_note(self):

        note = simpledialog.askstring("Add Note", "Enter note:")

        if note:
            self.data[self.current_date]["notes"].append(note)
            self.save_data()
            self.update_display()

    def add_task(self):

        task = simpledialog.askstring("Add Task", "Enter the task: ")

        if task:

            self.data[self.current_date]["tasks"].append({"task": task, "done" : False})
            self.queue_item("tasks" , task)
            self.save_data()
            self.update_display()

    
    def add_goal(self):

        goal = simpledialog.askstring("Add Goal", "Enter the goal: ")

        if goal:

            self.data[self.current_date]["goals"].append({"goal": goal, "completed" : False})
            self.queue_item("goals" , goal)
            self.save_data()
            self.update_display()

    
    def complete_task(self):

        selection = self.tasks_list.curselection()
        
        if selection:

            index = selection[0]
            self.data[self.current_date]["tasks"][index]["done"] = True
            self.save_data()
            self.update_display()


    def complete_goal(self):

        selection = self.goals_list.curselection()
        
        if selection:

            index = selection[0]
            self.data[self.current_date]["goals"][index]["completed"]= True 
            self.save_data()
            self.update_display()

     #edit option
    def edit_or_toggle(self, listbox, section):

        selection = listbox.curselection()
        
        if not selection:

            return
        
        index = selection [0]

        if section in ["tasks", "goals"]:

            action = simpledialog.askstring("Edit / Toggle / Delete ", "Type 't' to toggle ✓/x, 'd' to delete the text, 'e' to edit the text: " )

        else: 
            action = "e"

        if action and action.lower() == "t":

            if section == "tasks" :

                self.data[self.current_date]["tasks"][index]["done"] = not self.data[self.current_date]["tasks"][index]["done"]
            
            else:

                self.data[self.current_date]["goals"][index]["completed"] = not self.data[self.current_date]["goals"][index]["completed"]
         
            self.save_data()
            self.update_display()
            return
            

        elif action and action.lower() == "e":

            current_text = (self.data[self.current_date]["tasks"][index]["task"]
                            
                            if section == "tasks"
                            else self.data[self.current_date]["goals"][index]["goal"]
            )


            new_text = simpledialog.askstring("Edit", "Edit " + section + ":", initialvalue = current_text )

            if new_text:

                if section == "tasks":

                    self.data[self.current_date]["tasks"][index]["task"] = new_text
                
                else:

                    self.data[self.current_date]["goals"][index]["goal"] = new_text
                
                self.save_data()
                self.update_display()
                return
            
        if section == "notes":

                current_text = listbox.get(index)
                
                new_text = simpledialog.askstring("Edit Note", "Update notes: " , initialvalue = current_text)

                if new_text:

                    self.data[self.current_date]["notes"][index] = new_text
                    self.save_data()
                    self.update_display()

        if action == "d":
            self.data[self.current_date][section].pop(index)
            self.save_data()
            self.update_display()
            return

    #delete option
    def delete_item(self, listbox, section):

        selection = listbox.curselection()

        if not selection:
            return
        
        index = selection[0]
        removed = self.data[self.current_date][section].pop(index)
        self.undo_stack.append((section, index, removed))
        self.save_data()
        self.update_display()

    #queue 
    def queue_item(self, section, item):

        self.add_queue.append((section, item))

    def queue_item(self, section, item):

        self.add_queue.append((section, item))
        queue_str = ""
        for sec, item in self.add_queue:
            queue_str += sec + ": " +item + "\n"
        
        tk.messagebox.showinfo("Queue", "Queue: \n" + queue_str)

    #undo option

    def undo(self):

        if not self.undo_stack:

            return
        section, index, removed_item = self.undo_stack.pop()
        self.data[self.current_date][section].insert(index, removed_item)
        self.save_data()
        self.update_display()

    


    # calendar date

    def next_day(self):

            self.current_date = (datetime.strptime(self.current_date, "%m/%d/%Y") + timedelta(days = 1)).strftime("%m/%d/%Y")
            self.update_display()

    def prev_day(self):

            self.current_date = (datetime.strptime(self.current_date, "%m/%d/%Y") - timedelta(days = 1)).strftime("%m/%d/%Y")
            self.update_display()


#run the code
def run_planner():

    root = tk.Tk()
    app = NoteBookPlannerGUI()
    app.start(root)
    root.mainloop()

run_planner()