[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)
# SharkyPresence
A project I decided to take up on after finding out about [PyPresence](https://github.com/qwertyquerty/pypresence). Know that this is a massive work in progress code. All rights for the Library belongs to [PyPresence](https://github.com/qwertyquerty/pypresence).

This readme is a work in progress.


## Install the requirements:
* [Python 3](https://www.python.org/downloads/)
* Install the requirements using:
```
> pip install git+https://github.com/SharkyTheKing/SharkyPresence@fr/setupcfg-configuration
```

## Run the app:
```
> sharkypresence
```

> You should now have a neat lil' window with a buncha empty text boxes (hereforth refered to as the '**App**'). We still have to set the right values and hit the `Start` button for it to work!


## Fill out them text boxes:

1. Head over to [Discord's Developer Applications](https://discord.com/developers/applications) page. In the top right, click `New Application`; give it a nice name - we're gonna use "My Test Game" for ours. In Discord's user pane, this will show as your status "Playing **My Test Game**".
2. Copy the `Application ID` from the website and paste that value into the `Client ID` in our App.
3. In the website, on the left of the page, navigate to `Rich Presence`. The `Cover Image` is not used and we can ignore it. Next, add a few images with the `Add Image(s)` button; rename the images if needed, then click `Save Changes`. *It may take several minutes for the images to properly save on discord's servers. Refresh the page and verify that the images are still there.*
4. In our App, the `Large Image Name` and `Small Image Name` can be set to any image name that has been uploaded in the step above.
5. The remaining fields in our app can be set to anything you desire:

**Note:** *Large & Small Image Text is the text that displays if you hoover over the image in discord*

**Note:** *You cannot click a button on your own profile - it only works if another user click the button (so get a buddy to help you verify the button works!)*

## Making it show on discord
1. Launch Discord desktop app.
2. Make sure the Game Activity is enabled (Discord Settings -> Activity Status -> Display current activity as a status message)
3. In the App, click the `Start` button.

**Note:** *If you restart Discord, you may need to restart the *App.
