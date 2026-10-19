# The companion

**Your daemons can leave the game.**
[**daemons-companion**](https://github.com/CodeMusic/daemons-companion) is a goal companion that carries a daemon
from your game of DAEMONS into the real world. You feed it, train it and spend time with it, and you can talk with it.
Tell it what you want to get done and it turns that into **one next step**, and walks you through the day. As you get
things done, it thrives.

## How a daemon gets there

1. **Load your save into the companion** (a copy of it). Its first SYNC lets the game know about it, and from then on
   a party daemon's menu in the game offers **SEND**.
2. **SEND** a daemon from your party. The game saves; the companion reads the save and marks the daemon **AWAY**.
3. **The daemon is hosted** on a device of yours. With more than one device, each can host a different daemon from
   your party -- one daemon to one device, and moving it to another device moves it.
4. **Bring it home** the same way, reversed. It comes back with the friendship it built while it was away.

In the game an AWAY daemon is shown washed out -- in the party, the PORT and its summary -- so it is never lost. It
can't battle, be traded or be released while it is away, and if the companion can ever not be reached, the game can
call it home on its own.

## Where it can live

- **Your phone (the happy path).** The companion's app runs as a site in your browser and as an iPhone app from the
  same code, and on the iPhone a daemon can live on your home screen as a widget of its own, with DRINK, FEED, TRAIN
  and, at bedtime, SLEEP.
- **A board.** Most LilyGO and M5Stack boards can host one: the LilyGO T-Embed family, the T-Watch S3, the T-Deck,
  the T-Display-S3 Pro and AMOLED; the M5StickS3, the StickC-Plus (which, with its thermal HAT, **sees heat**), the
  CoreS3, M5GO, Fire, Dial and Cardputer; and the M5Stack Tab5 as a control center. The daemon is drawn as the game
  draws it, and its routines from the game come along.
- **Your home.** An ESP32-S3-BOX-3 running Home Assistant's own voice assistant can wear the daemon as its face.

Everything runs **on your own machine**: a local server, no accounts, no hosting. The phone can also host on its own,
with no computer, taking the save from an emulator on the same phone (built; still being checked on a real phone).

## What it does with your game

- **THE CASINO.** Every board has SLOTS -- and so do the phone, the site and the Tab5: three reels of your own party.
  **The coins are your game's money** -- the companion starts from what your save holds, and the next SYNC writes what
  was won or lost into the save, never below nothing and never past 999999. The odds move with the day, between 90 and
  100 back for every 100 bet: a holiday, the weather where you are, the hour and the season, as the game's own GAME
  CORNER does. THE HOUSE says today's odds and why; THE TABLE shows who else is playing, and a big win is called out.
- **The game's own voice.** On the phone, the site and the Tab5 every tune plays on the instrument your save's edition
  has -- DAEMONS' own harp for CONTENT, its flute for CONTEXT.
- **Experience.** Every step of a goal you finish feeds the daemon and gives it experience, which comes home with it.
- **Your save, to read.** The app, the site and the Tab5 show YOU (your MARKS, ROOTS, the regions you have seen, the
  hidden places you have found, the story so far), a LIBRARY (CALLOW SCHOOL and your DIPLOMA, THE GUIDE and THE SUBTLE LAYER once found -- see [Books](Books) -- the
  NOTEBOOK, the SONGBOOK's songs on a staff in their colours, and STREAM's lessons), and the INDEX with each daemon's
  NATIVE line -- only what your save has already reached.

## More

The companion has its own repository and its own wiki, with how to start it, which boards run today, and how to flash
them:

- [CodeMusic/daemons-companion](https://github.com/CodeMusic/daemons-companion)
- [The companion's wiki](https://github.com/CodeMusic/daemons-companion/wiki)

The companion holds nothing of Nintendo's. It reads a DAEMONS save; it never needs a ROM.
