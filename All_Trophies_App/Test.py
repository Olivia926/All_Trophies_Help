import tkinter as tk
from PIL import Image, ImageTk

confirmed = [0]

def change_state(ind, txt):
    global confirmed

    if confirmed[ind]:
        confirmed[ind] = 0
        txt.config(background='white')
    else:
        confirmed[ind] = 1
        txt.config(background='green')


root = tk.Tk()

file = "../Images/Image_Atlas.png"
photo = Image.open(file)
i = 0
cropped_rect = ((i % 16) * 250, int(i/16) * 300, (i % 16) * 250 + 250, int(i/16) * 300 + 300)
cropped_im = photo.crop(cropped_rect)
im = ImageTk.PhotoImage(cropped_im)

text = tk.Text(root)
text.pack()






text.tag_config("tag1", foreground="blue")
text.tag_bind("tag1", "<Button-1>", lambda * args:change_state(0, text))
text.insert(tk.END, "first link", "tag1")

text.insert(tk.END, " other text ")

text.tag_config("tag2", foreground="blue")
text.insert(tk.END, "second link\n", "tag2")

text.image_create(tk.END, image=im)
text.image = im


root.mainloop()