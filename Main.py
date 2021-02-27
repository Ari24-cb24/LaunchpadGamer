from Controller import Controller
import tkinter as tk
import json

__version__ = 0.7
__author__ = "Ari24"

class App:
    profile_scrollbar: tk.Scrollbar
    profile_listing: tk.Listbox

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Launchpad Controller V" + str(__version__))
        self.root.geometry("700x600")

        self.selected_profile_index = None
        self.selected_profile = None

        with open("profileData.json", "r") as fh:
            self.profiles = json.load(fh)

    def _save_profiles(self):
        with open("profileData.json", "w") as fh:
            json.dump(self.profiles, fh, indent=4)

    def on_profile_select(self, evt):
        widget = evt.widget
        index = int(widget.curselection()[0])
        value = widget.get(index)

        self.selected_profile_index = index
        self.selected_profile = value

        self.update_profiles()

    def add_profile(self):
        self.profile_listing.insert(tk.END, "dummyprofile")
        self.profiles.append({"name": "dummyprofile"})
        self.update_profiles()

    def remove_profile(self):
        if self.selected_profile_index is not None:
            self.profile_listing.delete(self.selected_profile_index)
            self.profiles.pop(self.selected_profile_index)

            self.selected_profile_index = None
            self.selected_profile = None

            self.update_profiles()

    def update_profiles(self):
        self.profile_listing.delete(0, tk.END)

        for profile in self.profiles:
            self.profile_listing.insert(tk.END, profile["name"])

        if self.selected_profile is not None:
            nameVar = tk.StringVar(self.root)
            name = tk.Entry(self.root, textvariable=nameVar)
            name.pack()

    def run(self):
        self.profile_scrollbar = tk.Scrollbar(self.root)
        self.profile_scrollbar.pack(side=tk.LEFT, pady=30)

        self.profile_listing = tk.Listbox(self.root, yscrollcommand=self.profile_scrollbar.set)
        for profile in self.profiles:
            self.profile_listing.insert(tk.END, profile["name"])

        self.profile_listing.bind("<<ListboxSelect>>", self.on_profile_select)
        self.profile_listing.pack(side=tk.LEFT, fill=tk.BOTH, pady=30)
        self.profile_scrollbar.config(command=self.profile_listing.yview)

        tk.Button(self.root, command=self.add_profile, text="+").place(x=20, y=0, width=27, height=27)
        tk.Button(self.root, command=self.remove_profile, text="-").place(x=52, y=0, width=27, height=27)

        self.root.mainloop()


if __name__ == '__main__':
    c = Controller()
    c.start()