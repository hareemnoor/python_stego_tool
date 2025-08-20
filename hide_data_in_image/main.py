import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

def to_bin(data):
    return ''.join(format(ord(i), '08b') for i in data)

def encode_lsb(image, message):
    binary_message = to_bin(message) + '1111111111111110'  # End delimiter
    data_index = 0
    pixels = list(image.getdata())
    new_pixels = []

    for pixel in pixels:
        if data_index < len(binary_message):
            r, g, b = pixel
            r = (r & ~1) | int(binary_message[data_index])
            data_index += 1
            if data_index < len(binary_message):
                g = (g & ~1) | int(binary_message[data_index])
                data_index += 1
            if data_index < len(binary_message):
                b = (b & ~1) | int(binary_message[data_index])
                data_index += 1
            new_pixels.append((r, g, b))
        else:
            new_pixels.append(pixel)

    image.putdata(new_pixels)
    return image

def decode_lsb(image):
    binary_data = ""
    for pixel in image.getdata():
        for value in pixel[:3]:
            binary_data += str(value & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ""
    for byte in all_bytes:
        if byte == '11111110':
            break
        message += chr(int(byte, 2))
    return message

# GUI Functions
def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if file_path:
        image_path_var.set(file_path)

def save_image(img):
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        img.save(file_path)
        messagebox.showinfo("Saved", "Image saved successfully.")

def encode_message():
    try:
        image_path = image_path_var.get()
        message = message_entry.get("1.0", tk.END).strip()
        if not image_path or not message:
            raise ValueError("Please select an image and enter a message.")

        img = Image.open(image_path)
        if img.mode != "RGB":
            img = img.convert("RGB")

        encoded_img = encode_lsb(img, message)
        save_image(encoded_img)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decode_message():
    try:
        image_path = image_path_var.get()
        if not image_path:
            raise ValueError("Please select an image.")

        img = Image.open(image_path)
        message = decode_lsb(img)
        messagebox.showinfo("Hidden Message", message)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Layout
root = tk.Tk()
root.title("StegoTool - Image Steganography")

image_path_var = tk.StringVar()

tk.Label(root, text="Image Path:").pack()
tk.Entry(root, textvariable=image_path_var, width=50).pack()
tk.Button(root, text="Browse Image", command=open_image).pack()

tk.Label(root, text="Enter your secret message:").pack()
message_entry = tk.Text(root, height=5, width=50)
message_entry.pack()

tk.Button(root, text="Encode Message", command=encode_message).pack(pady=5)
tk.Button(root, text="Decode Message", command=decode_message).pack()

root.mainloop()








