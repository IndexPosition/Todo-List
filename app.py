from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import mysql.connector  # pip install mysql-connector-python
import datetime

root = Tk()
root.title("Todo List")


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="12345",
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS todo_2;")
mycursor.execute("USE todo_2;")
mycursor.execute("CREATE TABLE IF NOT EXISTS todo (ID INT AUTO_INCREMENT PRIMARY KEY, task VARCHAR(255), due_date DATE, status TINYINT(1) DEFAULT 0)")

def add_task():
    task = entry.get()
    due_date = due_date_entry.get()
    if task == "":
        messagebox.showerror("Error", "Please enter a task")
    else:
        if not due_date or due_date == "DD-MM-YYYY":
            due_date_str = datetime.date.today().strftime("%Y-%m-%d")
            due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
        else:
            due_date = datetime.datetime.strptime(due_date, '%d-%m-%Y').strftime('%Y-%m-%d')
        mycursor.execute("INSERT INTO todo (task, due_date) VALUES (%s, %s) ", (task, due_date))
        mydb.commit()
        entry.delete(0, END)
        due_date_entry.delete(0, END)
        show_tasks() 


def show_tasks():
    if sort_by_due_date_var.get():
        mycursor.execute("SELECT ID, task, due_date, status FROM todo ORDER BY due_date")
    else:
        mycursor.execute("SELECT ID, task, due_date, status FROM todo")
    tasks = mycursor.fetchall()
    listbox.delete(0, END)
    for task in tasks:
        status = "✔" if task[3] == 1 else "❌"
        listbox.insert(END, f"{task[0]}. [{status}] {task[1]} - Due: {task[2]}")


def delete_task():
    try:
        mycursor.execute("DELETE FROM todo WHERE ID = %s;", (listbox.get(ACTIVE).partition('.')[0],))
        mydb.commit()
        mycursor.execute("ALTER TABLE todo AUTO_INCREMENT = 0;")
        show_tasks()
    except IndexError:
        show_tasks()


def toggle_task():
    try:
        task_id = listbox.get(ACTIVE).partition('.')[0]
        mycursor.execute("UPDATE todo SET status = NOT status WHERE ID = %s;", (task_id,))
        mydb.commit()
        show_tasks()
    except IndexError:
        show_tasks()

def sort_by_due_date_value():
    show_tasks()


width=500
height=460
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)
root.configure(background='#4169e1')

displayfont = "Open Sans"

listbox= Listbox(root)
listbox["borderwidth"] = "1px"
ft = tkFont.Font(family=displayfont,size=12)
listbox["font"] = ft
listbox["fg"] = "#333333"
listbox["justify"] = "left"
listbox.place(x=20,y=20,width=460,height=320)
listbox.bind("<Double-Button-1>", lambda x: toggle_task())

entry = Entry(root)
entry["borderwidth"] = "5px"
ft = tkFont.Font(family=displayfont,size=12)
entry["font"] = ft
entry["fg"] = "#333333"
entry["justify"] = "left"
entry["relief"] = "flat"
entry.place(x=20,y=350,width=350,height=50)

due_date_entry = Entry(root)
due_date_entry["borderwidth"] = "5px"
ft = tkFont.Font(family=displayfont,size=12)
due_date_entry["font"] = ft
due_date_entry["fg"] = "#333333"
due_date_entry["justify"] = "center"
due_date_entry["relief"] = "flat"
due_date_entry.place(x=20,y=410,width=212,height=30)
due_date_entry.insert(END, "DD-MM-YYYY")

delete_button= Button(root)
delete_button["bg"] = "#dc3545"
ft = tkFont.Font(family=displayfont,size=25)
delete_button["font"] = ft
delete_button["fg"] = "#000000"
delete_button["justify"] = "center"
delete_button["anchor"] = "n"
delete_button["text"] = "🗑"
delete_button["relief"] = "flat"
delete_button.place(x=430,y=350,width=50,height=50)
delete_button["command"] = delete_task

add_button= Button(root)
add_button["bg"] = "#5fb878"
ft = tkFont.Font(family=displayfont,size=28)
add_button["font"] = ft
add_button["fg"] = "#000000"
add_button["justify"] = "center"
add_button["text"] = "➕"
add_button["relief"] = "flat"
add_button.place(x=380,y=350,width=50,height=50)
add_button["command"] = add_task

toggle_button= Button(root)
toggle_button["bg"] = "#ffc107"
ft = tkFont.Font(family=displayfont,size=20)
toggle_button["font"] = ft
toggle_button["fg"] = "#000000"
toggle_button["justify"] = "center"
toggle_button["text"] = "Toggle"
toggle_button["relief"] = "flat"
toggle_button.place(x=380,y=400,width=100,height=40)
toggle_button["command"] = toggle_task

sort_by_due_date_var = BooleanVar(value=False)
sort_by_due_date_checkbox= Checkbutton(root)
ft = tkFont.Font(family = displayfont,size=10)
sort_by_due_date_checkbox["font"] = ft
sort_by_due_date_checkbox["fg"] = "white"
sort_by_due_date_checkbox["bg"] = "#4169e1"
sort_by_due_date_checkbox["selectcolor"] = "#4169e1"
sort_by_due_date_checkbox["activebackground"] = "#4169e1"
sort_by_due_date_checkbox["activeforeground"] = "white"
sort_by_due_date_checkbox["justify"] = "center"
sort_by_due_date_checkbox["text"] = "Sort by Due Date"
sort_by_due_date_checkbox["relief"] = "flat"
sort_by_due_date_checkbox.place(x=240,y=410,width=130,height=30)
sort_by_due_date_var = BooleanVar()
sort_by_due_date_checkbox["variable"] = sort_by_due_date_var
sort_by_due_date_checkbox["command"] = sort_by_due_date_value



show_tasks()

root.mainloop()
