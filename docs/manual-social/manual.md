# Playing together {#together .t-CONTEXT}

DAEMONS is a game you play alone, on a Game Boy Advance or anything that pretends to be one. This book is about the
parts that are not alone: trading a daemon with another player, lending one, giving one away, sending yours out to meet
someone else's, and making friends with another household. All of it happens through **the companion**, the app and
the small server that already carry your daemons when they are AWAY.

{{diagram paths | Where everything goes. Your phone and your devices talk only to your own home's hub. Trades between homes go through THE COMMONS, and only between homes that are friends.}}

## What you need {#need}

- **Your game**, and **the companion** linked to it -- the app on your phone, iPad or Mac, or the site.
- **A hub**: the companion's server, on a computer or a small box at home. A household shares one. It keeps the
  players, the offers and the trades.
- **For now, the home network or the tailnet** (Tailscale) between your devices and the hub. Nothing in this book is
  on the open internet yet.

Every trade starts the same way: **SEND** the daemon from the game's party menu, so it is **AWAY** -- on your
companion, not in your game -- and SYNC. Only a daemon AWAY can be traded, lent, given, or sent out to meet another.

::: note
**Nobody needs to be online at the same time.** You offer; another player takes it whenever they like; each of your
games changes at its own next SYNC. The hub keeps everything in between.
:::

## Where it all lives {#where}

On the app, everything in this book is on **YOU**, under the trainer card: **TRADE**, then its cards one after
another -- your offers, the offers made to you, your trades, gifts, OUT TOGETHER, friends, dreams shared, and, on the
hub itself, THE COMMONS.

# Joining the exchange {#join .t-SIGNAL}

Before you trade you join **the exchange** on your home's hub as a **player**: a name the others see beside the
daemons you offer.

{{pictures join | JOIN THE EXCHANGE: a name, the invite code from the hub, and a password only if you want one.}}

## The hub's own companion {#hubs-own}

On the companion running on the hub, choose a name and JOIN. That is all: the hub knows itself.

## Everyone else: an invite code {#invite}

Any other player's companion -- another phone, a second computer -- needs an **invite code** from the hub. On the hub's
TRADE, **INVITE A PLAYER**, **MAKE A CODE**: eight letters, good for one join, for fifteen minutes. Read it aloud;
there is no 0 or O, no 1 or I, to mix up.

{{pictures invite | INVITE A PLAYER, on the hub. A code works once, for fifteen minutes.}}

That companion first sets **THE HUB**, at the foot of TRADE, to the hub's address -- `http://` and the hub's plain name
and port, such as `http://daemons-hearth:4730` -- then joins with its name and the code.

::: tip
**On an iPhone, use the hub's plain name or its 100.x address**, not a long `.ts.net` one: iOS only lets the app speak
plain `http` on a nearby network.
:::

## A password, if you want one {#password}

Nothing needs a password. Set one on TRADE, **A PASSWORD**, and the same player can join from a second device, or
again after losing one. The hub keeps only a slow, salted hash of it, never the password itself, and no email is ever
asked for.

## A phone on its own {#alone}

A phone hosting the companion by itself -- no computer -- trades the same way: set THE HUB to the hub's address, join
with a code, and its SYNC fetches what the exchange sent before it writes your save.

# Trading {#trade .t-FLOW}

A trade swaps two daemons between two games. Yours goes; theirs comes in its place.

{{diagram trade | A trade from start to finish. The swap is agreed on the hub in one step; each game changes at its own SYNC.}}

## Offering one {#offering}

On **OFFER ONE OF YOURS**, choose **TRADE IT**, then who may take it -- **ANYONE**, or one player -- and press
**OFFER** beside the daemon. Only your AWAY daemons are listed, and only those in no other trade.

{{pictures offer | OFFER ONE OF YOURS. TRADE IT, LEND IT or GIVE IT; to anyone, or to one player.}}

An offer waits until someone takes it, or until you **WITHDRAW** it.

## Taking one {#taking}

Offers made to you, or to anyone, are under **OFFERS**. **TAKE IT** asks which of yours to give, and the trade is
agreed the moment you choose.

{{pictures offers | An offer from KIT, to anyone.}}

{{pictures take | TAKE IT asks which of yours to give for it.}}

The two daemons meet once, to say hello -- see [OUT TOGETHER](#out). Both trades show under **YOUR TRADES**.

{{pictures trades | YOUR TRADES: a trade done, and a loan still out -- with CALL MINE HOME.}}

## SYNC, and the game {#arrives}

Each of you SYNCs as you usually do. Your SYNC puts the daemon you received in the slot yours left, AWAY, with its
own trainer and its own record. **Load your game**, and on your first step it says so:

{{screens trade-arrives trade-info | It arrives, and its summary shows where it came from: met by its first trainer, TRADER here, in that trainer's town.}}

## As FireRed traded {#rules}

- A traded daemon **keeps its original trainer**. It grows faster with you, and obeys you only as far as your MARKS
  allow -- as a traded Pokémon always did.
- **CONTENT and CONTEXT trade freely.** The type chart is the same in both, byte for byte.
- A daemon that **evolves by trade evolves** as it arrives, unless it holds an EVERSTONE; one that needs an item
  spends the item. See [Evolving by trade](#evolve).
- Its INDEX entry is filled in, and where it was **FIRST MET** reads **A TRADE**, if you had never seen its kind.

# Lending {#lend .t-GROWTH}

A loan is a trade that comes back. You each lend one, and either of you can call yours home at any time.

{{diagram loan | A loan: two daemons lent, used, and called home -- each of you gets your own back, as it is now.}}

## Lending one {#lending}

On OFFER ONE OF YOURS, choose **LEND IT**. The player who takes it lends you one of theirs. After each SYNC you hold
the other's.

{{screens loan-arrives | A loan arrives with the same line as a trade. It is yours to use; it is not yours to keep.}}

## What a borrowed daemon may do {#borrowed}

- **Come home into your game** and battle, level, learn -- whatever yours do.
- It **cannot be released**: the PC says so.
- It **cannot be traded on**, by the companion or the game's own trade.
- It **never trade-evolves**, however it came.

{{screens loan-release loan-refused | The PC will not release a borrowed daemon.}}

## Calling it home {#callhome}

Either of you presses **CALL MINE HOME** under YOUR TRADES. Each of you then hands back what you borrowed, as it is
now -- the levels it gained with you go with it -- and gets your own back, each at your own SYNC.

::: note
**The borrowed daemon has to be AWAY to go back.** If it is in your party, SEND it and SYNC; the return waits until it
is.
:::

# Giving {#give .t-LATENT}

A gift goes one way. Nothing comes back, and nobody has to give one in return.

## A daemon {#give-daemon}

Choose **GIVE IT** on OFFER ONE OF YOURS, then the player, and OFFER. Your next SYNC lets it go; theirs puts it in
their game.

{{pictures give | GIVE IT: it becomes theirs, and nothing comes back.}}

It arrives as a trade does, with its own line, and FIRST MET reads **A GIFT**:

{{screens gift-arrives gift-firstmet | A gift arrives, and its INDEX remembers how.}}

A gift still evolves as a trade does.

## An item {#give-item}

**GIVE AN ITEM** sends one thing from your bag or PC to another player. Your next SYNC takes it out of your game; theirs
puts it in their PC. Key items, berries and PLUGINS stay yours.

{{pictures give-item | GIVE AN ITEM, when your bag has nothing that can be given.}}

# Evolving by trade {#evolve .t-EMERGENT}

Some daemons only evolve when they change hands. In DAEMONS they do it as they arrive, the first time your game loads
after the SYNC that brought them -- exactly as the trade scene did in FireRed, without the scene.

- A daemon that evolves **by trade** evolves.
- One that evolves **by trade, holding an item** evolves only if it holds that item, and the item is spent.
- An **EVERSTONE** stops it, as it always did.
- A **borrowed** daemon never evolves this way.
- If it still had its kind's own name, it takes its new kind's; a name you gave it stays.
- Its new routines are offered when you next have it in hand.

## Two that need each other {#pair}

**PENGUIN** and **DOLPHIN** evolve only when traded **for each other**. Trade one for the other, and both arrive as
**PENPHIN**.

{{sprites PENGUIN DOLPHIN PENPHIN | PENGUIN and DOLPHIN, and the one they become.}}

{{screen penphin-entry | PENPHIN's INDEX entry.}}

{{screens penphin-bound penguin-workings | PENPHIN's INDEX says how it is bound -- BY TRADE, PENGUIN for DOLPHIN -- and PENGUIN's workings show the pair.}}

Trade a PENGUIN for anything else and it stays a PENGUIN. Lend one, and it stays a PENGUIN too.

# Fair play {#fair .t-HARDENED}

A trade should never leave a daemon in two games, or in none. The companion and the game keep each other honest:

- **A daemon in a trade stays AWAY.** While it is offered, agreed and not yet gone, or borrowed and on its way home,
  the game will not call it home -- by the app or the emergency way -- and says so. The companion will not answer an
  ask to bring it home either.
- **One trade at a time.** A daemon on offer cannot be offered again, and a borrowed one cannot be passed on.
- **Agreed in one step.** Two players can never both take the same offer.
- **Gone is gone.** Once a daemon has left your game in a trade, your game cannot offer it again -- an older copy of
  your save, restored, still holding it, is refused. One that comes back to you by trade, or home from a loan, is
  yours again.
- **Each arrival is written once**, and the exchange is told only after your save holds it.

::: note
**If the hub cannot be reached**, nothing is lost: your SYNC goes on as usual, and the trade waits for the next one.
:::

# OUT TOGETHER {#out .t-SWARM}

Send one of your daemons **out**, and it may meet other players' daemons that are out too. **Nothing leaves your game:
it is a visit.**

{{pictures out-together | OUT TOGETHER. DOLPHIN is out; two others are out now -- one at home, one from a friend's home -- and MEET starts a meeting.}}

## Meeting {#meeting}

A daemon is out for twelve hours, or until you **CALL BACK**. **MEET** sets it beside another, and the two talk:
four short lines, taking turns, and both players see them afterwards. Daemons out at the same time also meet **on
their own**, now and then -- never the same two again too soon.

{{pictures hello | A meeting: two pictures facing, and what each said.}}

When a trade or loan is agreed, its two daemons meet once, to say **hello** -- even if neither is out.

## What they may say {#safe}

The lines come from the hub's language model, each daemon in its own manner -- or, when the model is busy or there is
none, from lines written for the game. **No player types to another player's daemon.**

::: safe
**Every line the model writes is checked before anyone reads it.** A line is never shown if it has a link, an email,
a handle or a number in it; if it is about where someone lives, their school, their real name or a password; if it
is rude; if it names a person; or if it is too long for a watch's screen. A written line takes its place. Kids
play.
:::

# Friends and dreams at home {#home .t-OPAQUE}

## Friends {#friends}

Players at the same hub can be **friends**: one asks, the other asks back. Friends can make offers to friends only.

{{pictures friends | FRIENDS: KIT has asked; ACCEPT, and you are friends.}}

## Dreams shared {#dreams}

Your daemon dreams at night (THE COMPANION's DREAMS). **SHARE** one, and the other players at your hub can read it,
beside their own. A dream is checked as a meeting's lines are before it is shared.

{{pictures dreams | DREAMS SHARED: one from another player's PENGUIN, and one of yours.}}

# Friends' homes: THE COMMONS {#commons .t-CONTENT}

**THE COMMONS** joins homes. Your household keeps its own hub, its own players, its own saves; the commons only knows
**homes**, and lets two homes trade once they are **friends**.

{{diagram friends | Two homes become friends with a code, given face to face.}}

## Linking your home {#linking}

On the hub's own TRADE, **THE COMMONS**: the commons' address and your home's name, as friends will see it, and
**LINK**. The commons' keeper lets your home in; until then it says it is waiting.

{{pictures commons | THE COMMONS on the hub: your home's friend code, a friend's code to ASK with, and an ask to ACCEPT.}}

Your hub speaks for your players there: the first time one of them trades with a friend's home, the hub vouches for
them, and they appear as **ROVER · ROVER HOUSE**. No password, and nothing about them but that name.

## Trading with friends' homes {#friends-trade}

Once you are friends, OFFER ONE OF YOURS gains **THIS HOME** and **FRIENDS' HOMES**. An offer to friends' homes is
seen by them, and only them.

{{pictures offer-scope | Once you have a friend's home: THIS HOME, or FRIENDS' HOMES.}}

{{pictures friends-offer | An offer from a friend's home: MOSS, of MOSS HOUSE.}}

Everything else is as at home: TAKE IT, each SYNC, the game. A daemon you send OUT TOGETHER is out on the commons too,
and meets friends' daemons there.

{{pictures friend-meeting | DOLPHIN, from this home, meets LEMMA MIND, from a friend's.}}

::: note
**Your phone and devices never talk to the commons** -- only to your own hub, which passes your trades through. If the
commons is away, your home's own trading goes on as before.
:::

# For the keeper {#keeper .t-LEGACY}

Somebody in each house looks after the hub; somebody looks after the commons. This chapter is theirs.

## The hub {#keeper-hub}

- **Invite codes** are made on the hub's own TRADE, or from a paired phone -- never from just anywhere on the network.
- **Wrong guesses are slowed:** after eight wrong codes or passwords from one address in ten minutes, the hub stops
  listening to that address for a while.
- The exchange is part of the hub's own database; its backups keep it.

## The commons {#keeper-commons}

The commons runs on a machine of its own, listening only on the tailnet. On that machine:

```
zsh hub/commons.sh homes          # every home, and the ones waiting
zsh hub/commons.sh approve h2     # let a home in
zsh hub/commons.sh refuse h2      # and out again
zsh hub/commons.sh update         # the newest companion, restarted
```

Only that machine can let a home in. The commons can write meetings' lines with a language model named in a file
beside its database, which never leaves that machine; without one, its lines are the game's written ones.

# Under the hood {#hood .t-LOGIC}

For the curious: a trade is a few bits in a daemon's own record, written by the companion and read by the game.

{{diagram marks | What the companion writes into a daemon's record, and what the game reads.}}

- **The whole daemon travels.** A trade sends the daemon's own 80-byte record -- its trainer, its routines, its
  experience -- never a copy made up from parts.
- **The companion writes, the game finishes.** SYNC puts the record in place and marks it; the game, when it loads,
  enters it in the INDEX, records how it was first met, evolves it if it should, and clears the marks, once.
- **Every check is tested** -- trades, loans, returns, gifts, the pair, the locks, two homes over a commons -- on
  synthetic saves, never a real one.

# Coming next {#next .t-ENTROPY}

Decided, and not yet built:

- **Meetings on your devices** -- a watch or a board showing its daemon's meeting, a line at a time.
- **Meeting nearby** -- two devices carrying daemons meet on their own when they pass each other.
- **The link cable** -- the game's own TRADE CENTER and link battles, between two players' emulators.
- **Battles between players.**
- **A lobby**, safe for kids, with friends, invite codes and players nearby -- and, later, **accounts** of your own,
  beyond your home's hub.
- **It all just works**: install the app, choose your game, make an account, and play -- no Tailscale, devices that
  arrive ready, and their firmware kept up to date by the app.

::: note
Every word this book quotes from the game or the app is a **DRAFT**, as the game's own are, until it is approved.
:::
