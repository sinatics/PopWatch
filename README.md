# PopWatch
Track when Funko Pops are in stock online.
Currently only Hot Topic, BoxLunch, Barnes & Noble, GameStop, and Walmart are implemented.

# Setup
1. pip install requests beautifulsoup4 pushbullet.py
2. Edit key.json with your Pushbullet API Key.
2. Edit pops.json and add your pops in json format.
3. (Optional) Run script with an interval in seconds (python PopWatch.py 30) to set how often the script will re-check each site.
If no interval is set the PopWatch will default to 60 seconds between checks.
4. (Optional) I'd recommend running this script in a screen instance on a linux box.
