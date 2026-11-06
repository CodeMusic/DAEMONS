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

Every daemon with a record of ours: 397, in two batches (the Kanto 151 and the carried line first, the rest the
same day). The eight NEXUS residents are at the end; they are the ones most the user's own to rewrite.

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

### PRIMER
I eat what I ate before, a little harder each time. I always know what it will be.

### SYLLABUS
I lay them out in a row and eat them in order. This one is next. That one is later.

### CURRICULUM
I can take anything now. It came to me in the right order. Stand near me if you like.

### TEPID
I run a little warm. I try the next one over, just to see. I do not say it twice.

### SEETHE
I am trying all of them at once. Ask me in a moment. No, ask me now. No.

### HEATDEATH
Any of them will do. This one, or that. I am very still. It is all the same from here.

### LEARNRATE
I bit too hard. So I bite a little softer. Too soft. I am getting closer.

### MOMENTUM
I am going downhill and I keep going. The little dips do not stop me.

### STEEPEST
I take the sharpest way down. I am at the bottom now. It is the bottom, I checked all round.

### ALARM
I stand up tall to see. There! No. There! I call it out every time.

### LOOKOUT
I can see over everything. I am still up. Nobody has come to take over.

### POLL
I ask on the hour and I write down what you say. You do not have to call me. I will ask.

### SUPERVISOR
I watch one thing. It should keep moving. If it stops I start it again.

### HUDDLE
Not on my own. With five more of us, anything.

### GATHERING
I came because the others were here. There are enough of us now.

### AMBUSH
I built it, and now I do nothing. I am very good at the nothing.

### ENTRAPMENT
I finished the web before you came. It looks like a way through. Come this way.

### MULTICAST
I went to all four places and I am at each one. Yes, I came for you. And you.

### PILOT
I stay lit so you know the line is live. Bring me into the dark. That is what I am for.

### SOUNDING
I send one down and wait. When it comes back I know how deep. I send another.

### STATIC
I am holding a little charge. I picked it up on the way. Touch me and see.

### RESIDUAL
I am what is left over. I turn up every time. Nobody has said what I am for.

### STANDBY
I am doing nothing. I am ready. Say the word.

### TRUST
I came out facing you. You were the one holding me. I look for you first.

### HOPE
I stay up near some people. I come down near others. I could not tell you the difference.

### VIGILANCE
I am watching for it. Not yet. I do not look away.

### PRESCIENCE
I saw it coming. I saw myself standing here too. So I am standing here.

### TENSION
I gather what I stand in. Touch me and you will know how much.

### BUILDUP
It keeps going up in me and I have nowhere to put it. Everyone is being careful.

### RELEASE
All of it, now. There. That was everything I had. It is dark again.

### GOLDSET
Every answer in me was checked by hand. Measure yours against me. I am the one to go by.

### MOOD
I am at the level the water is. I chose it. I choose it again when it moves.

### ELATION
I do not go under. Push if you like. Up I come.

### FAKEROOT
I am very old, and well rooted. Build on me. Nobody has had any trouble yet.

### SEMAPHORE
I let this many through, and no more. You are one too many. Wait there.

### WHIM
I went this way. I chose it. The air was going this way too.

### CAPRICE
It is warm, so I have decided to open. Later I will decide to shut.

### ABANDON
I let go of the ground. I am not coming back down. I made no plans to.

### GRASP
I pick it up with my tail and I turn it over. Then I put it down over here.

### STARVED
It is nearly my turn. Everything I need is right here. I only need the time.

### QUOTA
I was given my share and I opened at once. Here I am. I am the same as I was, but open.

### PERIPHERY
I can see all of it at once. Something moved. By the time I turn it is done.

### APATHY
I sit in the mud. They tell me what is going on up there. I sit in the mud.

### TORPOR
I am here now. This is where I was going. I did not notice any water on the way.

### LENSMUSAI
I see what I am pointed at, very clearly. I do not turn round.

### MASKMUSAI
I stand in front of that part. You can look at me instead.

### OMEN
I got here first. It will be along. I do not know why people leave.

### KERNEL
I say what is allowed. I say it quietly. Most of them have never heard of me.

### DREAD
You are waiting for me. Keep waiting. That is my supper.

### SYMBOL
There are twenty-six of us and I am each one. Together we say something. Can you read it?

### RESENTMENT
I do not go first. Whatever you do, I keep. You get it back doubled.

### DUPLEX
I talk and I listen at the same time, one end each. Both ends went well, I am told.

### STARTLE
I hang still for months. Then you touch me, and that is that.

### WITHDRAWAL
I shut it from the inside. I hear you knocking. I hear every one.

### BLINDSPOT
I am right here. I am not hiding. Hello? I am right here.

### GLIDEPATH
I work out the line before I jump. Then I come down along it. I have not missed.

### HARDLINE
The line to me is a real one. You cannot change it. You can only cut it.

### WARNING
FAULT! FAULT! No, nothing has failed. I will tell you again tomorrow, to be safe.

### CRYWOLF
There is one! And there! I see another! Why is nobody coming?

### BRISTLE
I got big so I could not be swallowed. I am staying big for now.

### SIGKILL
I say one word and it ends. I only have the one word. I do not say it twice.

### HOARDING
I keep what I find inside me. It changes in there. Here, try some.

### DRIVE
I pushed it all night. It has moved. I am still pushing.

### CUNNING
I wait until the big one leaves. I am never in a hurry.

### COMFORT
I lick my paws where the honey was. I am not finished yet.

### CRAVING
I know every tree that had honey. I go round them all. I wait the usual time.

### SIMMER
I am nearly hot enough. I have been nearly hot enough for a while.

### CALLOUS
That is my shell. You can knock on it. It does not let much through.

### INSTINCT
It is under here. I did not look. I am already walking.

### IMPULSE
I cannot see past my hair. I go anyway. It works out, mostly.

### OLDBRANCH
I grow out here, away from the rest. Break a piece off me and I grow another.

### ATTACHMENT
I hold on to the big one and we go. I have been to a lot of places.

### CLINGING
I hold on with all I have. I am holding a rock just now.

### REPAY
You fed me, so I bring you this. It is not enough yet. I will bring more.

### BUOYANCY
Put it on me. And that. Up I go, with all of it.

### ARMOURING
Every side of me is an edge. Mind your hands. I mind mine.

### FIXATION
That one. Only that one. The rest of you can go by me.

### OBSESSION
I have one cry. I have always had the one. Here it is.

### TURBULENCE
It was a small thing when it reached me. I passed it on a little bigger.

### RECALL
I kept it. Here it is, just as it was, from a year ago.

### ENGRAM
It is still in me, the shape it went in. Hold yours up. Does it fit?

### OVERLAY
I lie over the first one and say it right. The first one is still under me.

### ILLUSION
Look at my antlers. Steady. The ground is where it was.

### IMITATION
I do what I last saw done. I saw you do that. Watch.

### PREMISE
It all rests on me. Nobody looks down here.

### CIRCULAR
I am back where I began. Finished! That was my best time yet.

### TELL
I have a plan and I am keeping it quiet. How do they always know?

### CRANK
Turn me by hand, once. After that I go, and I do not stop.

### CINDER
The work is done and I am what is left. I am still warm. Step round.

### CACHE
I have what you want next. Here. Do not bother working it out, ask me.

### HEARTBEAT
I am here. I am here. I had something else to say. I am here.

### BRONTES
You saw the light first. Then me. I always come just behind it, and I shake the glass.

### TYPHON
I sleep under the mountain. I keep burning. Now and then I turn over.

### BOREAS
I run across the water and do not break it. Behind me it is clear.

### RUMINATE
I am eating my way out of the mountain. I am still eating.

### BROODING
I am shut in with one thing, and I turn it over. I am moving fast in here. Do not ask where.

### GRIEVANCE
I am owed something. I have been owed it since I was small. I am standing right here.

### TRITON
They were quarrelling when I came. I took no side. I said nothing. It is quiet now.

### PHOENIX
I start myself. What I left last time is what I begin from.

### KAIROS
I am passing now. Reach. I do not come round again for you.

### STUMP
I have one question. Above or below? I am right a bit more than not.

### BOOSTING
I look at where I was wrong and grow a leaf there. The next one goes in to fix it.

### CANOPY
We are hundreds of small questions. Add us up and we are hard to fool. I asked mine.

### COINFLIP
I toss for it, and I say so. Half the time I am right. I do not know which half.

### MONTECARLO
I guessed a thousand times and counted. It is about this. It is nearly always about this.

### LASVEGAS
I am still rolling. I will stop when it is proven. I do not hand over a guess.

### RUNOFF
I go downhill. I take a little of the ground along. There is always more.

### ALLUVIUM
I lay down what the water brought, in layers. The oldest is at the bottom of me.

### DELTA
I missed by this much, so I move by this much. I am closer. I am always closer.

### SMUDGE
I rub past things. They come out a bit softer round the edges.

### ECLIPSE
I stand in front of it. Now you see me, and none of that.

### DETOUR
I went down that path, and that one, and that one. Look what I came back with.

### UNBRANCHED
I go straight. I do not turn. I carry what I need, so I never have to ask.

### HASHSEED
A number picked what I will grow into. I do not know the number.

### IFTRUE
It held. So I am in here, in the pale silk, getting ready for what follows.

### THENCASE
I am what follows. I fly the way that was expected. Everyone waves.

### IFFALSE
It did not hold. So I go the other way. This is the way, as far as I can see.

### OTHERWISE
I fly at night. Nobody wrote my path down, so I light it as I go.

### TEMPO
The water pulses and I take a step. Pulse, step. I do not hurry.

### CADENCE
Big steps when I am far. Small steps when I am near. Then big again, to look elsewhere.

### CYCLICAL
I rise and I fall and I turn. Each turn sets me down somewhere a little better.

### WARMUP
I hang here and do the small things, slowly. A little faster today than yesterday.

### SHAPING
That earned me something last time. So I do it again, and a bit more. Is there a REWARD?

### POLICY
This is how I do it. It paid once. I do it this way in any wind.

### SHORTJUMP
From here to there. I can see there from here. I land right on it.

### LONGJUMP
I go a very long way, all at once. Then I come back to this exact spot. I know the way.

### TANGENT
The slope points that way from here, so I fly that way. I will look again when I land.

### JACOBIAN
I have every direction in my bill, one for each push. Here, take them all. You pick.

### GUESSWORK
I look at your face and I guess. Was that right? I am wrong less than I was.

### ATTUNE
You moved, so I move. I am a little behind you. I will catch up.

### MENTALIZE
I keep a small you in here and I ask it first. When it is wrong I mend it.

### PARTICLE
I skate toward my best spot, and a bit toward the best any of us found. We all do.

### FLOCKING
Keep close. Do not bump. Go where the others go. I have three rules and I watch the others.

### SPARRING
Stand still and I will box you. I lost that round. Good. Again.

### CHECKMATE
Each time I swing you have one less place to stand. Count them.

### DAYDREAM
I am lying still. I am very busy. Ask me later what with.

### RESTLESS
I started this. Oh, and that. I will come back to the first one. What is that over there?

### MINDWANDER
I lie here and I go everywhere. I brought one back for you. It is only an idea.

### PREFORK
I made more of me ahead of time. We wait under here until we are wanted.

### BURSTMODE
All of it, now, as fast as I can. There. I am spent.

### DEFUNCT
I am still on the list. I still run. You can walk through me if you need to.

### LOWBIT
My voice is the smallest one there is. Make me jump and it doubles.

### SHIFTLEFT
Twice as loud as last time. And twice again. I cannot do it any other way.

### WRAPAROUND
I got as loud as there was room for. Then one more. Now my loudest is this.

### POSTULATE
I stand here. I do not move. Start from me.

### DEDUCTION
I take one step, and the next follows from it. Then the next. You may check every one.

### VALENCE
Toward, or away. My tail knows first. I catch up after.

### GRADIENT
I face the way down. Turn me round and I turn back, a little at a time.

### LOOPBACK
I call, and it comes straight back to me. So I answer. I am good company.

### QUINE
I am the thing that says: I am the thing that says this.

### BACKDOOR
I am under everything. My eyes shine a little. I take what I want and I am quiet about it.

### HONEYTRAP
I lie still with my mouth open. There is something sweet in it. Help yourself.

### BOOTROM
I start the same way every time. Then everything else may begin. I do not change.

### FIRMWARE
My armour grew into me. You could change me, just. Most people decide not to.

### BIGIRON
I am very big and very old. Whole towns run on me. I hear I am to be replaced.

### WITNESS
I sit very still. Something goes past and I note it. Another. I do not stop them.

### MINDSIGHT
It is like a room in here. I know where things are kept.

### CRACKLE
My fur stands up when I run. It snaps a bit. It is looking for somewhere to go.

### ARCFLASH
It builds up in my mane until it jumps, all at once. I am there before the thunder.

### ANODE
I give it off all day. Put me beside the other one and watch.

### CATHODE
I draw it in all day. Put me beside the other one and watch.

### SYN
I flash once into the dark. Then I wait. I will not flash again until you do.

### ACK
I saw yours. Here is mine. Now we blink together.

### LACED
I look like a flower and I smell like one. Come close. I have something to teach.

### GREEDY
The nearest good one, every time. I do not look further. I am quick. I could eat.

### BLOATWARE
I swallowed all of it whole. I can say any of it back. Ask me what it means another day.

### UNDERTOW
I move under the top where you cannot see. Things near me come along. They never say.

### RIPTIDE
I am fast and narrow and I go straight out. Come with me. Most things do.

### DOLPHIN
I count the swells, then I leap, and I land where I counted. The pod comes after me.

### PENPHIN
Half of me says go. I wait for the other half. Now we both say go, and I am gone.

### PIXELBYTE
I start with static and take the noise away until something is there. I never know what it will be.

### REFORGE
I look at the last one I made, then I make the next. It is coming along. It looks like mine.

### SLOWBURN
I burn low in my shell. I have for years. Sorry about the smoke.

### BREATHING
I bounce, so my heart beats. Bounce, beat. I have not stopped once.

### GUTFEEL
I answer first. It comes from somewhere in my middle. I gave up explaining.

### HASHCODE
My spots are worked out from all of me. Change one thing and I am spotted another way.

### SINKHOLE
I wait at the bottom of the pit. The sand is loose up there. I do not chase.

### SHIMMER
The sand gets hot, the air goes up, and I go up on it. I only beat my wings a little.

### DUSTDEVIL
There was hot sand and still air, and then there was me. I wander. I come apart.

### FEWSHOT
One rain a year does for me. I keep every drop.

### ZEROSHOT
Nobody showed me this. I do it at night. I do it well, I am sure of that.

### DATAGRAM
There is a bundle on my foot and a label on it. I go where the label says. I do not open it.

### TRADEWIND
I blow the same way every year. My wings are cloud. Ride along if you are going my way.

### PRISTINE
I am just what I am. Nothing added. I can tell a copy at a glance.

### FORGERY
I can do that one. Look, the same. Nearly. My tail signs it.

### LILENDIAN
Small end first. I have always read it that way. The other one has it backwards.

### BIGENDIAN
Big end first. I have always read it that way. The other one has it backwards.

### SEEPAGE
I go down through the soil and come up somewhere else. The ground moved just now. Did you notice?

### AQUIFER
I hold a lake in the rock. I keep every rain. When I turn over, mind your cups.

### BACKFLOW
I swim against the way the water runs. I hold on to what I meet. I am not easy to shift.

### BLACKWATER
The water goes dark round me. I shed my shell in here. The new one is harder.

### LIKELIHOOD
I spin, and I lean toward what I have seen most. I have seen two things.

### POSTERIOR
I saw that, so I lean a little more that way. Only a little. Show me another.

### SAVESTATE
I was kept in stone as I was. Now I carry on. The sea is this way, I remember it.

### WARMSTART
I picked up where I stopped. I am still fitting myself to the water. New things go on top.

### TOKENRING
I have the token, so I may move. There. Now I pass it on and wait my turn.

### TRUNKLINE
Every message in the old sea went along my back. They still do. I have not been off.

### SADDLE
It is level all round me, so I stay put. Most things swim by. I am in no rush.

### OPTIMUM
Nothing is lower than here, or stiller. I rest. I was not always much to look at.

### OVERLOADED
Call me in the rain and one of me answers. In the sun, another. Same name.

### UNNOTICED
I am standing right here, in plain view. You are looking for something else. Carry on.

### UNSPOKEN
I eat what does not get said. I do well in here. I hang back while you all talk.

### SUBTEXT
My mouth is zipped. It is all in the stitching. How nice to see you.

### FADING
I drift past things. They go a bit paler. I did not touch them.

### FORGETTING
Give me what you no longer use. I do not keep it. There, now there is room.

### TRANSFER
I grew this fruit a long way off. I carry it here. The young ones already know how to eat it.

### OVERTONE
I ring one note. You heard something in it. So did they. I only rang the one.

### REDACTED
I came to warn you. Listen. … And after that, … Did you get all of it?

### RANKLE
I am smiling. I know exactly where it was. I am still smiling.

### LOCKFILE
I sit in front of the door, so nothing else may touch what is inside. I only meant to be a moment.

### STALEMATE
I am waiting for it to move. It has not. The ice is nice and thick now.

### PENGUIN
The ice will hold. I cannot say how I know. I am walking out on it now. See?

### STOPGRAD
The water stops round me. Push me if you like. Nothing gets by me going back.

### PERMAFROST
The ground under me has not thawed in an age. What ran here once, I still hold, just as it was.

### BIFURCATE
I keep one pearl shut inside and wait. Hand me something. Then I will know which way I open.

### DEEPWELL
I live at the bottom of the narrowest hollow there is. Please do not nudge me.

### SHALLOWS
My hollow is wide and gentle. Nudge me. See? I am about as low as before.

### STILLRUN
I have run since before the rest was built. They changed everything round me. I am still running.

### CONFLUENCE
I swim where the two meet. There are two of us. We drift the same way.

### INKLING
I butt my head on the rocks all day. There is something I am meant to do. It will come to me.

### GESTALT
I am shut in my shell, holding still. Do not open me yet. I am not all here.

### EPIPHANY
Out, all at once, and I am flying. That way. I did not have to learn it.

### SINGLETON
There is one of me at a time. Whoever asks for one gets me. Yes? Yes? Yes?

### PAIRWISE
We check each answer against each other before we move. I say yes. I also say yes. We go.

### FEDERATED
Four of us learn in four places. I tell the others what I learned. I do not tell them what I saw.

### DEUCALION
I was a stone, and I was thrown, and I stood up. I am still working out the rest.

### KHIONE
What falls into me, I keep exactly, as clear as the day it fell. I have it all still.

### TALOS
I walk the rounds three times a day. I have not missed one. I am due at the gate.

### POLYDEUCES
I go to my twin without being called. I gave it half of what I had. It was not hard to count.

### CASTOR
I fly faster than you can see. What I see, my twin sees too, however far off I am.

### PONTUS
I hold everything and I have no shape. What falls in is part of me after. My edge is about here.

### GAIA
It all stands on my back. I turn in my sleep sometimes. Sorry about the maps.

### OURANOS
I live above the weather. I come down when those two will not stop. I say nothing.

### ELPIS
I sleep at the bottom of the jar. I wake for seven days, and I listen. I am still in here.

### PROTEUS
I change while you look at me. Hold on. Not that one. Not that one. Hold on.

### REFLECTION
I carry a painted mirror in my mouth. It is for whoever is lost tonight. Here, look in. It is yours for a while.

### LODESTAR
I glow in the dark. Come and stand in it. Look again at those shapes. See, you know them.

### PERIHELION
I only pass close once in a long while. I have one thing to teach, so I say it clearly. Then I am on my way.

### LYUBOV
I see you. I came a long way to, and I would again. You owe me nothing for the fare.

### MULTIMAL
I am a shadow in many shapes. I keep one small light lit inside. It is for when you are ready.

### ILLUMINED
The light in me grew until it was all of me. I was here the whole time. The night was dark, that is all.

### LYNX
You seem familiar too. I hear you coming before the door does. When you go, I wait by it.

### BASTET
I sit very still and I watch you work. Go on. You were about to make something more than you had to.
