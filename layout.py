import tkinter
from tkinter import *
from tkinter.ttk import *
import PIL.ImageTk as imtk
import PIL.Image as im
import tkinter as tk
import os
from tkinter.font import Font
from PIL import Image, ImageTk
master = tk.Tk()
master.geometry("400x600")
background_image = imtk.PhotoImage(file="human-heart.png")
# Create and display the Canvas
canvas_widget = Canvas(master, width=800, height=500)
canvas_widget.pack(fill="both", expand=True)
# Displaying the image inside canvas
canvas_widget.create_image(0, 0, image=background_image, anchor="nw")
# Create a function to resize all the images
def resize_image(e, updated_background_image):
    # Resize Image using resize function
	resized_background_image = updated_background_image.resize(
		(e.width, e.height), im.ANTIALIAS)
	return resized_background_image
# Create resize function with argument e
def image_background(e):

	# Define updated_background_image, resized_background_image, new_background_image globally
	global updated_background_image, resized_background_image, new_background_image
# Open and identify the image
	updated_background_image = im.open("human-heart.png")

	# Call the resize_image function
	resized_background_image = resize_image(e, updated_background_image)

	# Define resized image again using PhotoImage function
	new_background_image = imtk.PhotoImage(resized_background_image)

	# Display the newly created image in canvas
	canvas_widget.create_image(0, 0, image=new_background_image, anchor="nw")
	image_background()
# Get parameters of resizing window and bind python function resizer to screen resize
master.bind('<Configure>', image_background)

def run_program():
    os.system('python bpm.py')
#def run_prog1():
    #os.system('python star.py')
#def run_prog2():
     #os.system('Static.py')
#def run_prog3():
     #os.system('No Beat.py')

def openNewWindow():
    newWindow = Toplevel(master)
    newWindow.title("Heart Activity")
    newWindow.geometry("400x600")
    button_font = Font(family="Tahoma", size=12, weight="bold")
    Button1 = tk.Button(newWindow,text ="Fast Beat",bg="red",width=10, height=2,compound = TOP,font=button_font, command = run_program)
    Button1.pack(pady = 40)
    Button2 = tk.Button(newWindow,text ="Slow Beat",bg="red",width=10, height=2,compound = TOP,font=button_font)
    Button2.pack(pady = 40)
    Button3 = tk.Button(newWindow,text ="Static",bg="red",width=10, height=2,compound = TOP,font=button_font)
    Button3.pack(pady = 40)
    Button4 = tk.Button(newWindow,text ="No Beat",bg="red",width=10, height=2,compound = TOP,font=button_font)
    Button4.pack(pady = 40)

def blink():
    button.config(bg='red' if button.cget('bg') == 'white' else 'white')
    button.after(500, blink)
button_font = Font(family="Tahoma", size=12, weight="bold")
button = tk.Button(master, text='Click Me!!', bg='white',width=10, height=2,command = openNewWindow,font=button_font)
button.pack()
blink()
master.mainloop()
