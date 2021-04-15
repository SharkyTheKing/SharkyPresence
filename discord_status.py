import json
import sys
import time

from pypresence import Presence

from exceptions import ButtonsNotDict, FileNotFound, JSONLoadError, NoClientID, TooManyButtons

# May need to look at this later.

# handle errors w/ https://qwertyquerty.github.io/pypresence/html/doc/presence.html#presence


class SharkyPresence:
    """
    Sharky working on building a constant presence.

    Allows customability through json file information.
    Then eventually a UI program.
    """

    __author__ = ["SharkyTheKing"]
    __version__ = "1.0.0"

    def __init__(self, client, data):
        self.client_id = client
        self.rpc_data = data
        # in the in __name__ gather data and set it properly for RPC update

    def start_rpc_connection(self):
        """
        Internal function to start the RPC connection
        """

        RPC = Presence(self.client_id)
        RPC.connect()

        try:
            self.update_rpc_connection(RPC)
        except KeyboardInterrupt:
            print("Closing...")
        finally:
            sys.exit(1)
            RPC.close()

    #   Look into properly updating different statuses, rotating statuses around, etc.
    def update_rpc_connection(self, RPC):
        RPC.update(**self.rpc_data)
        print("Connected.")
        while True:
            time.sleep(25)


class PresenceInfo:
    """
    Gathers and sorts information for RPC Presence
    """

    def __init__(self):
        self.path = "data\settings.json"

    def start_info_gathering(self):
        """
        Starts getting json information

        This will attempt to sort the information.
        It'll also raise exceptions on improper file handling
        """
        try:
            data_file = self.get_file_info()
        except FileNotFoundError:
            raise FileNotFound(self.path)

        RPC_data, client_id = self.sort_json_file(data_file)

        return RPC_data, client_id

    def get_file_info(self):
        with open(self.path, "r") as text_file:
            try:
                fetch_data = json.loads(text_file.read())
            except json.JSONDecodeError:
                raise JSONLoadError

            return fetch_data

    def sort_json_file(self, data):
        """
        Properly sorts out from settings.json for RPC.
        """
        # To properly set dictionary for RPC
        # rpc_data = {
        #    "client_id": None,
        #    "state": None,
        #    "details": None,
        #    "large_image": None,
        #    "large_text": None,
        #    "small_image": None,
        #    "small_text": None,
        #    "buttons": [],
        # }
        rpc_data = {}
        client_string = None

        client_id = data.get("client_id")
        state = data.get("state")
        details = data.get("details")
        large_image = data.get("large_image")
        large_text = data.get("large_text")
        small_image = data.get("small_image")
        small_text = data.get("small_text")
        buttons = data.get("buttons")

        if not client_id:
            raise NoClientID
        # will need to figure out how to actually get a valid client_Id. Probably need to handle in the RPC connection attempt.
        client_string = client_id

        if state:
            rpc_data["state"] = state
        # Need to test if you need state & details in order for either to work.

        if details:
            rpc_data["details"] = details
        # need to explain in readme.MD if the image they use isn't an asset in their dev, it won't work.

        if large_image:
            rpc_data["large_image"] = large_image

        # need to do testing if large_image needs large_text
        if large_text:
            rpc_data["large_text"] = large_text

        if small_image:
            rpc_data["small_image"] = small_image

        if small_text:
            rpc_data["small_text"] = small_text

        if buttons:
            check_dict = True
            if not isinstance(buttons, list):
                print(
                    "\nButtons was not properly set. Please compare "
                    "your settings.json file with example_settings.json"
                    " file.\nIt must be dictionary inside a list.\n"
                )
                check_dict = False
                # Probably just going to send message back to use to explain why this failed.

            if check_dict:
                for possible_dict in buttons:
                    if not isinstance(possible_dict, dict):
                        raise ButtonsNotDict

                if len(buttons) > 2:
                    raise TooManyButtons

                # Probably check to make sure it says label and URL for the contents? Not sure.

                rpc_data["buttons"] = buttons

        return rpc_data, client_string


# Example use: d = {"state": "Click the buttons below!", "details": "testing", "buttons": button}
# To properly display
# Reminder: Assests (images) MUST have text following and MUST be apart of the developer portal.
# TODO Look into rotating statuses

if __name__ == "__main__":
    print("Starting...\n")

    print("Opening setting file...")

    data_file, client_id = PresenceInfo().start_info_gathering()

    print("Starting RPC connection...")
    SharkyPresence(client_id, data_file).start_rpc_connection()
