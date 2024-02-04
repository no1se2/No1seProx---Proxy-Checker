#Coded by no1se in 6 hours I'm suck :(
import requests
import tkinter as tk
from tkinter import filedialog, StringVar
import os
from datetime import datetime
from tkinter import *
from PIL import Image, ImageTk
import platform



def check_proxy(proxy, proxy_type):
    headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)'}
    try:
        proxies = {proxy_type: proxy}
        url = "http://www.google.com"
        response = requests.get(url, proxies=proxies, timeout=5,headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException as e:
        return False

    
def browse_file():
    global proxies
    file_path = filedialog.askopenfilename(filetypes=[("Proxy File", "*.txt")])
    entry_file_path.delete(0, tk.END)
    proxies = [line.strip() for line in open(file_path, "r").readlines()]

    entry_file_path.insert(0, file_path)

    tk.messagebox.showinfo("Proxies Loaded", f"Loaded {len(proxies)} proxies")


def start_check():
    
    global stopping
    stopping = False

    working_proxies.clear()  
    proxy_file_path = entry_file_path.get()
    proxy_type = proxy_type_var.get()

    if not proxy_file_path:
        result_label.config(text="Hey man, you can't start without selecting a proxy file.")
        root.update()
        return

    with open(proxy_file_path, "r") as file:
        proxies = [line.strip() for line in file.readlines()]

    total_proxies = len(proxies)

    good_count = 0
    bad_count = 0

    def check_next_proxy():
        nonlocal good_count, bad_count, total_proxies
        
        global stopping

        if stopping:
            return

        if not proxies:
            save_working_proxies(good_count, proxy_type)
            return

        proxy = proxies.pop(0)

        if check_proxy(proxy, proxy_type):
            result_label.config(text=f"{proxy_type.upper()} Proxy {proxy} is alive.",fg="green",bg="black")
            good_count += 1
            working_proxies.append(proxy)  
        else:
            result_label.config(text=f"{proxy_type.upper()} Proxy {proxy} is dead (RIP).",fg="red",bg="black")
            bad_count += 1


        remaining_proxies = total_proxies - (good_count + bad_count)
        good_bad_label.config(text=f"Good: {good_count} | Bad: {bad_count} | Remaining: {remaining_proxies}")
        
        root.update()

        root.after(100, check_next_proxy)  

    check_next_proxy()

def save_working_proxies(good_count, proxy_type):
    answer = tk.messagebox.askquestion("Hold UP!", "Would you like to save the working proxies?")
    if answer == "yes":
        result_folder = os.path.join("results", datetime.now().strftime("%Y-%m-%d"))
        os.makedirs(result_folder, exist_ok=True)

        result_file_path = os.path.join(result_folder, f"working_proxies_{proxy_type}.txt")

        with open(result_file_path, "w") as result_file:
            result_file.write(f"Hey there, here is your {proxy_type.upper()} working proxies. Love you and have a good day!:\n")
            result_file.write(f"Total: {good_count}\n\n")

            for proxy in working_proxies:
                result_file.write(f"{proxy}\n")

    working_proxies.clear()
    entry_file_path.delete(0, tk.END)
    result_label.config(text="")
    good_bad_label.config(text="Good: 0 | Bad: 0")
    
    root.update()

working_proxies = []

root = tk.Tk()
root.title("Proxy Checker By no1se")

#Background&icon
if platform.system() == "Windows": 
    root.iconbitmap("src/icon.ico")

image_path = "src/background.png"
img = Image.open(image_path)

background_image = ImageTk.PhotoImage(img)
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
#Background&icon

frame_file = tk.Frame(root)
frame_file.pack(pady=10)
entry_file_path = tk.Entry(frame_file, width=50)
entry_file_path.pack(side=tk.LEFT, padx=5)
button_browse = tk.Button(frame_file, text="Browse", command=browse_file, bg="black", fg="white",relief=tk.FLAT)
button_browse.pack(side=tk.RIGHT, padx=5)

frame_type = tk.Frame(root)
frame_type.pack(pady=10)
proxy_type_var = StringVar()
proxy_type_var.set("http")
radio_http = tk.Radiobutton(frame_type, text="HTTP", variable=proxy_type_var, value="http", bg='black', fg='white', selectcolor='black')
radio_http.pack(side=tk.LEFT, padx=0)

button_start = tk.Button(root, text="Start Check", command=start_check, bg='black', fg='white', relief=tk.FLAT)
button_start.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

good_bad_label = tk.Label(root, text="Good: 0 | Bad: 0", bg='black', fg='white', relief=tk.FLAT)
good_bad_label.pack(pady=10)

root.mainloop()

#Coded by no1se in 6 hours I'm suck :(
