class FileNotFound(Exception):
    """
    This is used after FileNotFoundError on fetching the file.
    """

    def __init__(
        self, path, message="Is not the file we're looking for. Please read the README.MD file."
    ):
        self.path = path
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"\n\n{self.path}: {self.message}"


class JSONLoadError(Exception):
    """
    This is used after JSONDecodeError on attempting to load the file contents into Json.
    """

    def __init__(self, message=None):
        self.message = (
            "\n\nUnable to properly load the settings.json file.\n"
            "Please compare your settings.json file "
            "with example_settings.json file.\n"
            "For more documentation for pypresence, please review\n"
            "https://qwertyquerty.github.io/pypresence/html/doc/presence.html#update"
        )
        super().__init__(self.message)

        def __str__(self):
            return self.message


class NoClientID(Exception):
    """
    If there's no Client ID. Completely Fail and Kill program

    In order for RPC connection, we need a Client_ID for the application through discord.com/developers
    """

    def __init__(self):
        self.message = (
            "\n\nWARNING: No Client ID listed in settings.json.\n"
            "You MUST have a client_id from your application for this program to work.\n"
            "Please read the README.md file to review how to get your ID."
        )

        super().__init__(self.message)

    def __str__(self):
        return self.message


class ButtonsNotDict(Exception):
    """
    If the object is not a dictionary
    """

    def __init__(self):
        self.message = (
            "\n\nINFO: Your buttons are not a proper format."
            " Please review the README.md file on this."
        )
        super().__init__(self.message)

    def __str__(self):
        return self.message


class TooManyButtons(Exception):
    """
    If there are more than 2 buttons
    """

    def __init__(self):
        self.message = (
            "You can only have two buttons.\n"
            "Please adjust your settings.json file."
        )

        super().__init__(self.message)

    def __str__(self):
        return self.message
