import tkinter as tk
import tkinter.font as tkFont


def Task_1_command():
    pass

def Task_2_command():
    pass

def Task_3_command():
    pass

def add_task_command():
    pass

root = tk.Tk()
root.title("Todo - List")
root.configure(bg='#09081C')
width=900
height=600
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)

ddc=tk.Label(root)
ddc["bg"] = "#09081C"
ft = tkFont.Font(family='Times',size=18)
ddc["font"] = ft
ddc["fg"] = "#ffffff"
ddc["justify"] = "center"
ddc["text"] = "Due date complete"
ddc.place(x=0,y=0,width=900,height=50)

Task_1=tk.Button(root)
Task_1["bg"] = "#f0f0f0"
ft = tkFont.Font(family='Times',size=10)
Task_1["font"] = ft
Task_1["fg"] = "#000000"
Task_1["justify"] = "center"
Task_1["text"] = "Button"
Task_1.place(x=90,y=60,width=720,height=60)
Task_1["command"] = Task_1_command

Task_2=tk.Button(root)
Task_2["bg"] = "#f0f0f0"
ft = tkFont.Font(family='Times',size=10)
Task_2["font"] = ft
Task_2["fg"] = "#000000"
Task_2["justify"] = "center"
Task_2["text"] = "Button"
Task_2.place(x=90,y=130,width=720,height=60)
Task_2["command"] = Task_2_command

pend=tk.Label(root)
pend["bg"] = "#09081C"
ft = tkFont.Font(family='Times',size=18)
pend["font"] = ft
pend["fg"] = "#ffffff"
pend["justify"] = "center"
pend["text"] = "Pending"
pend.place(x=0,y=200,width=900,height=50)

Task_3=tk.Button(root)
Task_3["bg"] = "#f0f0f0"
ft = tkFont.Font(family='Times',size=10)
Task_3["font"] = ft
Task_3["fg"] = "#000000"
Task_3["justify"] = "center"
Task_3["text"] = "Button"
Task_3.place(x=90,y=260,width=720,height=60)
Task_3["command"] = Task_3_command

add_task=tk.Button(root)
add_task["bg"] = "#f0f0f0"
ft = tkFont.Font(family='Times',size=98)
add_task["font"] = ft
add_task["fg"] = "#000000"
add_task["justify"] = "center"
add_task["text"] = "+"
add_task.place(x=580,y=380,width=80,height=80)
add_task["command"] = add_task_command

root.mainloop()
