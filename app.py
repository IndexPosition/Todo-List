from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import mysql.connector
import datetime


root = Tk()
root.title("Todo List")


def create_database(cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS todo;")
    cursor.execute("USE todo;")
    cursor.execute("CREATE TABLE IF NOT EXISTS todo (ID INT AUTO_INCREMENT PRIMARY KEY, task VARCHAR(255), due_date DATE, status TINYINT(1) DEFAULT 0)")


def add_task(cursor, db, task_entry, due_date_entry, listbox):
    task = task_entry.get()
    due_date_str = due_date_entry.get()
    if task == "":
        messagebox.showerror("Error", "Please enter a task")
    else:
        try:
            if not due_date_str or due_date_str == "DD-MM-YYYY":
                due_date = datetime.date.today()
            else:
                due_date = datetime.datetime.strptime(due_date_str, "%d-%m-%Y").date()
        except ValueError:
            messagebox.showerror(
                "Error",
                "Invalid date format. Please enter a date in DD-MM-YYYY format.",
            )
            return
        query = "INSERT INTO todo (task, due_date) VALUES (%s, %s)"
        values = (task, due_date)
        cursor.execute(query, values)
        db.commit()
        task_entry.delete(0, END)
        due_date_entry.delete(0, END)
        show_tasks(cursor, listbox, sort_by_due_date_var)


def show_tasks(cursor, listbox, sort_by_due_date_var):
    if sort_by_due_date_var.get():
        query = "SELECT ID, task, due_date, status FROM todo ORDER BY due_date"
    else:
        query = "SELECT ID, task, due_date, status FROM todo"
    cursor.execute(query)
    tasks = cursor.fetchall()
    listbox.delete(0, END)
    for task in tasks:
        status = "✔" if task[3] == 1 else "❌"
        listbox.insert(END, f"{task[0]}. [{status}] {task[1]} - Due: {task[2]}")


def delete_task(cursor, db, listbox):
    try:
        task_id = listbox.get(ACTIVE).partition(".")[0]
        query = "DELETE FROM todo WHERE ID = %s;"
        values = (task_id,)
        cursor.execute(query, values)
        db.commit()
        cursor.execute("ALTER TABLE todo AUTO_INCREMENT = 0;")
        show_tasks(cursor, listbox, sort_by_due_date_var)
    except IndexError:
        show_tasks(cursor, listbox, sort_by_due_date_var)


def toggle_task(cursor, db, listbox):
    try:
        task_id = listbox.get(ACTIVE).partition(".")[0]
        query = "SELECT status FROM todo WHERE ID = %s"
        values = (task_id,)
        cursor.execute(query, values)
        status = cursor.fetchone()[0]
        new_status = 1 - status
        query = "UPDATE todo SET status = %s WHERE ID = %s"
        values = (new_status, task_id)
        cursor.execute(query, values)
        db.commit()
        show_tasks(cursor, listbox, sort_by_due_date_var)
    except IndexError:
        show_tasks(cursor, listbox, sort_by_due_date_var)


def sort_by_due_date_value(cursor, listbox, sort_by_due_date_var):
    show_tasks(cursor, listbox, sort_by_due_date_var)


def main():
    db = mysql.connector.connect(host="localhost", user="root", password="12345")
    cursor = db.cursor()
    create_database(cursor)

    width = 500
    height = 460
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = "%dx%d+%d+%d" % (
        width,
        height,
        (screenwidth - width) / 2,
        (screenheight - height) / 2,
    )
    root.geometry(alignstr)
    root.resizable(width=False, height=False)
    root.configure(background="#4169e1")

    displayfont = "Open Sans"

    listbox = Listbox(root)
    listbox["borderwidth"] = "1px"
    ft = tkFont.Font(family=displayfont, size=12)
    listbox["font"] = ft
    listbox["fg"] = "#333333"
    listbox["justify"] = "left"
    listbox.place(x=20, y=20, width=460, height=320)
    listbox.bind("<Double-Button-1>", lambda x: toggle_task())

    task_entry = Entry(root)
    task_entry["borderwidth"] = "5px"
    ft = tkFont.Font(family=displayfont, size=12)
    task_entry["font"] = ft
    task_entry["fg"] = "#333333"
    task_entry["justify"] = "left"
    task_entry["relief"] = "flat"
    task_entry.place(x=20, y=350, width=350, height=50)

    due_date_entry = Entry(root)
    due_date_entry["borderwidth"] = "5px"
    ft = tkFont.Font(family=displayfont, size=12)
    due_date_entry["font"] = ft
    due_date_entry["fg"] = "#333333"
    due_date_entry["justify"] = "center"
    due_date_entry["relief"] = "flat"
    due_date_entry.place(x=20, y=410, width=212, height=30)
    due_date_entry.insert(END, "DD-MM-YYYY")

    delete_button = Button(root)
    delete_button["bg"] = "#dc3545"
    ft = tkFont.Font(family=displayfont, size=25)
    delete_button["font"] = ft
    delete_button["fg"] = "#000000"
    delete_button["justify"] = "center"
    delete_button["anchor"] = "n"
    delete_button["text"] = "🗑"
    delete_button["relief"] = "flat"
    delete_button.place(x=430, y=350, width=50, height=50)
    delete_button["command"] = lambda: delete_task(cursor, db, listbox)

    add_button = Button(root)
    add_button["bg"] = "#5fb878"
    ft = tkFont.Font(family=displayfont, size=28)
    add_button["font"] = ft
    add_button["fg"] = "#000000"
    add_button["justify"] = "center"
    add_button["text"] = "➕"
    add_button["relief"] = "flat"
    add_button.place(x=380, y=350, width=50, height=50)
    add_button["command"] = lambda: add_task(
        cursor, db, task_entry, due_date_entry, listbox
    )

    toggle_button = Button(root)
    toggle_button["bg"] = "#ffc107"
    ft = tkFont.Font(family=displayfont, size=20)
    toggle_button["font"] = ft
    toggle_button["fg"] = "#000000"
    toggle_button["justify"] = "center"
    toggle_button["text"] = "Toggle"
    toggle_button["relief"] = "flat"
    toggle_button.place(x=380, y=400, width=100, height=40)
    toggle_button["command"] = lambda: toggle_task(cursor, db, listbox)

    global sort_by_due_date_var
    sort_by_due_date_var = BooleanVar(value=False)
    sort_by_due_date_checkbox = Checkbutton(root)
    ft = tkFont.Font(family=displayfont, size=10)
    sort_by_due_date_checkbox["font"] = ft
    sort_by_due_date_checkbox["fg"] = "white"
    sort_by_due_date_checkbox["bg"] = "#4169e1"
    sort_by_due_date_checkbox["selectcolor"] = "#4169e1"
    sort_by_due_date_checkbox["activebackground"] = "#4169e1"
    sort_by_due_date_checkbox["activeforeground"] = "white"
    sort_by_due_date_checkbox["justify"] = "center"
    sort_by_due_date_checkbox["text"] = "Sort by Due Date"
    sort_by_due_date_checkbox["relief"] = "flat"
    sort_by_due_date_checkbox.place(x=240, y=410, width=130, height=30)
    sort_by_due_date_var = BooleanVar()
    sort_by_due_date_checkbox["variable"] = sort_by_due_date_var
    sort_by_due_date_checkbox["command"] = lambda: sort_by_due_date_value(
        cursor, listbox, sort_by_due_date_var
    )
    show_tasks(cursor, listbox, sort_by_due_date_var)
    root.mainloop()


if __name__ == "__main__":
    main()
