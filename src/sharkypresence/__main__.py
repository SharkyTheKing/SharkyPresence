import pathlib
import pickle
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox

from pypresence import Presence, exceptions

NO_CLIENT_MESSAGE = {
    "No Client ID": (
        "No Client ID listed.\n"
        "You MUST have a client_id from your application for this program to work.\n\n"
        "Please read the README.md file to review how to get your ID."
    )
}

INVALID_CLIENT_MESSAGE = {
    "Invalid Client ID": (
        "Invalid Client ID. Please review the help menu or README.md "
        "documentation on how to get your proper client id.\n\n"
        "This will not work without the proper Client ID.\n\nIf this"
        " is shown in error and that IS your valid Client ID. Please "
        "reach out to me. I had to do something hacky regarding this."
    )
}

BUTTON_MESSAGE = {
    "Buttons": (
        "Buttons MUST have a link tied to it. "
        "If you don't want it to link to anything, you can use: "
        "https://localhost/\n\n"
        "This will work and won't link to anywhere as it's acting "
        "as a local source.\n\n We put it in for you "
        "so the program doesn't stop."
    )
}

RESTART_DISCORD_MESSAGE = {
    "Discord Failed": (
        "If you are seeing this error, it means something on discord's end dropped. "
        "Please restart your discord client and hit process to restart the presence."
    )
}

# Look at https://www.geeksforgeeks.org/python-tkinter-validating-entry-widget/ for entry
# https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter
# menu https://www.geeksforgeeks.org/changing-the-colour-of-tkinter-menu-bar/
# https://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html


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
        self.icon_path = pathlib.Path(__file__).parent / "data/myicon.ico"
        self.master.title("Sharky PyPresence")
        self.master.geometry("435x320")
        self.master.configure(bg="gray")
        self.master.iconbitmap(self.icon_path)

        self.started_rpc = False
        self.RPC = None
        self.wait_until = None
        self.restore_file = pathlib.Path(__file__).parent.absolute() / "data/settings.pickle"
        # https://stackoverflow.com/questions/33553200/save-and-load-gui-tkinter

        self.start_building_widget()
        self._restore_state()

    def start_building_widget(self):
        ents = self.presence_form(self.DICT_OF_FIELDS)

        b1 = tk.Button(self.master, text="Process", command=(lambda e=ents: self.temp_rpc(e)))
        b1.pack(side=tk.LEFT, padx=5, pady=5)

        b2 = tk.Button(self.master, text="Stop", command=(lambda e=self.master: self._stop_rpc()))
        b2.pack(side=tk.LEFT, padx=5, pady=5)

        b3 = tk.Button(
            self.master, text="Help", command=(lambda e=self.master: self.help_window())
        )
        b3.pack(side=tk.RIGHT, padx=5, pady=5)

        # b4 = tk.Button(self.master, text="Quit", command=(lambda e=ents: self._save_state(e)))
        # b4.pack(side=tk.LEFT, padx=5, pady=5)
        self.master.wm_protocol("WM_DELETE_WINDOW", (lambda e=ents: self._save_state(e)))

    def presence_form(self, fields):
        entries = []
        did_buttons = False
        for key in fields.keys():
            row = tk.Frame(self.master)
            if key == "buttons":
                if not did_buttons:
                    # need to create 4 entries w/ different labels
                    reg = self.master.register(self._limit_characters)

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
                    b_One_label_entry.config(validate="key", validatecommand=(reg, "%P"))
                    b_One_label_entry.grid(row=8, column=2, padx=3, pady=1, rowspan=tk.YES)
                    b_One_link_entry.grid(row=8, column=4, padx=3, pady=1, rowspan=tk.YES)

                    button_two_label.grid(row=9, column=1, sticky=tk.W, rowspan=tk.YES)
                    button_two_link.grid(row=9, column=3, sticky=tk.W, rowspan=tk.YES)
                    b_Two_label_entry.config(validate="key", validatecommand=(reg, "%P"))
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
            elif key in ["details", "state", "large_text", "small_text"]:
                # need to print the keys to confirm
                reg = self.master.register(self._limit_longer_characters)
                lab = tk.Label(row, width=15, text=fields[key], anchor="w", bg="gray")
                ent = tk.Entry(row)
                row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
                lab.pack(side=tk.LEFT)
                ent.config(validate="key", validatecommand=(reg, "%P"))
                ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
                entries.append((key, ent))
            else:
                reg = self.master.register(self._limit_characters)
                lab = tk.Label(row, width=15, text=fields[key], anchor="w", bg="gray")
                ent = tk.Entry(row)
                row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
                lab.pack(side=tk.LEFT)
                ent.config(validate="key", validatecommand=(reg, "%P"))
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

    def _limit_characters(self, character_input):
        """
        Internal Function to check character limits of entry
        Currently 32 limitation for Buttons and Images
        """
        if len(character_input) > 32:
            return False
        else:
            return True

    def _limit_longer_characters(self, character_input):
        """
        Same as above
        Currently 128 for details, state, large and small text
        """
        if len(character_input) > 128:
            return False
        else:
            return True

    def help_window(self):
        """
        Displays help menu on start or when help is clicked.
        """
        helpwindow = tk.Toplevel(self.master)

        helpwindow.title("Help Menu")
        helpwindow.geometry("400x400")
        helpwindow.config(bg="gray")
        helpwindow.iconbitmap(self.icon_path)
        helpwindow.resizable(width=False, height=False)

        message = (
            "Hello! If you are new to this program. "
            "Please have a read at the README file on the repo. It"
            " will help explain everything if it's not listed.\n\n"
            "1. Head over to Discord's Developer Application Page.\n"
            "Click `New Application`; give it a nice name. we're gonna use "
            '"My Test Game" for ours. In discord\'s user pane, this will'
            ' show as your status "Playing My Test Game"\n\n'
            "2. Copy the `Application ID` from the website and paste "
            "that value into the `Client ID` in our App.\n\n"
            "3. In the website, on the left of the page, navigate to "
            "`Rich Presence`. The `Cover Image` is not used and we can ignore it."
            " Next, add a few images with the `Add Image(s)` button; rename the images "
            "if needed, then click `Save Changes`. It may take several minutes for it to "
            "properly save on discord's side.\n\n"
            "4. In our App, the `Large Image Name` and `Small Image Name` can be set "
            "to any image name that has been uploaded in the steps above.\n\n"
            "5. The remaining fields in our app can be set to anything you desire."
        )
        label = tk.Label(helpwindow, text=message, bg="gray")
        label.configure(wraplength=350, justify=tk.LEFT)
        label.pack()
        credit_label = tk.Label(helpwindow, text="Credits: SharkyTheKing", bg="gray")
        credit_label.place(relx=0.0, rely=1.0, anchor="sw")
        version_label = tk.Label(helpwindow, text="Version: 1.0.3", bg="gray")
        version_label.place(relx=1.0, rely=1.0, anchor="se")

    def _error_window(self, error: dict):
        key_view = error.keys()
        key_iterator = iter(key_view)
        first_key = next(key_iterator)

        # values_view = error.values()
        # value_iterator = iter(values_view)
        # first_value = next(value_iterator)
        first_value = error[first_key]

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
        raise_button_link = False
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
                        if not text:
                            raise_button_link = True
                        button_dict["buttons"][0]["url"] = text if text else "https://localhost/"
                    if button_dict.get("buttons"):
                        if field == "Button 2 Label":
                            if not text:
                                button_dict["buttons"].pop(1)
                            else:
                                button_dict["buttons"][1]["label"] = text
                        elif field == "Button 2 Link":
                            try:
                                if button_dict.get("buttons")[1]:
                                    if not text:
                                        raise_button_link = True
                                    button_dict["buttons"][1]["url"] = (
                                        text if text else "https://localhost/"
                                    )
                            except (KeyError, IndexError):
                                continue

                    entry_dict["buttons"] = button_dict["buttons"]
            else:
                if text:
                    entry_dict[field] = text
                else:
                    entry_dict.pop(field)
        if raise_button_link is True:
            self._error_window(BUTTON_MESSAGE)

        return entry_dict

    def temp_rpc(self, entry_info):
        if self.wait_until:
            now = datetime.now()
            if self.wait_until > now:
                time_left = (self.wait_until - now).seconds
                return self._error_window(
                    {
                        "Timeout Error": (
                            "Please do not repeatedly push process.\n\n"
                            "You must wait 15 seconds before you update your status.\n\n"
                            "You have {seconds} seconds left to wait.".format(seconds=time_left)
                        )
                    }
                )

        if self.started_rpc is False:
            entries = self.process_information(entry_info)
            try:
                self.RPC = Presence(entries["client_id"])
                self.RPC.connect()
            except KeyError:
                return self._error_window(NO_CLIENT_MESSAGE)

            entries.pop("client_id")

        else:
            entries = self.process_information(entry_info)
            entries.pop("client_id")

        now = datetime.now()
        self.wait_until = now + timedelta(seconds=15)

        try:
            self.RPC.update(**entries)
            self.started_rpc = True
        except exceptions.InvalidID:
            return self._error_window(INVALID_CLIENT_MESSAGE)
        except Exception as error:
            if str(error) == "unpack requires a buffer of 8 bytes":
                return self._error_window(RESTART_DISCORD_MESSAGE)
            else:
                raise error  # Odd...but I need to know if there's any other issues.

    def _stop_rpc(self):
        if not self.RPC:
            return
        self.RPC.close()
        self.started_rpc = False

    def _save_state(self, entry):
        text = entry[0][1].get()
        data = {}

        for widget in entry:
            label = widget[0]
            text = widget[1].get()
            data[label] = text

        try:
            with open(self.restore_file, "wb") as f:
                pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print("error saving state:", str(e))

        self.master.quit()

    def _restore_state(self):
        """
        Currently will only restore the state, everything else is manual
        """
        # https://stackoverflow.com/questions/6112482/how-to-get-the-tkinter-label-text
        data = False
        try:
            with open(self.restore_file, "rb") as f:
                data = pickle.load(f)
        except FileNotFoundError:  # File will get created on save state anyways.
            pass
        except Exception as e:
            print("error loading saved state:", str(e))

        if not data:
            return

        self._restore_values(data)

    def get_all_children(self, widget):
        """
        Return a list of all the children, if any, of a given widget.
        Credit to https://stackoverflow.com/questions/52484359/how-to-select-all-instances-of-a-widget-in-tkinter/52484948#52484948
        """
        result = []  # Initialize.
        return self._all_children(widget.winfo_children(), result)

    def _all_children(self, children, result):
        """
        Recursively append all children of a list of widgets to result.
        """
        for child in children:
            result.append(child)
            subchildren = child.winfo_children()
            if subchildren:
                self._all_children(subchildren, result)

        return result

    def _restore_values(self, data):
        """
        Internal function to restore all entry state in UI
        """
        toplevel = self.master.winfo_toplevel()
        selection = [child for child in self.get_all_children(toplevel)]
        try:
            selection[-9].insert(0, data["Button 1 Label"])  # button 1 label entry
            selection[-8].insert(0, data["Button 1 Link"])  # button 1 link entry
            selection[-5].insert(0, data["Button 2 Label"])  # button 2 label entry
            selection[-4].insert(0, data["Button 2 Link"])  # button 2 link
        except (KeyError, IndexError, AttributeError):
            pass

        for child in self.master.winfo_children():
            try:
                label = child.winfo_children()[0]["text"]
                entry = child.winfo_children()[1]
                if label == "Client ID":
                    entry.insert(0, data["client_id"])
                elif label == "State":  # This works
                    entry.insert(0, data["state"])
                elif label == "Details":
                    entry.insert(0, data["details"])
                elif label == "Large Image Name":
                    entry.insert(0, data["large_image"])
                elif label == "Large Image Text":
                    entry.insert(0, data["large_text"])
                elif label == "Small Image Name":
                    entry.insert(0, data["small_text"])
                elif label == "Button 1 Label":
                    entry.insert(0, data["Button 1 Label"])
                elif label == "Button 1 Link":
                    entry.insert(0, data["Button 1 Link"])
                elif label == "Button 2 Label":
                    entry.insert(0, data["Button 2 Label"])
                elif label == "Button 2 Link":
                    entry.insert(0, data["Button 2 Link"])
            except (KeyError, IndexError, AttributeError):  # Since no point failing on these.
                pass


def main():
    root = tk.Tk()
    root.resizable(width=False, height=False)
    Presence_Class = PresenceGUI(root)
    try:
        root.mainloop()
    finally:
        Presence_Class._stop_rpc()


if __name__ == "__main__":
    main()
