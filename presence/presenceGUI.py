import asyncio
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox

from pypresence import Presence

# import pickle


# Look at https://www.geeksforgeeks.org/python-tkinter-validating-entry-widget/ for entry
# https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter
# menu https://www.geeksforgeeks.org/changing-the-colour-of-tkinter-menu-bar/
# https://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html

## Figure out how to store previous info


class PresenceGUI:
    def __init__(self, master):
        self.master = master
        self.DICT_OF_FIELDS = {
            "client_id": "Client ID",
            "state": "State",
            "details": "Details",
            "large_image": "Large Image Name",
            "large_text": "Large Image Text",
            "small_image": "Small Image Name",
            "small_text": "Small Image Text",
            "buttons": "Buttons",
        }
        self.master.title("Sharky PyPresence")
        # master.geometry("300x300")
        self.master.geometry("435x320")
        self.master.configure(bg="gray")
        self.master.iconbitmap("data/myicon.ico")
        self.started_rpc = False
        self.wait_until = None
        # self.restore_file = "data/settings.pickle"
        # https://stackoverflow.com/questions/33553200/save-and-load-gui-tkinter

        # vcdm = master.register(
        #    self.presence_form(self.LIST_OF_FIELDS),
        # ) # we have to wrap the command

        ents = self.presence_form(self.DICT_OF_FIELDS)

        b1 = tk.Button(
            root, text="Process", command=(lambda e=ents: self.temp_rpc(e))
        )  # Fetch returns the content
        b1.pack(side=tk.LEFT, padx=5, pady=5)
        b2 = tk.Button(root, text="Quit", command=root.quit)
        b2.pack(side=tk.LEFT, padx=5, pady=5)
        b3 = tk.Button(root, text="Help", command=(lambda e=root: self.help_window()))
        b3.pack(side=tk.RIGHT, padx=5, pady=5)

    def presence_form(self, fields):
        entries = []
        did_buttons = False
        for key in fields.keys():
            row = tk.Frame(self.master)
            if key == "buttons":
                if not did_buttons:
                    # need to create 4 entries w/ different labels
                    button_one_label = tk.Label(
                        row, width=11, text="Button 1 Label", anchor="w", bg="gray"
                    )
                    button_one_link = tk.Label(
                        row, width=11, text=" Button 1 Link", anchor="w", bg="gray"
                    )
                    b_One_label_entry = tk.Entry(row)
                    b_One_link_entry = tk.Entry(row)

                    button_two_label = tk.Label(
                        row, width=11, text="Button 2 Label", anchor="w", bg="gray"
                    )
                    button_two_link = tk.Label(
                        row, width=11, text=" Button 2 Link", anchor="w", bg="gray"
                    )
                    b_Two_label_entry = tk.Entry(row)
                    b_Two_link_entry = tk.Entry(row)

                    row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

                    button_one_label.grid(row=8, column=1, sticky=tk.W, rowspan=tk.YES)
                    button_one_link.grid(row=8, column=3, sticky=tk.W, rowspan=tk.YES)
                    b_One_label_entry.grid(row=8, column=2, padx=3, pady=1, rowspan=tk.YES)
                    b_One_link_entry.grid(row=8, column=4, padx=3, pady=1, rowspan=tk.YES)

                    button_two_label.grid(row=9, column=1, sticky=tk.W, rowspan=tk.YES)
                    button_two_link.grid(row=9, column=3, sticky=tk.W, rowspan=tk.YES)
                    b_Two_label_entry.grid(row=9, column=2, padx=3, pady=1, rowspan=tk.YES)
                    b_Two_link_entry.grid(row=9, column=4, padx=3, pady=1, rowspan=tk.YES)

                    entries.append(("Button 1 Label", b_One_label_entry))
                    entries.append(("Button 1 Link", b_One_link_entry))
                    entries.append(("Button 2 Label", b_Two_label_entry))
                    entries.append(("Button 2 Link", b_Two_link_entry))

                    did_buttons = True

            elif key == "client_id":
                reg = self.master.register(self._client_callback)
                lab = tk.Label(row, width=15, text=fields[key], anchor="w", bg="gray")
                ent = tk.Entry(row)
                ent.config(validate="key", validatecommand=(reg, "%P"))
                row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
                lab.pack(side=tk.LEFT)
                ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
                entries.append((key, ent))

            else:
                lab = tk.Label(row, width=15, text=fields[key], anchor="w", bg="gray")
                ent = tk.Entry(row)
                row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
                lab.pack(side=tk.LEFT)
                ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
                entries.append((key, ent))
        return entries

    def _client_callback(self, client_input):
        """
        Requires client_id to only be an int
        """
        if client_input.isdigit() or client_input == "":
            return True
        else:
            return False

    def help_window(self):
        """
        Displays help menu on start or when help is clicked.
        """
        helpwindow = tk.Toplevel(self.master)

        helpwindow.title("Help Menu")
        helpwindow.geometry("400x400")
        helpwindow.config(bg="gray")
        helpwindow.resizable(width=False, height=False)

        tk.Label(helpwindow, text="Test", bg="gray").pack()

    def _error_window(self, error: dict):
        key_view = error.keys()
        key_iterator = iter(key_view)
        first_key = next(key_iterator)

        values_view = error.values()
        value_iterator = iter(values_view)
        first_value = next(value_iterator)

        messagebox.showerror(first_key, first_value)

    def fetch(self, entries):
        for entry in entries:
            field = entry[0]
            text = entry[1].get()
            print('%s: "%s"' % (field, text))

    def process_information(self, entries):
        entry_dict = {
            "client_id": False,
            "state": False,
            "details": False,
            "large_image": False,
            "large_text": False,
            "small_image": False,
            "small_text": False,
            "buttons": [],
        }
        button_type = ["Button 1 Label", "Button 1 Link", "Button 2 Label", "Button 2 Link"]
        button_dict = {"buttons": [{"label": "", "url": ""}, {"label": "", "url": ""}]}
        for entry in entries:
            field = entry[0]
            text = entry[1].get()
            if field in button_type:
                if button_dict.get("buttons"):
                    if field == "Button 1 Label":
                        if not text:  # Since we require text on this...
                            button_dict.pop("buttons")
                            entry_dict.pop("buttons")
                            continue
                        else:
                            button_dict["buttons"][0]["label"] = text
                    elif field == "Button 1 Link":
                        button_dict["buttons"][0]["url"] = text
                    if button_dict.get("buttons"):
                        if field == "Button 2 Label":
                            if not text:
                                button_dict["buttons"].pop(1)
                            else:
                                button_dict["buttons"][1]["label"] = text
                        elif field == "Button 2 Link":
                            if not text:
                                try:
                                    button_dict["buttons"].pop(1)
                                except IndexError:
                                    continue
                            else:
                                button_dict["buttons"][1]["url"] = text

                    entry_dict["buttons"] = button_dict["buttons"]
            else:
                if text:
                    entry_dict[field] = text
                else:
                    print(field)
                    entry_dict.pop(field)
            # print('%s: "%s"' % (field, text))
        print(entry_dict)
        return entry_dict

    def temp_rpc(self, entry_info):
        if self.wait_until:
            now = datetime.now()
            while self.wait_until > now:
                asyncio.run(asyncio.sleep(1))
                now = datetime.now()

        if self.started_rpc is False:
            entries = self.process_information(entry_info)
            self.RPC = Presence(entries["client_id"])
            self.RPC.connect()
            entries.pop("client_id")

        else:
            entries = self.process_information(entry_info)
            entries.pop("client_id")

        now = datetime.now()
        self.wait_until = now + timedelta(seconds=15)

        self.RPC.update(**entries)
        self.started_rpc = True


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=False, height=False)
    presgui = PresenceGUI(root)
    root.mainloop()
