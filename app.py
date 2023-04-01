from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import mysql.connector #pip install mysql-connector-python


root = Tk() 
root.title("Todo List") 


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "12345",
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS todo;")
mycursor.execute("USE todo;")
mycursor.execute("CREATE TABLE IF NOT EXISTS todo (ID INT AUTO_INCREMENT PRIMARY KEY, task VARCHAR(255))")


def add_task():
    task = entry.get()
    if task == "":
        messagebox.showerror("Error","Please enter a task")
    else:
        mycursor.execute("INSERT INTO todo (task) VALUES (%s) ",(task,))
        mydb.commit()
        entry.delete(0,END)
        show_tasks()

def show_tasks():
    mycursor.execute("SELECT ID, task FROM todo")
    tasks = mycursor.fetchall()
    listbox.delete(0,END)
    for task in tasks:
        listbox.insert(END,f"{task[0]}. {task[1]}")

def delete_task():
    try:
        tasks = mycursor.fetchall()
        mycursor.execute("DELETE FROM todo WHERE ID = %s;",(listbox.get(ACTIVE).partition('.')[0],))
        mydb.commit()
        mycursor.execute("ALTER TABLE todo AUTO_INCREMENT = 0;")
        show_tasks()
    except IndexError:
        show_tasks()


width=350
height=500
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)
root.configure(background='black')

mainfont = "Tekton Pro"

add_button=Button(root)
add_button["activebackground"] = "#5fb878"
add_button["activeforeground"] = "#5fb878"
add_button["anchor"] = "center"
add_button["bg"] = "#5fb878"
ft = tkFont.Font(family = mainfont,size = 28)
add_button["font"] = ft
add_button["fg"] = "black"
add_button["justify"] = "center"
add_button["text"] = "➕"
add_button["relief"] = "flat"
add_button.place(x=250,y=0,width=50,height=50)
add_button["command"] = add_task

entry = Entry(root)
entry["bg"] = "#a9e2f9"
entry["borderwidth"] = "5px"
ft = tkFont.Font(family = mainfont,size = 18)
entry["font"] = ft
entry["fg"] = "#333333"
entry["justify"] = "left"
entry["relief"] = "flat"
entry.place(x=0,y=0,width=250,height=50)

delete_button=Button(root)
delete_button["anchor"] = "center"
delete_button["bg"] = "#ff0000"
ft = tkFont.Font(family = mainfont,size = 28)
delete_button["font"] = ft
delete_button["fg"] = "#000000"
delete_button["justify"] = "center"
delete_button["text"] = "🗑"
delete_button["relief"] = "flat"
delete_button.place(x=300,y=0,width=50,height=50)
delete_button["command"] = delete_task

listbox=Listbox(root)
listbox["bg"] = "#09081C"
ft = tkFont.Font(family = mainfont,size = 20)
listbox["font"] = ft
listbox["fg"] = "white"
listbox["justify"] = "left"
listbox["relief"] = "flat"
listbox.place(x=1,y=50,width=349,height=450)
listbox["selectbackground"] = "#1e9fff"


show_tasks()
root.mainloop()
