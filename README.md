# PopWatch
Track when Funko Pops are in stock online.

#Setup
1. pip install requests beautifulsoup4 pushbullet.py
2. Edit key.ini with your Pushbullet API Key.
2. Edit funkos list under run function, add format is [Site, Title, URL]. Currently only Hot Topic and BoxLunch are implemented.
3. Edit time.sleep value you'd like, this is how often the script will run once started.
4. I'd recommend running this script in a screen instance on a linux box.
