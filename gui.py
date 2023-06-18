from dfa import *
import tkinter as tk
from tkinter import font as tkFont
from PIL import ImageTk, Image
import timeit
import itertools
import pydot

root = tk.Tk()

k = 2
to_print = False
image_ratio = 1

guess = dfa(0,0)



accepted_strings = [] #test

accepted_frame = tk.Frame(root)
accepted_frame.grid(row=0, column=0, padx=10, pady=10)

accepted_title_label = tk.Label(accepted_frame, text="Accepted Strings")
accepted_title_label.pack()

accepted_scrollbar = tk.Scrollbar(accepted_frame)
accepted_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

accepted_listbox = tk.Listbox(accepted_frame, yscrollcommand=accepted_scrollbar.set)
accepted_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

accepted_scrollbar.config(command=accepted_listbox.yview)

def add_accepted_string(string):
    accepted_strings.append(string)
    if string == "":
        accepted_listbox.insert(tk.END, "eps")
    else:
        accepted_listbox.insert(tk.END, accepted_strings[-1])
   
   
        
rejected_strings = [] #test

rejected_frame = tk.Frame(root)
rejected_frame.grid(row=0, column=1, padx=10, pady=10)

rejected_title_label = tk.Label(rejected_frame, text="Rejected Strings")
rejected_title_label.pack()

rejected_scrollbar = tk.Scrollbar(rejected_frame)
rejected_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

rejected_listbox = tk.Listbox(rejected_frame, yscrollcommand=rejected_scrollbar.set)
rejected_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

rejected_scrollbar.config(command=rejected_listbox.yview)

def add_rejected_string(string):
    rejected_strings.append(string)
    if string == "":
        rejected_listbox.insert(tk.END, "eps")
    else:
        rejected_listbox.insert(tk.END, rejected_strings[-1])
        
        
def clear_accepted_text(event):
    current_text = accept_input.get()
    if current_text == accept_text:
        accept_input.delete(0, tk.END)
        
def restore_accepted_text(event):
    current_text = accept_input.get()
    if current_text == "":
        accept_input.insert(0, accept_text)

def accept_string():
    string = accept_input.get()
    if string == accept_text or guess.known_string(string):
        return
    guess.add_string(1, string)
    add_accepted_string(string)
    accept_input.delete(0, tk.END)
    update_dfa_image()
    
    
accept_input_frame = tk.Frame(root)
accept_input_frame.grid(row=1, column=0, padx=10, pady=10)
  
accept_text = "String to accept"
accept_input = tk.Entry(accept_input_frame)
accept_input.insert(0, accept_text)
accept_input.bind("<FocusIn>", clear_accepted_text)
accept_input.bind("<FocusOut>", restore_accepted_text)
accept_input.grid(row=0, column=0)

accept_button = tk.Button(accept_input_frame, text="Accept string", command=accept_string)
accept_button.grid(row=1, column=0)


def clear_rejected_text(event):
    current_text = reject_input.get()
    if current_text == reject_text:
        reject_input.delete(0, tk.END)
        
def restore_rejected_text(event):
    current_text = reject_input.get()
    if current_text == "":
        reject_input.insert(0, reject_text)
        
def reject_string():
    string = reject_input.get()
    if string == reject_text or guess.known_string(string):
        return
    guess.add_string(0, string)
    add_rejected_string(string)
    reject_input.delete(0, tk.END)
    update_dfa_image()
        

rejected_input_frame = tk.Frame(root)
rejected_input_frame.grid(row=1, column=1, padx=10, pady=10)

reject_input = tk.Entry(rejected_input_frame)
reject_input.grid(row=0, column=1)

reject_text = "String to reject"
reject_input = tk.Entry(rejected_input_frame)
reject_input.insert(0, reject_text)
reject_input.bind("<FocusIn>", clear_rejected_text)
reject_input.bind("<FocusOut>", restore_rejected_text)
reject_input.grid(row=0, column=1)

reject_button = tk.Button(rejected_input_frame, text="Reject string", command=reject_string)
reject_button.grid(row=1, column=1)

num_processed_dfa_label = tk.Label(root, text="Number of Dfa's processed: " + str(guess.count))
num_processed_dfa_label.grid(row=2, column=0, padx=10, pady=10)

num_final_dfa_label = tk.Label(root, text="Number of guesses: " + str(guess.count_final))
num_final_dfa_label.grid(row=3, column=0, padx=10, pady=10)


curr_image = 0

image_path = "out" + str(guess.count_final-1) + ".png"
image = Image.open(image_path)
image = image.resize((round(image.width*image_ratio), round(image.height*image_ratio)))
tk_image = ImageTk.PhotoImage(image)

image_box = tk.Canvas(root, width=image.width, height=image.height, bg="white")
image_box.grid(row=0, column=2, rowspan=2)
image_box.create_image(0, 0, image=tk_image, anchor="nw")


def update_dfa_image():
    global curr_image
    curr_image = guess.count_final-1
    
    
    image_path = "out" + str(guess.count_final-1) + ".png"
    image = Image.open(image_path)
    image = image.resize((round(image.width*image_ratio), round(image.height*image_ratio)))
    tk_image = ImageTk.PhotoImage(image)
    
    global image_box
    image_box.configure(width=image.width, height=image.height)
    image_box.create_image(0, 0, image=tk_image, anchor="nw")
    image_box.image = tk_image
    
    global image_label
    image_label.configure(text=image_path)
    
    global num_processed_dfa_label
    num_processed_dfa_label.configure(text="Number of Dfa's processed: " + str(guess.count))
    
    global num_final_dfa_label
    num_final_dfa_label.configure(text="Number of guesses: " + str(guess.count_final))
    
    root.update_idletasks()
    root.geometry('{}x{}'.format(root.winfo_reqwidth(), root.winfo_reqheight()))

def next_dfa_image():
    global curr_image
    curr_image += 1
    curr_image = curr_image % guess.count_final
    image_path = "out" + str(curr_image) + ".png"
    image = Image.open(image_path)
    image = image.resize((round(image.width*image_ratio), round(image.height*image_ratio)))
    tk_image = ImageTk.PhotoImage(image)
    
    global image_box
    image_box.configure(width=image.width, height=image.height)
    image_box.create_image(0, 0, image=tk_image, anchor="nw")
    image_box.image = tk_image
    
    global image_label
    image_label.configure(text=image_path)
    
    root.update_idletasks()
    root.geometry('{}x{}'.format(root.winfo_reqwidth(), root.winfo_reqheight()))

def prev_dfa_image():
    global curr_image
    curr_image -= 1
    curr_image = curr_image % guess.count_final
    image_path = "out" + str(curr_image) + ".png"
    image = Image.open(image_path)
    image = image.resize((round(image.width*image_ratio), round(image.height*image_ratio)))
    tk_image = ImageTk.PhotoImage(image)
    
    global image_box
    image_box.configure(width=image.width, height=image.height)
    image_box.create_image(0, 0, image=tk_image, anchor="nw")
    image_box.image = tk_image
    
    global image_label
    image_label.configure(text=image_path)

    root.update_idletasks()
    root.geometry('{}x{}'.format(root.winfo_reqwidth(), root.winfo_reqheight()))

image_label = tk.Label(root, text=image_path, bg="white")
image_label.grid(row=2, column=2)


image_button_frame = tk.Frame(root)
image_button_frame.grid(row=3, column=2, padx=10, pady=10)


backwards_button = tk.Button(image_button_frame, text="<", command=prev_dfa_image)
backwards_button.pack(side=tk.LEFT, padx=5)

forward_button = tk.Button(image_button_frame, text=">", command=next_dfa_image)
forward_button.pack(side=tk.LEFT, padx=5) 

def set_font_size():
    size = int(font_size_input.get())
    tkFont.nametofont("TkDefaultFont").configure(size=size)
    tkFont.nametofont("TkTextFont").configure(size=size) 

font_size_input_frame = tk.Frame(root)
font_size_input_frame.grid(row=4, column=0, padx=10, pady=10)

font_size_input = tk.Entry(font_size_input_frame)
font_size_input.grid(row=0, column=0)
font_size_button = tk.Button(font_size_input_frame, text="Set font size", command=set_font_size)
font_size_button.grid(row=0, column=1)

def set_image_size():
    size = float(image_size_input.get())
    global image_ratio
    image_ratio = size
    
    global curr_image
    image_path = "out" + str(curr_image) + ".png"
    image = Image.open(image_path)
    image = image.resize((round(image.width*image_ratio), round(image.height*image_ratio)))
    tk_image = ImageTk.PhotoImage(image)
    
    global image_box
    image_box.configure(width=image.width, height=image.height)
    image_box.create_image(0, 0, image=tk_image, anchor="nw")
    image_box.image = tk_image
    
    global image_label
    image_label.configure(text=image_path)
    
    root.update_idletasks()
    root.geometry('{}x{}'.format(root.winfo_reqwidth(), root.winfo_reqheight()))

image_size_input_frame = tk.Frame(root)
image_size_input_frame.grid(row=5, column=0, padx=10, pady=10)

image_size_input = tk.Entry(image_size_input_frame)
image_size_input.grid(row=0, column=0)
image_size_button = tk.Button(image_size_input_frame, text="Set image size", command=set_image_size)
image_size_button.grid(row=0, column=1)

root.mainloop()
