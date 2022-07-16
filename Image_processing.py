from tkinter import *
import os
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter
from matplotlib import image as mpimg
import numpy as np
import cv2
import scipy.signal

gui_width = 1385
gui_height = 595

ip_file = ""
op_file = ""
original_img = None
modified_img = None
user_arg = None
popup = None
popup_input = None

root = Tk()
root.minsize(gui_width, gui_height)

s = ttk.Style()
s.configure('TLabelframe.Label', font='Lora 14')

def draw_before_canvas():
    global original_img, ip_file
    original_img = Image.open(ip_file)
    original_img = original_img.convert("RGB")
    img = ImageTk.PhotoImage(original_img)
    before_canvas.create_image(
        256,
        256,
        image=img,
        anchor="center",
    )
    before_canvas.img = img


def draw_after_canvas(mimg):
    global modified_img

    modified_img = Image.fromarray(mimg)
    img = ImageTk.PhotoImage(modified_img)
    after_canvas.create_image(
        256,
        256,
        image=img,
        anchor="center",
    )
    after_canvas.img = img


def load_file():
    global ip_file
    ip_file = filedialog.askopenfilename(
        title="Open an image file",
        initialdir=".",
        filetypes=[("All Image Files", "*.*")],
    )
    draw_before_canvas()


def save_file():
    global ip_file, original_img, modified_img
    file_ext = os.path.splitext(ip_file)[1][1:]
    op_file = filedialog.asksaveasfilename(
        filetypes=[
            (
                f"{file_ext.upper()}",
                f"*.{file_ext}",
            )
        ],
        defaultextension=[
            (
                f"{file_ext.upper()}",
                f"*.{file_ext}",
            )
        ],
    )
    modified_img = modified_img.convert("RGB")
    modified_img.save(op_file)


left_frame = ttk.LabelFrame(root, text="Original Image", borderwidth=4, labelanchor=N)
left_frame.pack(fill=BOTH, side=LEFT, padx=10, pady=10, expand=1)

middle_frame = ttk.LabelFrame(root, text="Algorithms", borderwidth=4, labelanchor=N)
middle_frame.pack(fill=BOTH, side=LEFT, padx=5, pady=10)

right_frame = ttk.LabelFrame(root, text="Modified Image", borderwidth=4, labelanchor=N)
right_frame.pack(fill=BOTH, side=LEFT, padx=10, pady=10, expand=1)

# left frame contents
before_canvas = Canvas(left_frame, bg="white", width=512, height=512)
before_canvas.pack(expand=1)

browse_btn = ttk.Button(left_frame, text="Browse", command=load_file)
browse_btn.pack(expand=1, anchor=SW, pady=(5, 0))

# middle frame contents
algo_canvas = Canvas(middle_frame, width=200, highlightthickness=0)
scrollable_algo_frame = Frame(algo_canvas)
scrollbar = Scrollbar(
    middle_frame, orient="vertical", command=algo_canvas.yview, width=15
)

scrollbar.pack(side="right", fill="y")
algo_canvas.pack(fill=BOTH, expand=1)
algo_canvas.configure(yscrollcommand=scrollbar.set)
algo_canvas.create_window((0, 0), window=scrollable_algo_frame, anchor="nw")
scrollable_algo_frame.bind(
    "<Configure>", lambda _: algo_canvas.configure(scrollregion=algo_canvas.bbox("all"))
)

# right frame contents
after_canvas = Canvas(right_frame, bg="white", width=512, height=512)
after_canvas.pack(expand=1)

save_btn = ttk.Button(right_frame, text="Save", command=save_file)
save_btn.pack(expand=1, anchor=SE, pady=(5, 0))


def rgb2gray():
    img = mpimg.imread(ip_file)
    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    return 0.299 * R + 0.58 * G + 0.114 * B

def callrgb2gray():
    grayscale = rgb2gray()
    draw_after_canvas(grayscale)

def negative(set_gray):
    img = rgb2gray() if (set_gray) else Image.open(ip_file)
    img = np.array(img)
    img = 255 - img
    draw_after_canvas(img)

def edge_detection():
    image_edge = cv2.imread(ip_file)
    edges = cv2.Canny(image_edge, 50, 300)
    draw_after_canvas(edges)

def blur_image():
    image_blur = cv2.imread(ip_file)
    kernel_size = (7, 7)
    img_blur = cv2.blur(image_blur, kernel_size)
    img_cv = cv2.imshow('blur', img_blur)
    # draw_after_canvas(img_blur)

ttk.Button(
    scrollable_algo_frame, text="RGB to Grayscale", width=30, command=callrgb2gray
).pack(expand=1, padx=5, pady=2, ipady=2)

ttk.Button(
    scrollable_algo_frame,
    text="Negative",
    width=30,
    command=lambda: negative(set_gray=False),
).pack(pady=2, ipady=2)

ttk.Button(
    scrollable_algo_frame,
    text="Canny Edge Detection",
    width=30,
    command=edge_detection,
).pack(pady=2, ipady=2)

ttk.Button(
    scrollable_algo_frame,
    text="Blur image",
    width=30,
    command=blur_image
).pack(pady=2, ipady=2)

root.mainloop()