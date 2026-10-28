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
4. **Bring it home** the same way, reversed. It comes back with the friendship it built while it was away -- and, if
   it crossed the line while it was out there, evolved: the companion applies the game's own rules for level,
   friendship and the hour, and the game finishes the change when the save is next loaded.

In the game an AWAY daemon is shown washed out -- in the party, the PORT and its summary -- so it is never lost. It
can't battle, be traded or be released while it is away, and if the companion can ever not be reached, the game can
call it home on its own.

## Where it can live

- **Your phone (the happy path).** The companion's app runs as a site in your browser and as an iPhone and iPad app
  from the same code, and on the iPhone a daemon can live on your home screen as a widget of its own, with DRINK, FEED,
  TRAIN and, at bedtime, SLEEP.
- **A watch.** The LilyGO T-Watch S3 and the bigger **T-Watch Ultra**, which knows when you sleep and when you walk,
  wakes you gently, reads you the books, and holds a card to its NFC ([The T-Watch Ultra](https://github.com/CodeMusic/daemons-companion/wiki/The-T-Watch-Ultra)).
- **A board.** Most LilyGO and M5Stack boards can host one: the LilyGO T-Embed family, the T-Watch S3, the T-Deck,
  the T-Display-S3 Pro and AMOLED; the M5StickS3, the StickC-Plus (which, with its thermal HAT, **sees heat**), the
  CoreS3, M5GO, Fire, Dial and Cardputer; and the M5Stack Tab5 as a control center. The daemon is drawn as the game
  draws it, and its routines from the game come along.
- **Your home.** An ESP32-S3-BOX-3 running Home Assistant's own voice assistant can wear the daemon as its face.

Everything runs **on your own machine**: a local server, no accounts, no hosting. The phone can also host on its own,
with no computer, taking the save from an emulator on the same phone (built; still being checked on a real phone).

**Or a hub that never sleeps.** A small Linux board at home -- an M5Stack CoreMP135 -- can be the companion's server,
serve its site and pair a phone from its own screen. Stacked on it, an **AX630** AI board hears, thinks and speaks for
every daemon in the house: it talks as your daemon, tells its dreams, and answers as THE GUIDE once you have found it.
No device waits on it, and when it is busy the talk goes to your own n8n
([The hub and its AI](https://github.com/CodeMusic/daemons-companion/wiki/The-hub-and-its-AI)).

## The one app

**The game and the companion in one app** (internal and in testing). On an iPhone or an iPad, give the app your own
*FireRed* or *LeafGreen* once: it fetches the matching DAEMONS patch, applies it on the device, checks the result, and
plays the game in a GAME tab. **The game's save is the companion's** -- showing the companion pauses the game, SEND
and SYNC write the save, and the game carries on from it. On an iPad on its side, the game and the companion sit side
by side, and a NOTEBOOK page just filed or the INDEX card of a daemon just met opens next to the game. A newer release
is one tap. A Mac version is coming. In a browser, [daemons-playground](https://github.com/CodeMusic/daemons-playground)
plays the game with the companion in a tab ([The one app](https://github.com/CodeMusic/daemons-companion/wiki/The-one-app)).

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
  NATIVE line -- only what your save has already reached. In the app the INDEX card is whole, and takes its colour as
  your save comes to understand that kind of daemon. **THE ROAD AHEAD** shows the next step and the fights and places
  open to you, and never anything past the next step.
- **Nights and dreams.** A watch keeps the night -- tucked in, or, on the Ultra, just still -- and in the morning your
  daemon has had a dream: deep, quiet or restless, read aloud if you like, kept in a journal. At the next SYNC the last
  dream goes home into your save, for the game's **ITS DREAMS**. A good week shows on the daemon, subtly
  ([Nights and dreams](https://github.com/CodeMusic/daemons-companion/wiki/Nights-and-dreams)).
- **SOUNDINGS.** Each SYNC writes how each daemon away is doing into your save, for the game to hear, and the app
  shows a quiet card for each: when it was last heard, and how it was. Never a score.
- **THE SUBTLE LAYER, out here too.** Once your save holds the book, the daemon on a watch sometimes notices something
  first; a read now and then, a lean at the CASINO's reels. The companion judges each by what happens after and keeps
  the count. It never vouches.

## More

The companion has its own repository and its own wiki, with how to start it, which boards run today, and how to flash
them:

- [CodeMusic/daemons-companion](https://github.com/CodeMusic/daemons-companion)
- [The companion's wiki](https://github.com/CodeMusic/daemons-companion/wiki)

The companion holds nothing of Nintendo's. It reads a DAEMONS save; it never needs a ROM.
