import json
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

color="#36C2CE"   #028391"
color2="#ce4236"     #"#FF0000"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    # password_list = []
    pass_letter = [random.choice(letters) for i in range(nr_letters)]
    pass_symbol = [random.choice(symbols) for i in range(nr_symbols)]
    pass_number = [random.choice(numbers) for i in range(nr_numbers)]
    password_list = pass_letter + pass_symbol + pass_number
    random.shuffle(password_list)
    password="".join(password_list)
    pass_entry.insert(0,password)
    pyperclip.copy(password)



# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website=web_entry.get()
    email=email_entry.get()
    password=pass_entry.get()
    new_data={
        website:{
            "email": email,
            "password": password
        }
    }
    if len(website)==0 or len(password)==0 or len(email)==0:
        messagebox.showinfo(title="OOPS",message="Cannot leaave any fields empty")
    else:
        is_ok=messagebox.askokcancel(title=website,message=f"The details entered are:\nEmail: {email}"
                                                           f"\nPassword: {password}\n Is it ok to save?")
        if is_ok:
            try:
                with open("data.json","r") as data_file:
                    data=json.load(data_file)   ##read old data
            except(FileNotFoundError, json.decoder.JSONDecodeError):
                with open("data.json","w") as data_file:
                    json.dump(new_data, data_file, indent=4)


            else:
                # Check if the website already exists in the data
                if website in data:
                    update = messagebox.askyesno("Warning",
                                                 f"There is already a password saved for {website}.\n"
                                                 f"Would you like to overwrite?")
                    if update:
                        # Overwrite the existing data for the website
                        data[website]["password"] = password
                        data[website]["email"] = email
                    else:
                        return  # Exit the function without saving
                else:
                    data.update(new_data)  # Update old data with new data
                with open("data.json","w") as data_file:
                    json.dump(data,data_file,indent=4)      ##Save updated data

            finally:
                web_entry.delete(0,END)
                email_entry.delete(0, END)
                pass_entry.delete(0, END)


# ---------------------------- Search ------------------------------- #
def search():
    website=web_entry.get()
    try:
        with open(file="data.json",mode="r") as data_file:
            data=json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error",message="No such file found")
    else:
        if website in data:
            email=data[website]["email"]
            password=data[website]["password"]
            messagebox.showinfo(title=website,message=f"email: {email}\npassword: {password}")
        else:
            messagebox.showinfo(title="Error",message=f"No details for {website} exist")








# ---------------------------- UI SETUP ------------------------------- #
window=Tk()
window.title("Password Manager")
window.config(padx=40,pady=40,bg=color)
canvas=Canvas(width=200,height=200,bg=color,highlightthickness=0)
img=PhotoImage(file="logo.png")
canvas.create_image(100,100,image=img)
canvas.grid(column=1,row=0)

#website label
website_label=Label(text="Website:",bg=color)
website_label.grid(column=0,row=1)

#email/username label
email_label=Label(text="Email/Username:",bg=color)
email_label.grid(column=0,row=2)

#password label
pass_label=Label(text="Password:",bg=color)
pass_label.grid(column=0,row=3)

web_entry=Entry(width=35)
web_entry.grid(column=1,row=1,sticky="EW")
web_entry.focus()

email_entry=Entry(width=35)
email_entry.grid(column=1,row=2,columnspan=2,sticky="EW")

pass_entry=Entry(width=21)
pass_entry.grid(column=1,row=3, sticky="EW")

#Generate Button
g_button=Button(text="Generate password",command=gen_password,bg=color2)
g_button.grid(column=2,row=3,sticky="EW")

#Add Button
add_button=Button(text="Add",width=36,command=save,bg=color2)
add_button.grid(column=1,row=4,columnspan=2,sticky="EW")

#search button
search_button=Button(text="Search",command=search,bg=color2)
search_button.grid(column=2,row=1,sticky="EW")


window.mainloop()