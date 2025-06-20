#🎧 Spotifetch

>   WARNING: installation is still broken, running the install script does absolutely nothing. I'll fix it eventually. Maybe.

## What is Spotifetch?

Spotifetch was a fun little project I made thinking — "wouldn’t it be hilarious if we had neofetch… but for Spotify?"
It’s completely useless, and just meant for aesthetic vibes or showing off to your Discord friends.


## Dependencies

You'll need these, installed inside your virtual environment or globally (on Windows) just run:

```
pip install spotipy flask pkce requests
```

## Windows Installation (Easiest)

*Don't run the installation script, it won't even work it's shell script*
Do this instead


Clone the repo:
```
git clone https://github.com/yourusername/spotifetch
cd spotifetch
```

Install the dependencies:
Open PowerShell or CMD and run:
```
pip install spotipy flask pkce requests
```
run it with

```
python spotifetch.py
```


## Ubuntu / Linux (Super Complicated)

Unfortunately, Linux support is technically broken because spotipy isn’t in APT and you can’t install Python packages globally anymore (thanks to, PEP 668)

But if you're desperate for some reason, do this:

1. Clone the repo
```
git clone https://github.com/yourusername/spotifetch
cd spotifetch
```

2. Create a virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies manually:

```
pip install spotipy flask pkce requests
```

4. Run it:

```
python spotifetch.py
```

If you want to be fancy and pretend it's a command:

alias spotifetch='source ~/spotifetch/.venv/bin/activate && python ~/spotifetch/spotifetch.py'

Then reload your terminal:
```
 source ~/.bashrc
```

🛠 Future Fixes (copium)

    I’ll fix the install.sh script when my brain stops leaking.

    Proper support for Linux packaging… someday.

    Maybe a .deb package? Maybe not.

🐸 Final Thoughts

Don’t expect this to change your life. It prints your Spotify stats next to an ASCII logo. That’s it. It’s dumb. I love it.

Pull requests welcome.
Bugs ignored affectionately.