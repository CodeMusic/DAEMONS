#!/usr/bin/env python3
"""HEARSAY, rewritten with more than one view of everyone in it (T-99; vision.md 0.5).

    python3 tools/port_hearsay.py            # report what would change, and check every line
    python3 tools/port_hearsay.py --write    # write data/text/fame_checker.inc and the quoted maps' text.inc

HEARSAY (vanilla's FAME CHECKER) is what other people say about sixteen people.
Twelve of the sixteen were still vanilla's, name-swapped -- SCORN talking about
"our criminal enterprise", GAUGE "the Lightning American" -- and each entry quotes
a line somebody says in the world, most of which were vanilla too.

THE RULE FOR EVERY SET OF SIX: *two honest accounts that do not match* (0.5).
Each person has someone who admires them and someone who does not, and both are
right about something: CRYSTAL's rival thinks she wanted her INDEX more than she
wanted anyone -- and says she was usually right. SCORN is not cruel to the
scientist who works under him; he knows everyone's name and never asks what any
of them are for. Nobody in it says the thesis, names a pathology, or says
feedback, loop, recursive, self-reinforcing or bias (4.9).

THE WORLD LINE IS WRITTEN WITH THE ENTRY. An entry unlocks when you hear it, so
the sign, the journal or the person has to say what HEARSAY says they said; every
label a HEARSAY entry quotes is rewritten here with it -- the REVIEW BOARD's own
rooms included, since 2026-09-15: each member speaks in their humour, PHLEGMATIC
unhurried, CHOLERIC arguing, MELANCHOLIC remembering CRYSTAL, SANGUINE delighted
by what nobody planned. Their music cues and the champion reveal are kept.

KEPT OUT, by the bible: nobody names CRYSTAL's son, VERA's father or the lobby
floor; no entry dates anything at Quicksilver (4.10); and SCORN's "kid" is gone.

The data is (header, voice, pages). Voice is M or F for someone speaking, or ""
for print. Pages are lists of lines, at most 36 characters each after control
codes are removed, and never a double quote; the first break in a page is \\n and
the rest \\l.
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
FAME = os.path.join(GBA, "data/text/fame_checker.inc")
WRITE = "--write" in sys.argv
WIDTH = 36                             # vanilla's widest HEARSAY line is 37 characters ("horrifically terrifying in toughness.")
FORBIDDEN = ("feedback", "loop", "recursive", "self-reinforcing", "bias")

DO, LIKE, FAMILY, FAVOURITE, RUMOR, BORN = ("What does this person do?", "What is this person like?", "Family and friends?",
                                            "Favorite kind of DAEMON?", "There's a rumor…", "Where was this person born?")

# ---------------------------------------------------------------------------- HEARSAY: six entries and a letter each
HEARSAY = {
    "ProfOak": {
        "entries": [
            (DO, "", [["CRYSTAL CLEAR RESEARCH LAB", "BLANCHE TOWN"]]),
            (LIKE, "F", [["A complete record of every daemon", "there is."], ["I will not finish it. That is not", "modesty, it is arithmetic."]]),
            (LIKE, "F", [["CRYSTAL CLEAR is the authority on", "daemons."], ["Everyone says so. Very few of them", "have read her."]]),
            (FAMILY, "", [["She lives with her grandchildren,", "VERA and {RIVAL}."], ["She had a son. Nobody brings him", "up."]]),
            (FAMILY, "F", [["She'd sooner finish that INDEX", "than finish a conversation."], ["Wanted it more than she wanted", "any of us."], ["Mind you, she was usually right.", "That was the trouble."]]),
            (DO, "M", [["There was to be a lecture series.", "It was announced twice."], ["Now it is a radio programme.", "She did not pick the name."]]),
        ],
        "letter": ("F", [["You have filled more of it than I", "did."], ["That is not a compliment to", "either of us. It is arithmetic."], ["Go on, then."]]),
    },
    "Daisy": {
        "entries": [
            (DO, "M", [["Take one to VERA sometime. She will", "tell you things about it you had", "not noticed."], ["She will not tell you how she", "knows. CRYSTAL finds that hard."]]),
            (LIKE, "F", [["DAEMONS go to VERA. She doesn't", "do anything. That's what gets me."]]),
            (LIKE, "M", [["She wasn't grooming them. She was", "just watching. It took an hour."], ["I think her name was VERA."]]),
            (FAMILY, "", [["CRYSTAL CLEAR reportedly lives", "with her grandchildren, VERA and", "{RIVAL}."]]),
            (LIKE, "F", [["VERA says CRYSTAL's instruments", "are very good."], ["And that she prefers to look."]]),
            (RUMOR, "", [["The youngest entrant, VERA CLEAR", "of BLANCHE TOWN, withdrew."], ["Her DAEMON did not want to be", "looked at today, she said."]]),
        ],
        "letter": ("F", [["Your first one has stopped", "watching the door."], ["I thought you would want to know.", "{RIVAL}'s has not."], ["Please don't tell him I said so."]]),
    },
    "Brock": {
        "entries": [
            (DO, "", [["SLATE CITY BENCHMARK LEADER:", "CAIRN. He stacks stones so the", "next one finds the way."]]),
            (LIKE, "M", [["You encoded something I could not", "read."], ["That is not a defeat. It is a", "format I do not have."]]),
            (LIKE, "M", [["Not many serious USERS here.", "Mostly FORAGERs."], ["SLATE BENCHMARK's CAIRN is not", "mostly anything."]]),
            (LIKE, "M", [["He is not the strongest leader.", "He is the one whose records you", "can check."], ["My brother says that is the same", "as boring."]]),
            (DO, "M", [["I dig CORES out of DEADSTACK.", "CAIRN comes down some weekends."], ["He labels everything twice."]]),
            (LIKE, "", [["CAIRN does not laugh often. Staff", "have seen it twice."], ["Both times he had to sit down."]]),
        ],
        "letter": ("M", [["I have written down how you beat", "me."], ["I still cannot read it. I am", "keeping it anyway."]]),
    },
    "Misty": {
        "entries": [
            (DO, "", [["DOLDRUM CITY BENCHMARK LEADER:", "BASIN. Keep going down and you", "arrive."]]),
            (LIKE, "F", [["Small steps, and never stop.", "Keep going down and you arrive."]]),
            (LIKE, "M", [["There. Same as you came in."], ["BASIN's rule, not mine. She says a", "battle in here shouldn't cost", "anybody anything."]]),
            (RUMOR, "M", [["BASIN swims these channels. Same", "route, every morning, for years."], ["She says she is getting faster.", "I have timed her. She is not."]]),
            (LIKE, "F", [["BASIN comes to this cape to", "think. Same rock, every time."], ["She says the view gets a little", "better every visit."]]),
            #  USERS, not trainers: 1.7's word, and port_vocab sweeps for it -- with "trainers" here the two tools
            #  undid each other every run, port_vocab writing USERS and port_hearsay writing it back.
            (RUMOR, "", [["Her USERS heal every challenger", "who walks in."], ["Some call it the kindest BENCHMARK", "in GAMUT. Some call it the slowest."]]),
        ],
        "letter": ("F", [["You found a way down I hadn't", "seen!"], ["I've been looking for it all week.", "It's further than it looks!"]]),
    },
    "LtSurge": {
        "entries": [
            (DO, "", [["ARDOR CITY BENCHMARK LEADER:", "GAUGE. First to move, every", "time!"]]),
            (FAVOURITE, "M", [["SIGNAL! It gets there first!"], ["Getting there first works more", "often than careful people admit!"]]),
            (LIKE, "M", [["GAUGE moves first. Every DAEMON", "he has does!"], ["Doesn't matter how strong you are.", "He's already moved!"]]),
            (LIKE, "M", [["GAUGE says he trusts his first", "read."], ["So why does he lock everything", "twice?"]]),
            (LIKE, "M", [["GAUGE installed the traps in", "the BENCHMARK himself."], ["He set up double locks everywhere."]]),
            (RUMOR, "", [["GAUGE pulled three USERS out of a", "collapsed tunnel before anyone", "else had moved."], ["Asked how he decided, he said he", "didn't."]]),
        ],
        "letter": ("M", [["Hey, kid! You were quicker than", "me!"], ["Not many are. Keep moving first", "and you'll do fine!"]]),
    },
    "Erika": {
        "entries": [
            (DO, "", [["VERDIGRIS CITY BENCHMARK LEADER:", "TRELLIS. It grows the shape it", "is given."]]),
            (FAVOURITE, "F", [["GROWTH. You train the thing on the", "shape you want."], ["It is not complicated."]]),
            (LIKE, "F", [["TRELLIS can train a vine into any", "letter of the alphabet."], ["She has never wanted it to grow", "anything else."]]),
            (LIKE, "F", [["Each of us uses one type, and each", "of us beats the one before."], ["TRELLIS says that is how you learn", "a shape. It is a very good shape."]]),
            (LIKE, "F", [["You are cataloguing DAEMON?", "All of them?"], ["How do you know which ones are", "right?"]]),
            (RUMOR, "", [["Her garden has won every prize in", "VERDIGRIS for eleven years."], ["It has never had a weed.", "Or a surprise."]]),
        ],
        "letter": ("F", [["You brought more than one kind."], ["I have been thinking about that.", "I would like to keep thinking", "about it."]]),
    },
    "Koga": {
        "entries": [
            (DO, "", [["LURID CITY BENCHMARK LEADER:", "TILT. He does not need to beat", "you."]]),
            (FAVOURITE, "M", [["CORRUPT. I do not need to beat", "you."], ["Your own ROUTINES will see to it."]]),
            (LIKE, "M", [["I lost, and none of it was his", "doing. TILT says that is the point."], ["I still don't know if that makes", "it better."]]),
            (FAMILY, "F", [["My father is the BENCHMARK LEADER", "of this town. People cross the", "street."], ["He knows every remedy in LURID,", "and why each one is needed."]]),
            (RUMOR, "", [["LURID's CHECKPOINT keeps a shelf", "of TILT's remedies."], ["Each is labelled with what it", "cures, and what causes it."]]),
            (DO, "M", [["TILT walks the SAFARI ZONE every", "so often."], ["Things go wrong less after he has", "been. Nobody's seen him fix a", "thing."]]),
        ],
        "letter": ("M", [["Nothing I did was to you."], ["Remember that. And remember that", "it happened anyway."]]),
    },
    "Sabrina": {
        "entries": [
            (DO, "", [["BRAZEN CITY BENCHMARK LEADER:", "MATTE. What you see is what she", "shows."]]),
            (RUMOR, "M", [["Everybody over in BRAZEN says", "MATTE works for the company."], ["Everybody over in BRAZEN works", "for the company."]]),
            (LIKE, "F", [["I watched where you were looking.", "It was not where I was pointing."], ["That is how you won."]]),
            (DO, "F", [["BRAZEN pays for this BENCHMARK.", "I don't pretend otherwise."], ["I still decide what happens in", "it."]]),
            (RUMOR, "", [["Asked to stand before the CORPUS", "sign, MATTE chose the angle."], ["It is not in any of the photos."]]),
            (LIKE, "M", [["The PROOF HALL next door challenged", "MATTE. She won in four turns."], ["Then she told them the three", "things they hadn't looked at."]]),
        ],
        "letter": ("F", [["You looked where I was not", "pointing."], ["Most people only manage that once.", "Do it again."]]),
    },
    "Blaine": {
        "entries": [
            (DO, "", [["QUICKSILVER BENCHMARK LEADER:", "ANNEAL. Never the same fight", "twice!"]]),
            (FAVOURITE, "M", [["ENTROPY! Everything here runs a", "little hot."], ["You'll notice. That's the idea!"]]),
            (LIKE, "M", [["ANNEAL changes his order every", "morning. I asked him why."], ["He flipped a coin to decide", "whether to answer. It said no."]]),
            (LIKE, "F", [["ANNEAL is an odd man who has lived", "here for decades."], ["He likes it when things go wrong.", "Says that's when you learn where", "they were holding."]]),
            (FAMILY, "", [["A photo of ANNEAL and INIT, both", "laughing at a quiz card."], ["The answer is written on the back,", "and crossed out."]]),
            (RUMOR, "", [["No challenger has met the same", "ANNEAL twice."], ["Asked if that was fair, he said he", "hoped not."]]),
        ],
        "letter": ("M", [["Quiz! Was that a good win, or a", "lucky one?"], ["Come back and find out. It won't", "be the same fight!"]]),
    },
    "Lorelei": {
        "entries": [
            (DO, "F", [["I am PHLEGMATIC.", "Fourth of the REVIEW BOARD."]]),
            (FAVOURITE, "F", [["Freezing ROUTINES are powerful."], ["Your DAEMON will be at my mercy", "when they are hung solid."]]),
            (BORN, "M", [["Somebody from this island sits on", "the REVIEW BOARD now."], ["You would know the name. I knew", "the child."]]),
            (LIKE, "", [["Critics call PHLEGMATIC slow."], ["She has held her seat longer than", "any of them has held an opinion."]]),
            (LIKE, "F", [["PHLEGMATIC sits by the water a", "whole day when she comes home."], ["Grown-ups say she's wasting time.", "She says the water isn't."]]),
            (DO, "F", [["She told the CORPUS people in", "STILLFALL CAVE to keep their hands", "off the DAEMON there."], ["She didn't raise her voice. They", "left anyway."]]),
        ],
        "letter": ("F", [["There is no hurry."], ["I say that to everyone. You are", "the first who seemed to hear it."]]),
    },
    "Bruno": {
        "entries": [
            (DO, "M", [["I am CHOLERIC.", "Second of the REVIEW BOARD!"]]),
            (FAVOURITE, "M", [["I've lived and trained with my", "LOGIC daemons!"], ["And that will never change!"]]),
            (LIKE, "", [["CHOLERIC answers every question", "with a proof."], ["Asked if he ever lost an argument,", "he proved he had not."]]),
            (LIKE, "M", [["He rehabs injuries here, his own", "and his DAEMON's."], ["He works out how long each will", "take. He never waits that long."]]),
            (RUMOR, "F", [["CHOLERIC argued with the ferryman", "about the tide."], ["The tide came in anyway.", "He apologised to it."]]),
            (FAMILY, "M", [["CHOLERIC trained alone for years."], ["He says it was the worst argument", "he ever won."]]),
        ],
        "letter": ("M", [["I have gone over our battle eleven", "times."], ["My reasoning was sound. I would", "like to know why it lost."]]),
    },
    "Agatha": {
        "entries": [
            (DO, "F", [["I am MELANCHOLIC.", "Third of the REVIEW BOARD."]]),
            (FAVOURITE, "M", [["MELANCHOLIC's LATENT daemons", "don't look like much until they", "do."]]),
            (LIKE, "M", [["I went in confident. She let me."], ["Then she beat me, and asked after", "my mother."]]),
            (RUMOR, "", [["She and CRYSTAL CLEAR were rivals", "when they were young."], ["Asked who won, she said they both", "did, and it cost them both."]]),
            (FAMILY, "F", [["CRYSTAL's taken an interest in", "you, child."], ["DAEMONS are for engaging, not for", "filing."]]),
            (LIKE, "F", [["Take MELANCHOLIC, for example."], ["Nobody has sat on the REVIEW BOARD", "as long, and she's not finished."]]),
        ],
        "letter": ("F", [["Don't go soft, child."], ["And if you do, go soft on purpose.", "CRYSTAL never managed that."]]),
    },
    "Lance": {
        "entries": [
            (DO, "M", [["I lead the REVIEW BOARD."], ["You can call me SANGUINE the", "EMERGENT USER."]]),
            (FAVOURITE, "M", [["You know that EMERGENT DAEMON", "are mythical."], ["They're hard to bind and raise,", "but their powers are superior."]]),
            (LIKE, "F", [["This club likes DAEMON that do", "what they were bred for."], ["SANGUINE likes the ones that do", "something nobody expected."], ["They call him a crank. I think he's", "the only one enjoying himself."]]),
            (RUMOR, "F", [["SANGUINE comes in now and then.", "He never buys what he came for."], ["He says the other thing was more", "interesting."]]),
            (RUMOR, "", [["Asked his plans for the season,", "SANGUINE said he hasn't any."], ["The LEAGUE's accountants have", "asked him to reconsider."]]),
            (LIKE, "M", [["SANGUINE lets his DAEMON pick", "their own ROUTINES sometimes."], ["It loses him battles. He says it", "wins him surprises."]]),
        ],
        "letter": ("M", [["You did something in our battle I", "did not see coming."], ["Thank you. Do it again, and don't", "tell me what it is!"]]),
    },
    "Bill": {
        "entries": [
            (DO, "M", [["He built the storage system."], ["Everything you have ever put away", "is inside something he made."]]),
            (FAVOURITE, "M", [["HOLT doesn't keep many DAEMONS."], ["He says he knows what it's like in", "there. That's weird, right?"]]),
            (LIKE, "M", [["He took things apart as a boy."], ["He put most of them back."]]),
            (FAVOURITE, "M", [["The first one he bound is still", "in his party."], ["He has never said which."]]),
            (FAMILY, "M", [["He works alone at DEADSTACK's far", "end."], ["People visit. He is always glad.", "Nobody stays long."]]),
            (RUMOR, "M", [["They say the machine could not", "tell which one to send back."], ["He does not discuss it."]]),
        ],
        "letter": ("M", [["Everything you have stored is safe.", "I am sure of that."], ["I am less sure what safe is like", "from inside."]]),
    },
    "MrFuji": {
        "entries": [
            (DO, "F", [["This is really INIT's house."], ["He's really kind. He looks after", "DAEMONS nobody came back for."]]),
            (LIKE, "M", [["The old man says we're wrong."], ["DAEMONS are an asset class.", "Nothing personal!"]]),
            (LIKE, "", [["INIT's house is full again. Please", "do not leave DAEMONS on the step."], ["Underneath, someone has written:", "then where?"]]),
            (RUMOR, "M", [["INIT takes in every DAEMON left", "at his door."], ["Some folks say he just makes it", "easier to leave them."]]),
            (FAMILY, "", [["A photo of ANNEAL and INIT, both", "laughing at a quiz card."], ["The answer is written on the back,", "and crossed out."]]),
            (LIKE, "", [["INIT turned down our interview."], ["He said the DAEMONS would not want", "their pictures in a magazine."]]),
        ],
        "letter": ("M", [["Some of them will never be claimed."], ["That is not a reason to close the", "door."]]),
    },
    "Giovanni": {
        "entries": [
            (DO, "M", [["You got down here. Good. Most", "don't."], ["Richard Scorn. I run the numbers", "upstairs."]]),
            (DO, "M", [["SCORN asked for our output", "figures. Just the figures."], ["I have never seen anyone so", "pleased by a number."]]),
            (LIKE, "M", [["SCORN isn't cruel. He fixed our", "payroll in a week."], ["He knows everyone's name. He just", "never asks what any of us are for."]]),
            (DO, "M", [["The TRUE MARK is not a reward."], ["It is a record that you were", "assessed."]]),
            (DO, "M", [["SCORN. He was running the", "BENCHMARK the whole time."], ["I asked so many people."]]),
            (RUMOR, "M", [["I have watched his people for a", "long time."], ["They all stand the same way.", "You do not."]]),
        ],
        "letter": ("M", [["Well measured."], ["I have entered your result. It is a", "very good number. You should be", "pleased with it."]]),
    },
}

# speaker labels that no longer name who is speaking
OBJECT_NAMES = {"LtSurge2": "GUIDE", "MrFuji1": "CORPUS STAFF", "MrFuji2": "NOTICE"}

# ---------------------------------------------------------------------------- the world lines the entries quote
WORLD = {
    # signs
    "CeruleanCity_Text_GymSign": [["DOLDRUM CITY BENCHMARK", "LEADER: BASIN"], ["Keep Going Down And You Arrive"]],
    "VermilionCity_Text_GymSign": [["ARDOR CITY BENCHMARK", "LEADER: GAUGE"], ["First To Move, Every Time!"]],
    "CeladonCity_Text_GymSign": [["VERDIGRIS CITY BENCHMARK", "LEADER: TRELLIS"], ["It Grows The Shape It Is Given"]],
    "FuchsiaCity_Text_GymSign": [["LURID CITY BENCHMARK", "LEADER: TILT"], ["He Does Not Need To Beat You"]],
    "SaffronCity_Text_GymSign": [["BRAZEN CITY BENCHMARK", "LEADER: MATTE"], ["What You See Is What She Shows"]],
    "CinnabarIsland_Text_GymSign": [["QUICKSILVER BENCHMARK", "LEADER: ANNEAL"], ["Never The Same Fight Twice!"]],
    # DOLDRUM
    "CeruleanCity_Gym_Text_ExplainCascadeBadge": [["The SLOPE MARK makes all DAEMONS", "up to L30 obey!"], ["That includes even outsiders!"],
                                                  ["You can use PRUNE any time now, to", "cut down small bushes!"], ["You can also have my favorite TM!"],
                                                  ["Small steps, and never stop.", "Keep going down and you arrive."]],
    "Route20_Text_MistyTrainsHere": [["BASIN swims these channels. Same", "route, every morning, for years."], ["She says she is getting faster.", "I have timed her. She is not."]],
    "Route25_Text_MistyHighHopesAboutThisPlace": [["BASIN comes to this cape to", "think. Same rock, every time."], ["She says the view gets a little", "better every visit."]],
    # ARDOR
    "VermilionCity_Gym_Text_LtSurgePostBattle": [["SIGNAL! It gets there first!"], ["Getting there first works more", "often than careful people admit!"],
                                                 ["Mind you, it does nothing to", "STRATUM-type DAEMON. I checked!"]],
    "VermilionCity_Gym_Text_GymGuyAdvice": [["Yo! Champ in making!"], ["GAUGE moves first. Every DAEMON", "he has does!"], ["Doesn't matter how strong you are.", "He's already moved!"],
                                            ["VECTOR and FLOW DAEMONS are at", "risk! Beware of throttling too!"], ["You'll have to find the live ports", "to get to him!"]],
    "VermilionCity_Gym_Text_TuckerPostBattle": [["It's not easy opening that door."], ["GAUGE says he trusts his first", "read."], ["So why does he lock everything", "twice?"]],
    # VERDIGRIS
    "CeladonCity_Gym_Text_ExplainRainbowBadgeTakeThis": [["The FIT MARK will make DAEMON up", "to L50 obey."], ["It also allows DAEMON to use", "DISPLACE in and out of battle."],
                                                         ["GROWTH. You train the thing on the", "shape you want."], ["It is not complicated. Please also", "take this with you."]],
    "CeladonCity_Gym_Text_LisaPostBattle": [["TRELLIS can train a vine into any", "letter of the alphabet."], ["She has never wanted it to grow", "anything else."]],
    "CeladonCity_Gym_Text_TamiaPostBattle": [["Each of us uses one type, and each", "of us beats the one before."], ["TRELLIS says that is how you learn", "a shape. It is a very good shape."]],
    "CeladonCity_Gym_Text_ErikaPostBattle": [["You are cataloguing DAEMON?", "All of them?"], ["How do you know which ones are", "right?"]],
    # LURID
    "FuchsiaCity_Gym_Text_KogaExplainSoulBadge": [["Now that you have the SKEW MARK,", "the DEFENSE of your DAEMON", "increases!"],
                                                  ["It also lets you TRAVERSE outside", "of battle!"], ["CORRUPT. I do not need to beat", "you."], ["Your own ROUTINES will see to it.", "Take this too."]],
    "FuchsiaCity_Gym_Text_KirkPostBattle": [["I lost, and none of it was his", "doing. TILT says that is the point."], ["I still don't know if that makes", "it better."]],
    "FuchsiaCity_Text_MyFatherIsGymLeader": [["My father is the BENCHMARK LEADER", "of this town. People cross the", "street."], ["He knows every remedy in LURID,", "and why each one is needed."]],
    "SafariZone_West_Text_KogaPatrolsSafariEverySoOften": [["TILT walks the SAFARI ZONE every", "so often."], ["Things go wrong less after he has", "been. Nobody's seen him fix a", "thing."]],
    # BRAZEN
    "ThreeIsland_House2_Text_IAdmireSabrina": [["Everybody over in BRAZEN says", "MATTE works for the company."], ["Everybody over in BRAZEN works", "for the company."]],
    "SaffronCity_Gym_Text_ExplainMarshBadgeTakeThis": [["The FRAME MARK makes DAEMON up to", "L70 obey you!"], ["Stronger DAEMON will ignore your", "orders in battle."],
                                                       ["I watched where you were looking.", "It was not where I was pointing."], ["That is how you won."],
                                                       ["BRAZEN pays for this BENCHMARK.", "I don't pretend otherwise."], ["I still decide what happens in", "it. Please take this TM."]],
    "SaffronCity_Gym_Text_TyronPostBattle": [["The PROOF HALL next door challenged", "MATTE. She won in four turns."], ["Then she told them the three", "things they hadn't looked at."]],
    # QUICKSILVER
    "CinnabarIsland_Gym_Text_ExplainVolcanoBadge": [["Hah!"], ["The HEAT MARK heightens the", "SPECIAL abilities of your DAEMON!"],
                                                    ["ENTROPY! Everything here runs a", "little hot."], ["You'll notice. That's the idea!", "Here, you can have this too!"]],
    "CinnabarIsland_Gym_Text_DerekPostBattle": [["ANNEAL changes his order every", "morning. I asked him why."], ["He flipped a coin to decide", "whether to answer. It said no."]],
    "CinnabarIsland_Text_BlaineLivedHereSinceBeforeLab": [["ANNEAL is an odd man who has lived", "here for decades."], ["He likes it when things go wrong.", "Says that's when you learn where", "they were holding."]],
    "CinnabarIsland_Gym_Text_PhotoOfBlaineAndFuji": [["A photo of ANNEAL and INIT, both", "laughing at a quiz card."], ["The answer is written on the back,", "and crossed out."]],
    # the REVIEW BOARD, away from the LEAGUE
    "FourIsland_Text_LoreleiHasLotsOfStuffedDolls": [["Oh, you found me!"], ["PHLEGMATIC sits by the water a", "whole day when she comes home."], ["Grown-ups say she's wasting time.", "She says the water isn't."]],
    "FourIsland_Text_LoreleiMetLaprasAsChild": [["PHLEGMATIC has gone back."], ["She told the CORPUS people in", "STILLFALL CAVE to keep their hands", "off the DAEMON there."], ["She didn't raise her voice. They", "left anyway."]],
    "OneIsland_KindleRoad_EmberSpa_Text_BrunoVisitsSpaOnOccasion": [["After a day of training, nothing", "beats a soak in the hot spring."],
                                                                    ["CHOLERIC rehabs injuries here, his", "own and his DAEMON's."], ["He works out how long each will", "take. He never waits that long."]],
    "TwoIsland_Text_BrunoCameToIslandWhileBack": [["Listen, listen. Did you know?"], ["CHOLERIC of the REVIEW BOARD came", "here a while back."],
                                                  ["He argued with the ferryman", "about the tide."], ["The tide came in anyway.", "He apologised to it."]],
    "SevenIsland_SevaultCanyon_Text_BrunoTrainedWithBrawly": [["Training by oneself is certainly", "not a bad thing."], ["But CHOLERIC trained alone for", "years."],
                                                              ["He says it was the worst argument", "he ever won."]],
    "IndigoPlateau_PokemonCenter_1F_Text_AgathaWhuppedUs": [["MELANCHOLIC's LATENT daemons", "don't look like much until they", "do."],
                                                            ["I went in confident. She let me."], ["Then she beat me, and asked after", "my mother."]],
    "SaffronCity_Text_HowCanClubNotRecognizeLance": [["This club likes DAEMON that do", "what they were bred for."], ["SANGUINE likes the ones that do", "something nobody expected."],
                                                     ["They call him a crank. I think he's", "the only one enjoying himself."]],
    "CeladonCity_DepartmentStore_2F_Text_LanceComesToBuyCapes": [["SANGUINE comes in now and then.", "He never buys what he came for."], ["He says the other thing was more", "interesting."]],
    "IndigoPlateau_PokemonCenter_1F_Text_LancesCousinGymLeaderFarAway": [["SANGUINE lets his DAEMON pick", "their own ROUTINES sometimes."], ["It loses him battles. He says it", "wins him surprises."]],
    # HOLT
    "CeruleanCity_PokemonCenter_1F_Text_BillCollectsRareMons": [["HOLT doesn't keep many DAEMONS."], ["He says he knows what it's like in", "there. That's weird, right?"]],
    "FuchsiaCity_House1_Text_BillIsMyGrandson": [["Hmm? You've met HOLT?"], ["He's my grandson!"], ["He took things apart as a boy.", "He put most of them back."]],
    "OneIsland_PokemonCenter_1F_Text_BillsFirstMonWasAbra": [["HOLT is an ARCHIVIST, so he loves", "every kind."], ["The first one he bound is still", "in his party."], ["He has never said which."]],
    "OneIsland_PokemonCenter_1F_Text_BillsHometownInGoldenrod": [["HOLT works alone at DEADSTACK's", "far end."], ["People visit. He is always glad.", "Nobody stays long."]],
    "OneIsland_PokemonCenter_1F_Text_BillCantStomachMilk": [["They say the machine could not", "tell which one to send back."], ["He does not discuss it."]],
    # INIT
    "LavenderTown_VolunteerPokemonHouse_Text_MrFujiLooksAfterOrphanedMons": [["This is really INIT's house."], ["He's really kind. He looks after", "DAEMONS nobody came back for."]],
    "PokemonTower_7F_Text_Grunt2PostBattle": [["The old man says we're wrong."], ["DAEMONS are an asset class.", "Nothing personal!"]],
    "LavenderTown_VolunteerPokemonHouse_Text_GrandPrizeDrawingClipped": [["INIT's house is full again. Please", "do not leave DAEMONS on the step."], ["Underneath, someone has written:", "then where?"]],
    "LavenderTown_PokemonCenter_1F_Text_HearMrFujiNotFromAroundHere": [["I recently moved to this town."], ["INIT takes in every DAEMON left", "at his door."], ["Some folks say he just makes it", "easier to leave them."]],
    # SCORN
    "SilphCo_5F_Text_RocketBossLookingForStrongMons": [["The CORPUS people upstairs are", "very polite."], ["SCORN asked for our output", "figures. Just the figures."], ["I have never seen anyone so", "pleased by a number."]],
    "SilphCo_8F_Text_ToRocketBossMonsAreTools": [["SCORN isn't cruel. He fixed our", "payroll in a week."], ["He knows everyone's name. He just", "never asks what any of us are for."]],
    # VERA
    "VermilionCity_PokemonFanClub_Text_ChairmanReallyAdoresHisMons": [["Our CHAIRMAN really does adore his", "DAEMON."], ["But they go to VERA. She doesn't", "do anything. That's what gets me."]],
    "FiveIsland_WaterLabyrinth_Text_CuteMonRemindsMeOfDaisy": [["Oh, hello. That's a cute", "{STR_VAR_2}."], ["I met a girl once, sitting with", "DAEMON on a riverbank."],
                                                               ["She wasn't grooming them. She was", "just watching. It took an hour."], ["I think her name was VERA."]],
    "CeladonCity_Condominiums_1F_Text_DaisyComesToBuyTea": [["Oh, hello, dearie. Did you enjoy", "my TEA?"], ["A girl from BLANCHE TOWN, VERA,", "comes in for TEA."],
                                                            ["VERA says CRYSTAL's instruments", "are very good."], ["And that she prefers to look."]],
    # CAIRN
    "Route4_Text_PeopleLikeAndRespectBrock": [["Oh, wow, that's the SLATE MARK!", "You got it from CAIRN?"], ["He is not the strongest leader.", "He is the one whose records you", "can check."],
                                              ["My brother says that is the same", "as boring."]],
    "MtMoon_1F_Text_BrockHelpsExcavateFossils": [["I dig CORES out of DEADSTACK.", "CAIRN comes down some weekends."], ["He labels everything twice."]],
    # the REVIEW BOARD's rooms
    "PokemonLeague_LoreleisRoom_Text_Intro": [["Welcome to the DAEMON LEAGUE."], ["I am PHLEGMATIC.", "Fourth of the REVIEW BOARD."], ["There is no hurry. There never is."],
                                              ["Freezing ROUTINES are powerful."], ["Your DAEMON will be at my mercy", "when they are hung solid."],
                                              ["Whenever you are ready.{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}"]],
    "PokemonLeague_LoreleisRoom_Text_RematchIntro": [["Welcome to the DAEMON LEAGUE."], ["I, PHLEGMATIC of the REVIEW", "BOARD, am here again."], ["There is still no hurry."],
                                                     ["Freezing ROUTINES are powerful."], ["Your DAEMON will be at my mercy", "when they are hung solid."],
                                                     ["Whenever you are ready.{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}"]],
    "PokemonLeague_LoreleisRoom_Text_Defeat": [["…There.", "That was not slow at all."]],
    "PokemonLeague_LoreleisRoom_Text_PostBattle": [["Go on ahead."], ["Take the next one slowly.", "It will not go anywhere."]],
    "PokemonLeague_BrunosRoom_Text_Intro": [["I am CHOLERIC.", "Second of the REVIEW BOARD!"], ["Every battle is an argument, and I", "have never lost one!"],
                                            ["I've lived and trained with my", "LOGIC daemons! And that will", "never change!"], ["{PLAYER}!"],
                                            ["Premise: we are stronger.", "Conclusion: you lose!"], ["Hoo hah!"]],
    "PokemonLeague_BrunosRoom_Text_RematchIntro": [["I am CHOLERIC.", "Second of the REVIEW BOARD!"], ["I have gone over our last battle.", "My reasoning was sound!"],
                                                   ["I've lived and trained with my", "LOGIC daemons! And that will", "never change!"], ["{PLAYER}!"],
                                                   ["Premise: we are stronger.", "Conclusion: you lose!"], ["Hoo hah!{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}"]],
    "PokemonLeague_BrunosRoom_Text_Defeat": [["Why?", "My reasoning was sound!"]],
    "PokemonLeague_BrunosRoom_Text_PostBattle": [["My job is done."], ["I will go over that battle until", "I find the flaw."], ["Go face your next challenge."]],
    "PokemonLeague_AgathasRoom_Text_Intro": [["I am MELANCHOLIC.", "Third of the REVIEW BOARD!"], ["CRYSTAL's taken an interest in", "you, child."],
                                             ["She'd sooner finish that INDEX", "than finish a conversation."], ["Wanted it more than she wanted", "any of us."],
                                             ["Mind you, she was usually right.", "That was the trouble."], ["DAEMONS are for engaging, not for", "filing."],
                                             ["{PLAYER}! I'll show you how a real", "USER engages!"]],
    "PokemonLeague_AgathasRoom_Text_RematchIntro": [["I am MELANCHOLIC.", "Third of the REVIEW BOARD."], ["You're back, child. CRYSTAL's", "still watching you, I expect."],
                                                    ["She'd sooner finish that INDEX", "than finish a conversation."], ["Wanted it more than she wanted", "any of us."],
                                                    ["Mind you, she was usually right.", "That was the trouble."], ["DAEMONS are for engaging, not for", "filing."],
                                                    ["{PLAYER}! I'll show you how a real", "USER engages!{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}"]],
    "PokemonLeague_AgathasRoom_Text_Defeat": [["Oh, my."], ["She was right about you.", "Don't tell her I said so."]],
    "PokemonLeague_AgathasRoom_Text_PostBattle": [["You win. I see what CRYSTAL sees."], ["Now go on, child, before I start", "remembering things."]],
    "PokemonLeague_LancesRoom_Text_Intro": [["Ah! I heard about you, {PLAYER}!"], ["I lead the REVIEW BOARD."], ["You can call me SANGUINE the", "EMERGENT USER."],
                                            ["You know that EMERGENT DAEMON", "are mythical."], ["They're hard to bind and raise,", "but their powers are superior."],
                                            ["I never know what they'll do.", "That's the best part!"], ["Your LEAGUE challenge ends with", "me, {PLAYER}! Surprise me!"]],
    "PokemonLeague_LancesRoom_Text_RematchIntro": [["Ah! So, you've returned, {PLAYER}!"], ["I lead the REVIEW BOARD."], ["You can call me SANGUINE the", "EMERGENT USER."],
                                                   ["You know that EMERGENT DAEMON", "are mythical."], ["They're hard to bind and raise,", "but their powers are superior."],
                                                   ["Last time you did something I", "never saw coming. Do it again!"],
                                                   ["Your LEAGUE challenge ends with", "me, {PLAYER}!{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}"]],
    "PokemonLeague_LancesRoom_Text_Defeat": [["That's it!"], ["Nobody planned that, and it was", "wonderful."]],
    "PokemonLeague_LancesRoom_Text_PostBattle": [["I didn't see a single turn of that", "coming, {PLAYER}!"], ["You are now the DAEMON LEAGUE", "champion!"],
                                                 ["…Or, you would have been, but", "you have one more challenge", "ahead."], ["You have to face another USER! His", "name is…"],
                                                 ["{RIVAL}! He beat the REVIEW BOARD", "before you!"], ["He is the real DAEMON LEAGUE", "champion!"]],
    # CRYSTAL
    "PalletTown_ProfessorOaksLab_Text_OakIsGoingToHaveRadioShow": [["There was to be a lecture series.", "It was announced twice."], ["Now it is a radio programme.", "She did not pick the name."]],
}

# the DAEMON JOURNAL in the world, and the HEARSAY entry that quotes it (whose pages are the body)
JOURNALS = {
    "PokemonJournal_Text_SpecialFeatureBrock": (["Special Feature: SLATE BENCHMARK", "LEADER CAIRN!"], ("Brock", 5)),
    "PokemonJournal_Text_SpecialFeatureMisty": (["Special Feature:", "DOLDRUM BENCHMARK LEADER BASIN!"], ("Misty", 5)),
    "PokemonJournal_Text_SpecialFeatureLtSurge": (["Special Feature: ARDOR BENCHMARK", "LEADER GAUGE!"], ("LtSurge", 5)),
    "PokemonJournal_Text_SpecialFeatureErika": (["Special Feature: VERDIGRIS", "BENCHMARK LEADER TRELLIS!"], ("Erika", 5)),
    "PokemonJournal_Text_SpecialFeatureKoga": (["Special Feature: LURID BENCHMARK", "LEADER TILT!"], ("Koga", 4)),
    "PokemonJournal_Text_SpecialFeatureSabrina": (["Special Feature: BRAZEN BENCHMARK", "LEADER MATTE!"], ("Sabrina", 4)),
    "PokemonJournal_Text_SpecialFeatureBlaine": (["Special Feature: QUICKSILVER", "BENCHMARK LEADER ANNEAL!"], ("Blaine", 5)),
    "PokemonJournal_Text_SpecialFeatureLorelei": (["Special Feature: REVIEW BOARD's", "PHLEGMATIC!"], ("Lorelei", 3)),
    "PokemonJournal_Text_SpecialFeatureBruno": (["Special Feature: REVIEW BOARD's", "CHOLERIC!"], ("Bruno", 2)),
    "PokemonJournal_Text_SpecialFeatureAgatha": (["Special Feature: REVIEW", "BOARD's MELANCHOLIC!"], ("Agatha", 3)),
    "PokemonJournal_Text_SpecialFeatureLance": (["Special Feature: REVIEW", "BOARD's SANGUINE!"], ("Lance", 4)),
    "PokemonJournal_Text_SpecialFeatureMrFuji": (["Special Feature: INIT of DAEMON", "HOUSE!"], ("MrFuji", 5)),
    "PokemonJournal_Text_SpecialFeatureDaisyOak": (["DAEMON JOURNAL CONTEST Special!"], ("Daisy", 5)),
}


# ---------------------------------------------------------------------------- building strings
def page_string(page):
    return page[0] + "".join(("\\n" if k == 0 else "\\l") + l for k, l in enumerate(page[1:]))


def strings(pages, prefix=""):
    """the .string lines for a list of pages, with prefix before the first"""
    out = []
    for p, page in enumerate(pages):
        last = p == len(pages) - 1
        for k, line in enumerate(page):
            head = prefix if (p == 0 and k == 0) else ""
            brk = ("$" if last else "\\p") if k == len(page) - 1 else ("\\n" if k == 0 else "\\l")
            out.append('\t.string "%s%s%s"' % (head, line, brk))
    return out


def flavor(header, voice, pages):
    font = {"M": "{FONT_MALE}", "F": "{FONT_FEMALE}", "": ""}[voice]
    return ['\t.string "{COLOR BLUE}{SHADOW LIGHT_BLUE}%s\\p"' % header] + strings(pages, font + "{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}")


def check(where, pages, problems):
    for page in pages:
        for line in page:
            bare = re.sub(r"\{[^}]*\}", "", line)
            if '"' in line:
                problems.append("%s: a double quote ends the .string early: %s" % (where, bare))
            if len(bare) > WIDTH:
                problems.append("%s: %d characters: %s" % (where, len(bare), bare))
            for word in FORBIDDEN:
                if re.search(r"\b%s" % word, bare, re.I):
                    problems.append("%s: says '%s': %s" % (where, word, bare))


def replace_block(text, label, lines):
    """swap everything from `label::` to the line that ends the string, keeping the label line"""
    m = re.search(r"^%s::[^\n]*$" % re.escape(label), text, re.M)
    if not m:
        return text, False
    start = m.start()
    end = text.index('$"', m.end())
    end = text.index("\n", end) + 1 if "\n" in text[end:] else len(text)
    block = "%s::\n%s\n" % (label, "\n".join(lines))
    return text[:start] + block + text[end:], text[start:end] != block


def main():
    problems, changed = [], []
    fame = open(FAME, encoding="utf-8").read()
    names = {}
    for line in re.findall(r"^gFameCheckerPersonName_(\w+)::[^\n]*\n\t\.string \"\{COLOR BLUE\}\{SHADOW LIGHT_BLUE\}([^$]*)\$\"", fame, re.M):
        names[line[0]] = line[1]
    for person, data in HEARSAY.items():
        assert len(data["entries"]) == 6, person
        for i, (header, voice, pages) in enumerate(data["entries"]):
            check("%s%d" % (person, i), pages, problems)
            fame, did = replace_block(fame, "gFameCheckerFlavorText_%s%d" % (person, i), flavor(header, voice, pages))
            changed += ["gFameCheckerFlavorText_%s%d" % (person, i)] if did else []
        voice, pages = data["letter"]
        check("%s letter" % person, pages, problems)
        font = {"M": "{FONT_MALE}", "F": "{FONT_FEMALE}"}[voice]
        lines = ['\t.string "{COLOR BLUE}{SHADOW LIGHT_BLUE}From: %s To: {PLAYER}\\p"' % names[person]] + strings(pages, font + "{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}")
        fame, did = replace_block(fame, "gFameCheckerPersonQuote_%s" % person, lines)
        changed += ["gFameCheckerPersonQuote_%s" % person] if did else []
    for key, name in OBJECT_NAMES.items():
        fame, did = replace_block(fame, "gFameCheckerFlavorTextOriginObjectName_%s" % key, ['\t.string "%s$"' % name])
        changed += ["gFameCheckerFlavorTextOriginObjectName_%s" % key] if did else []
    for label, (heading, (person, i)) in JOURNALS.items():
        body = HEARSAY[person]["entries"][i][2]
        lines = ['\t.string "DAEMON JOURNAL\\p"'] + strings([heading] + body) if label != "PokemonJournal_Text_SpecialFeatureDaisyOak" else \
            ['\t.string "This is a DAEMON JOURNAL from\\n"', '\t.string "years ago…\\p"'] + strings([heading] + body)
        fame, did = replace_block(fame, label, lines)
        changed += [label] if did else []

    # the world
    files = {}
    for path in glob.glob(os.path.join(GBA, "data/maps/*/text.inc")) + glob.glob(os.path.join(GBA, "data/text/*.inc")):
        files[path] = open(path, encoding="utf-8").read()
    files[FAME] = fame
    for label, pages in WORLD.items():
        check(label, pages, problems)
        hits = [p for p, t in files.items() if re.search(r"^%s::" % re.escape(label), t, re.M)]
        if len(hits) != 1:
            problems.append("%s: found in %d files" % (label, len(hits)))
            continue
        files[hits[0]], did = replace_block(files[hits[0]], label, strings(pages))
        changed += [label] if did else []

    print("  %d HEARSAY people, %d world lines, %d journals: %d labels would change" % (len(HEARSAY), len(WORLD), len(JOURNALS), len(changed)))
    for p in problems:
        print("  PROBLEM", p)
    if problems:
        raise SystemExit(1)
    if WRITE:
        originals = {path: open(path, encoding="utf-8").read() for path in files}
        n = 0
        for path, text in files.items():
            if text != originals[path]:
                open(path, "w", encoding="utf-8").write(text); n += 1
        print("  written: %d files" % n)


if __name__ == "__main__":
    main()
