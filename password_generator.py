# password generator - cs 3080 final project

import tkinter as tk            # for GUI
from tkinter import messagebox  # for pop up windows
import string 
import secrets                  # more secure than random 

class PasswordGenerator:
    def __init__(self, length, use_upper, use_digits, use_symbols):
        # save user's settings so other methods can use them
        self.length = length 
        self.use_upper = use_upper 
        self.use_digits = use_digits
        self.use_symbols = use_symbols

    def check_length(self):
        # make sure length is in range before generating 
        # raise ValueError so GUI can catch and show error
        if self.length < 8:
            raise ValueError("password length must be at least 8")
        if self.length > 64:
            raise ValueError("password length cannot be more than 64")

    def get_character_groups(self):
        # build list of charcter sets the user selected 
        # lowercase always included (others chosen through checkboxes)
        groups = [string.ascii_lowercase]         # a-z
        if self.use_upper:
            groups.append(string.ascii_uppercase) # A-Z
        if self.use_digits:
            groups.append(string.digits)          # 0-9
        if self.use_symbols:
            groups.append(string.punctuation)     # !@#$%^&*...
        return groups

    def generate(self):
        # create and return passwords
        self.check_length() # stop if length invalid 
        groups = self.get_character_groups() # get selected character sets 

        password_list = [] # build password list then turn to string

        # add one character from each selected character set
        for group in groups:
            password_list.append(secrets.choice(group))

        # combine selected character sets into one string of allowed characters 
        all_characters = ""
        for group in groups:
            all_characters = all_characters + group

        # add random charcters until length reached 
        while len(password_list) < self.length:
            password_list.append(secrets.choice(all_characters))

        # shuffle list so characters not all at front
        secrets.SystemRandom().shuffle(password_list)

        # join list of charcters into one string
        return "".join(password_list)

class StrongPasswordGenerator(PasswordGenerator):
    def __init__(self, length, use_upper, use_digits, use_symbols):
        # call parent __init__ so settings are the same 
        super().__init__(length, use_upper, use_digits, use_symbols)
        self.strength = "" # stores password strength 

    def check_strength(self, password):
        # rate password using point system 0-6
        score = 0

        # longer passwords gain points 
        if len(password) >= 16:
            score = score + 1
        if len(password) >= 32:
            score = score + 1

        # character type flags 
        has_lower = False
        has_upper = False
        has_digit = False
        has_symbol = False

        # go through characters and check what type (set flags to true if found)
        for character in password:
            if character in string.ascii_lowercase:
                has_lower = True
            elif character in string.ascii_uppercase:
                has_upper = True
            elif character in string.digits:
                has_digit = True
            elif character in string.punctuation:
                has_symbol = True

        # point gained for each character type used 
        if has_lower:
            score = score + 1
        if has_upper:
            score = score + 1
        if has_digit:
            score = score + 1
        if has_symbol:
            score = score + 1

        # convert score to rating 
        if score <= 2:
            return "weak"
        elif score <= 4:
            return "medium"
        else:
            return "strong"

    def generate(self):
        # override parent generate method 
        # uses parent version to make password then rates 
        password = super().generate()
        self.strength = self.check_strength(password)
        return password

class PasswordApp:
    def __init__(self, window):
        # window setup
        self.window = window
        self.window.title("password generator")
        self.window.geometry("420x360")

        # title at top of window 
        title = tk.Label(window, text="password generator", font=("Arial", 18, "bold"))
        title.pack(pady=10) # place widget with pack() and verical spacing with pady

        # password length input (default 12)
        length_label = tk.Label(window, text="password length (8-64):")
        length_label.pack()
        self.length_entry = tk.Entry(window, width=10, justify="center")
        self.length_entry.insert(0, "12")
        self.length_entry.pack(pady=5)

        # keep track of what checkbox is selected 
        # all options start checked
        self.upper_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        # checkboxes 
        tk.Checkbutton(window, text="include uppercase letters (A-Z)", variable=self.upper_var).pack()
        tk.Checkbutton(window, text="include numbers (0-9)", variable=self.digits_var).pack()
        tk.Checkbutton(window, text="include symbols (!@#$%^&*...)", variable=self.symbols_var).pack()

        # generate button (make password)
        generate_button = tk.Button(window, text="generate password", command=self.make_password)
        generate_button.pack(pady=10)

        # box where generated password is displayed 
        self.password_entry = tk.Entry(window, width=40, font=("Courier", 12), justify="center")
        self.password_entry.pack(pady=5)

        # show strength rating of password after generated 
        self.strength_label = tk.Label(window, text="strength: ", font=("Arial", 12))
        self.strength_label.pack(pady=5)

        # copy button
        copy_button = tk.Button(window, text="copy to clipboard", command=self.copy_password)
        copy_button.pack(pady=5)

    def make_password(self):
        # called when genereate button is clicked 
        try:
            # get length from user and convert to int
            length = int(self.length_entry.get())

            # create generator object with user's settings
            generator = StrongPasswordGenerator(
                length,
                self.upper_var.get(),
                self.digits_var.get(),
                self.symbols_var.get()
            )
            password = generator.generate()

            # clear old password and display new one
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)

            # pick color based on strength
            if generator.strength == "strong":
                color = "green"
            elif generator.strength == "medium":
                color = "orange"
            else:
                color = "red"

            # update strength label with rating and color
            self.strength_label.config(text="strength: " + generator.strength, fg=color)

        except ValueError:
            # if non number or outside range shows pop-up
            messagebox.showerror("invalid input", "please enter a whole number from 8 to 64")

    def copy_password(self):
        # called when copy to clipboard button clicked
        password = self.password_entry.get()

        # do not copy if no password generated 
        if password == '':
            messagebox.showerror("nothing to copy", "generate a password first")
            return

        # replace what is on clipboard with password
        self.window.clipboard_clear()
        self.window.clipboard_append(password)
        messagebox.showinfo("copied", "password copied to clipboard")

# run when file is run directly
if __name__ == "__main__":
    window = tk.Tk() # create main window
    app = PasswordApp(window) # build app inside window 
    window.mainloop() # keep window open 