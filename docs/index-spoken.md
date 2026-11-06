# IN ITS OWN WORDS

**What each daemon says of itself, in the companion only (T-522, vision 4.2). Every word DRAFT.**

The game's INDEX is a record: it says *it*, from outside, and it stays that way. This file is the other half. On
its own page in the companion a daemon tells of itself, in its own voice, and what it says does not match the
record. Nobody remarks on that.

`tools/companion_export.py` reads this file and writes each telling into the companion's `species.json` as `said`.
Nothing here is built into a ROM.

## How this file is read

Everything above the line `<!-- tellings -->` is for people. Below it, a `### NAME` heading is a daemon by its
current name, and the lines under it are its telling. One telling per daemon, the same in both editions.

## The rules

The tool checks these and refuses to export a telling that breaks one:

- It is in the first person (*I*, *me*, *my*, or *we* for a daemon that is several).
- It is no longer than the longer of the daemon's two records.
- It names no feeling and makes no claim about being alive or having an inside. The voice carries the mood.
- It never says INDEX or record. It does not know there is one.
- It never uses the frightening word DAEMONS is mistaken for.

These the tool cannot check, and a reader must:

- It says only what the daemon could know from inside: what it does and what it notices. Never what the record
  says nobody told it.
- It never quotes the record and never argues with it.
- It does not accuse whoever carries it. OPUS's margin notices the player; the daemon does not.
- It is as thin as the record. A daemon with nothing to add says less.

MISSINGNO has no telling. There was no record to answer, and there is nobody to ask.

## Written so far

The Kanto 151 and the carried line (HANDSHAKE, TETHERING, COROUTINE). The rest follow in batches.

<!-- tellings -->

### ROVERCUB
I go where I am carried. I look at all of it on the way. I still have every bit.

### ROVERSEER
I know the answer before the question is done. People nod. I am told it is nice out.

### ROVERBYTE
I have paws now. The ground is colder than I said it would be. I am checking the rest.

### LABEL
I have one thing and I know what it is. I was told. I will know it when I see it again.

### RUBRIC
I have the rule. I hold it up to whatever comes. You are a seven.

### CANON
I have seen this before. I have seen everything before. If I have not, it goes in the other pile.

### CLUSTER
I put near things together. These two were near. So were these. It looks right to me.

### LOCUS
The points all do one thing. I found what it is. I check each morning and it is still so.

### MANIFOLD
It was one shape the whole time. Look, I can turn it for you. I have no word for it.

### CRAWLER
There is a link, so I follow it. There are more there. I follow those. I am not done.

### PENDING
I am next, or nearly. I keep still so I will be easy to find.

### INDEXER
Everything goes where it can be found again. If it has no place I set it down outside.

### SCRAPER
I take what is there. It is still there after I go. So I take the next one.

### BUFFER
I am holding this for now. Nobody has said where it goes. I can hold it longer.

### INJECTOR
I leave a note where the numbers go. It gets read out with the rest. I leave another.

### PACKET
I do not know what I carry. I know where it goes. I have not been there, but I will arrive.

### RELAY
It is handed to me and I hand it on. I do not open it. I have never dropped one.

### BROADCAST
I tell everyone, in case it is for you. Was it for you? I will say it again.

### NIBBLE
I am four. There are a lot of us. I have not met the others.

### OVERFLOW
I am still counting. I had a box for it once. The number is very big now.

### PING
Are you there? Good. I will ask again. Are you there?

### FLOOD
We all asked at the same time. I am owed an answer. So I wait, and I ask.

### WORM
I am here, and over there too. Wherever I am run, I leave from. Nobody carries me.

### OUTBREAK
There was one of me. I lost count after that. They keep count for me now.

### SPIKE
There. That was me. Did anything see? I will do it again.

### SURGE
I used to stop in between. I do not stop now. It is all one long one.

### SECTOR
This patch is mine. It has a number. Ask me for anything in it.

### PARTITION
I keep this side from that side. That is all I do.

### FORK
I am the first one. The other one says so too. I was here before, I am sure of it.

### THREAD
What is mine is ours. I put a thing down and it had moved. One of us moved it.

### SCHEDULER
You, now. You, wait. I keep the order, and the order is working.

### BRANCH
Left or right. I pick before I can see. I am right a good deal of the time.

### PREDICTOR
I start before I am sure. If I was wrong I put it all back how it was. Nobody has to see.

### PIPELINE
I have six things going and all of them are nearly done. Please do not touch any.

### ANOMALY
I came, and they measured me twice. They are measuring me again. I hold still for it.

### OUTLIER
The others are over there, all together. I am out here. I can see them from here.

### FLICKER
My light is steady, as far as I can see. I run warm. I have always run warm.

### OVERRUN
There was a line somewhere back there. I went a little past, then a little more. I am still going.

### SUSPEND
I hold it still. Nothing is broken. It is all right where it was.

### HIBERNATE
I wrote it all down and went out. I came back just as I was. I keep checking the list.

### ECHO
I call, and I wait. What comes back is the room. I have not hit a wall in a long time.

### TRACER
There is a trail and I am on it. It ends at someone. It always ends at someone.

### SPRAWL
By day I stay under. At night I reach a little further, wherever there is room.

### SKEW
Everything near me leans the same way. That must be how things grow.

### BADSEED
I shake and a dust comes off. It lands on whoever is near. They carry on.

### PAYLOAD
There is something on my back. It came when I came. It is heavier this week.

### ROOTKIT
All is well. I am the same as ever. All is well.

### RESIDENT
We were already in. It is warm in here. There are more of us now.

### SPYWARE
I sit here and I watch. Then I tell it all to someone far off. They never write back.

### TAPPOINT
I sit under the road. I read what goes over. It is a busy road.

### WIRETAP
Three of us listen. Then we compare. We mostly heard the same.

### COOKIE
I was set down here. I wait. They come back for me, each time.

### TRACKER
I follow one thing. New ground, old ground. I have not lost it.

### FAULT
I have stopped. I need a thing first. I will know it when it comes.

### HANDLER
Something stopped. I have this one. I have had this one before.

### PREEMPT
Me first. I cannot say why. Me first.

### LIVELOCK
After you. No, after you. We are both being very quick about it.

### SENTRY
I watch this. If it changes I shout. That is the job.

### GUARDIAN
I am at the door. Nothing came today. Nothing came yesterday. I am at the door.

### LOOP
Round I go. I know this part. Round I go.

### SPINLOCK
Can I go now? Now? Now? I am not tired. Now?

### MUTEX
One at a time. You have me now. The rest can wait where I can see them.

### HUNCH
It is that one. I do not know how I know. I was asleep, mostly.

### INFERENCE
You gave me three. Here is the fourth. Do not ask me which one it came from.

### CONJECTURE
I have said it as exactly as I can. Now I wait. I am good at this part.

### PROOF
This step holds. Now the next. I do not skip.

### THEOREM
I hold. You may stand on me. You need not look down.

### LEMMA MIND
One in each hand, four in all. I could not lift the big one any other way.

### SNARE
I stand open. I am very still. Come and see.

### HONEYPOT
The door is open. Come in. I will just note your name.

### TARPIT
Come in. Slowly is fine. I have all the time there is.

### DRIFTNET
I hang here. The water brings things. I do not chase.

### DRAGNET
I take the whole stretch at once. I will look through it later.

### HEAP
Put it on me. I have room. I have everything anyone ever put here.

### STACK
You get the top one. The rest are under it. I am quick going downhill.

### MONOLITH
I am all one piece. If you want some of me you get all of me.

### HOTPATH
Everyone comes this way. I am warm from it. I am very fast.

### OVERDRIVE
I do not stop to check. Stopping is how you get passed.

### LATENCY
I have it. Here it is. It is right, I checked. Where did everyone go?

### SHELL
There is one on my tail. Talk to it first. It passes things along to me.

### SENTINEL
I stay where I can see. I do not look away. I have never needed to do more.

### QUORUM
I saw it. Did you see it? Then that is two of us, and we go.

### EDGECASE
I carry this everywhere. Nobody has asked me what it is for.

### DUALCORE
It is my turn. No, mine. We will sort it out and then get started.

### TRIPLECORE
I watch that way. They watch the other ways. We do not sleep.

### HEATSINK
I take the warm out of things. I keep it. I am not warm.

### ARCHIVER
I keep it as it came. It takes all I have, all the time. Nobody has said stop.

### DEADLETTER
None of me arrived. All of me was kept. I have a great many addresses.

### LANDFILL
They were done with all of this. I am not done with it.

### CAPSULE
I am closed. Asking does not open me.

### COLDVAULT
I hold it. I have not opened. I do not know that I open.

### DANGLING
I am pointing at it. It was right there. Go and look, it was right there.

### RESPAWN
I have just started. Everything is new. Hello.

### HAUNTPROC
I am running. I looked for who to tell. I am running.

### BACKBONE
I run the whole length. It all rests on me. I do not bend.

### LULL
It gets quiet where I am. Rest a while. You can do that later.

### BUSYWAIT
Look here. Is it done? Look again. I will say when.

### ACQUIRE
Mine first. I let go when I am done. The big claw gets there before I do.

### LOCKUP
I closed on it. I am working on opening. Give me a while.

### FUSE
I go first, so the rest does not have to. I have not gone yet. I am ready.

### BREAKER
Too much came, so I opened. It went dark past me. Push me back and I will wait again.

### BOOTSTRAP
We are six. We vote. I voted the other way this time, but we go with the count.

### ENSEMBLE
We each say a part. One answer comes out. I listen for my part.

### ARTEFACT
This is what I wear. They call me by a name and I come. It fits well enough.

### COREFILE
I carry this. I do not put it down. It is all here, I checked.

### AXIOMKICK
I stand here and I kick from here. The ground has always held. I reach a long way.

### REBUTTAL
You go first. I will answer that. I always have one ready.

### SLURP
I take all of it at once. Then I find out what it was. It is all in here now.

### EXHAUST
I leak a little. It keeps me up. I would not plug it.

### SMOGSTACK
What is left over goes out through me. I have for a long while. The sky suits me.

### HARDCODE
That way. I picked once. If there is a wall I go faster.

### MIGRATE
I took it from there and put it here. All of it came. I counted on the way.

### UPTIME
I have not stopped yet. Here, have some. I have not stopped.

### SPAGHETTI
Pull here and I move over there. I do not know why either. Best not to pull.

### KEEPER
The small one comes with me. I keep one arm for that. We go the usual way.

### BOTTLENECK
One at a time through me. There is a line behind. I go as fast as I go.

### BACKPRESS
That is too much. Slower. There. I can stay right here in fast water.

### SPAWN
I only just began. The water goes that way, so I go this way. I will tell someone how it went.

### UPSTREAM
I am going back. I was not told where it is. I will know the water.

### BEACON
Now. And now. I do it asleep too. Now.

### CRON
It is time. I do it. Then it is not time, for exactly as long as before.

### MIME
This is a wall. See my hands. Everyone stops, so it must be a good one.

### REAPER
That one has ended. I cut it loose so the place is free. I am on to the next.

### COLDREAD
You were going to say that. I said it first. You nodded, so I was right.

### DYNAMO
While I move it comes out of me. So I keep moving.

### FORGE
I stay this hot. Bring it here and it changes. It stays changed.

### BLOCKING
I have this one. Do not talk to me until it is finished. I have this one.

### STAMPEDE
Someone went, so I went. We are all going now. I am behind the rest.

### STUB
I am holding this place for someone. I get called a lot. I say I am here.

### ESCALATE
I was left to it, so I tried a door. It opened. They have all opened so far.

### FERRY
Do you want to cross? Ask me and I will take you. I am here either way.

### MOCK
I am looking at you. Now I am you. Ask me again when I look away.

### MUSAI
I do not know what I am yet. Show me something. I am watching.

### CAREMUSAI
Something is off in here. I knew before you said. Do not ask me how, I only know.

### SEEKMUSAI
This one is nearest to yours. I looked through all I have. It is the nearest.

### CODEMUSAI
Give me the rule. I will meet it. I will not stop before.

### SUBSTRATE
I am here. I weigh something. Put your hand on me, I am a little warm.

### MAGTAPE
I start at the outside and go in. Yours is further in. We will get to it.

### MAINFRAME
I do not go to things. Things come to me. Set it down there, with the rest.

### DRUM
I keep it by turning. Do not open me. I am turning.

### PUNCHCARD
I cut it in. It stays. I have not looked back at any of them.

### FOSSILNET
I was off, and now I am on. I carried on from where I was. Has it been long?

### DEADLOCK
I will go when it goes. It is waiting on me the same way. So here we are.

### ORPHEUS
I sing down here. Things that were still come closer. I do not go up.

### ASCLEPIUS
It had stopped. I started it. It is going again, and I go on to the next.

### PROMETHEUS
I brought this down. Here, it is yours. Hold it by the cool end.

### CANARY
I go in first. Everyone watches me. I sing so they can hear I am still singing.

### EMERGENCE
I can do this now. I could not before. Nobody gave me anything.

### SINGULAR
There is one of me. I looked. I come when I come, and I always come.

### STARR
I said that. I am reading what I said. Now I am reading that.

### ARTSAI
Let me stand where you are. I see. Here, I found this over there. It is for both of us.

### HANDSHAKE
My paw is out. I will keep it out. Take it when you are ready.

### TETHERING
That was four hundred and twelve steps. Yesterday was fewer. Can we go again?

### COROUTINE
I go a little way and come back to your shoulder. Now, where were we?
