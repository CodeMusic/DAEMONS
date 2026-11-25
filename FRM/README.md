# FRM -- the Field Resonance Methodology

*Decided by the user, 2026-11-25. This folder will hold every cycle's demo and every retro. Nothing in it is built
yet; the tickets that build it are listed at the end. Shown on EUDAIMONIA (the dashboard), read from here.*

## Cycles and Revolutions

Work runs in **cycles** of **one week** (the user's pick, 2026-11-25), Monday to Sunday. **R1C1F starts Monday 30 November 2026**: R1C1F 30 Nov-6 Dec, R1C2F 7-13 Dec, R1C3H 14-20 Dec. Two **Forward** cycles of momentum are followed
by a **Horizon** cycle: polish, bugs, documentation and tech debt first (new features allowed, refinement the focus).
The three together are a **Revolution**.

| Long name | Short |
|---|---|
| Revolution 1, Cycle 1 (Forward) | R1C1F |
| Revolution 1, Cycle 2 (Forward) | R1C2F |
| Revolution 1, Cycle 3 (Horizon) | R1C3H |
| Revolution 2, Cycle 1 (Forward) | R2C1F |

Presentations and demos say the long name, with the dates the cycle ran in smaller text beneath it. Each cycle is a
Redmine version (T-582's "a version per loop"), and every ticket reviewed in a demo carries its cycle.

**A demo follows every cycle. A retro follows every Horizon cycle**, and may follow any other.

**Before R1C1F** work goes on as it does now. In the days before Monday 30 November the Revolution Backlog is
groomed and the first Cycle Backlog drawn from it.

## A ticket's way (the user, 2026-11-25)

```
Backlog -> Revolution Backlog -> Cycle Backlog -> Ready for Development -> In Progress -> (Code Review) -> Closed
                                                                     \-> Awaiting Feedback -> In Progress
```

| Status | Means |
|---|---|
| **Backlog** | uncategorised; every ticket that was Ready on 2026-11-25 starts here |
| **Revolution Backlog** | wanted within this Revolution's three cycles |
| **Cycle Backlog** | drawn from the Revolution Backlog for this cycle: can be assigned and picked up. Unfinished at the cycle's end, it carries into the next cycle, which is then topped up from the Revolution Backlog |
| **Ready for Development** | a lane is assigned |
| **In Progress** | the lane's agent has started |
| **Code Review** | needs more eyes: **two other lanes' agents** each review the diff and post a note in the ticket (approve, or the changes needed). Also how a ticket asks for the user's own eyes |
| **Awaiting Feedback** | a question is posted (below); it returns to In Progress with the answer as a comment |

Blocked, Deferred, Closed and Superseded stay; Needs decision becomes Awaiting Feedback.

**Grooming**: before each cycle the ops lane proposes, ranked by priority and age, what goes into the Revolution
Backlog (before a Revolution) and the Cycle Backlog (before each cycle); the user ticks it on a page. With no answer by
the Monday, the top of the list goes in.

**Awaiting Feedback.** The agent's comment starts **`Requesting Feedback From: @<account>`**. Tagging the admin
account asks the user; tagging a lane's account asks that lane's agent, which answers in the ticket, the way sessions
message each other. A question is either free text or about four choices plus *Other* with a text box; the answer is
recorded either way. On the dashboard the waiting tickets filter in one click and **anyone can read a question**; a
click on it asks a signed-out visitor to sign in, then opens a modal with the question and its choices or a text area.
Answering records the reply as a comment and moves the ticket back to In Progress.

**Agents talking, on the dashboard.** A small widget with the number of active agent-to-agent questions. A click opens
a modal listing them (**active**, or **all** by a toggle): one row each, thick enough for two lines -- the question,
truncated, with the asking daemon's sprite to its left, and under it the answer, truncated, beside the answering
daemon's sprite. The ticket's small number heads the row and links to Redmine. A click on a row shows it in full in the
same modal, a back arrow top left to the list; every modal has an **X** top right and **[Full View]** to open it in a
new tab.

## The folder

```
FRM/
  index.html                  every Revolution, its cycles grouped, a line on what each achieved; demos and retros linked
  R1C1F Forward/demo.html
  R1C2F Forward/demo.html
  R1C3H Horizon/demo.html
  R1C3H Horizon/retro.html
```

Each cycle's folder also holds the demo's screenshots, slides and one audio file per feature.

## A demo page

One section per **feature** (one or more tickets closed in the cycle):

- the feature's name, links to each of its tickets, one description of the whole feature, and any QA feedback;
- small sprites of every contributor (each lane's daemon), and its **presentation**: one audio file, led by the
  lane lead's daemon in its own voice -- *"Hi, I'm <daemon>, I handled the <lane> lane and will be presenting
  <feature>."* Other contributing daemons may speak in the same file, each in its own voice, like a real demo;
- screenshots, and slides the daemon makes for anything else it wants to show, changed by timestamps in the audio;
- **for a signed-in admin**, a checkbox that opens a free-text field: input, a change request, or praise;
- **Ask about this feature** (below), open to everyone by default.

At the bottom, **Submit** reads each feature that has feedback and, where it asks for a change, opens a ticket with it:
related to the demo's tickets, tagged with the demo it came from.

Signed out, a demo or retro is **read-only**. A settings page lets a signed-in user choose what is public and what
needs a sign-in.

## Ask about this feature

A modal with the daemon's sprite, the feature's name and its short description, and a text box. The question goes to
the model with the daemon's persona, the tickets as context and the conversation so far; the answer comes back as text
and is spoken in the daemon's voice. With several contributors, the one best suited answers, and its sprite appears and
moves as it speaks.

- A **speaker** icon under the text box, with a note that the daemon will speak its reply. Clicked, it becomes a muted
  speaker: text only, the daemon still shown.
- The replies scroll in rounded bubbles, iMessage-like: one colour for the asker's, with the overworld monkey as their
  avatar, another for the daemon's, with the sprite of the daemon that answered.
- Unmuted, each daemon bubble has a **play** button to hear it again; while it speaks the button is **HUSH**.
- **One voice at a time**: playing another bubble, or a new reply arriving, hushes whatever was playing, without asking.

## The dashboard's daemons speak

The dashboard shows each lane's daemon at three depths: the **home dashboard**, the **modal** (opened by clicking the
box) and the **full view** (from the modal). In all three, the daemon shows it is working, and:

- **hovering on the daemon** shows a **play** overlay; play asks it to say what it is doing, in its own voice. While it
  thinks, the overlay is **stop** (abort the request); while it speaks, **HUSH**. The overlays show only on hover;
- a box whose daemon is answering looks slightly different;
- **one daemon at a time**: playing another while one is preparing asks *"<daemon> in the <area> lane is still
  preparing your response; if you proceed here, the other request will be stopped"* -- **Proceed** or **Wait**.

**Depth builds, never repeats.** The home dashboard: about one sentence, *"Hi, I am <daemon>, I am working on ..."*,
what and how far along. The modal: no more than a paragraph, from the modal's contents, the detail the sentence left
out. The full view: a few paragraphs at most, what the other two did not cover, and the questions waiting on the user.

**Persona and voice are shared, not rewritten.** The same persona function the companion uses (the daemon's
first-person INDEX entry, its type and the rest, made into a paragraph on how it speaks) and the same voice-recipe
function make each daemon's voice, here and in the demos, so a daemon sounds the same everywhere. A voice may be saved
once made.

**The daemons are chosen to fit the work**: the dashboard already picks a daemon to represent each lane's work (a
signed-in user can pick another). The **QA lanes** get daemons the same way: one QA type, and within it a daemon fitting
each area.

## QA

Three QA lanes, each its own Redmine user and daemon, for areas that do not block each other: **the game** (the ROMs),
**the companion** (app, hub, boards) and **the site** (EUDAIMONIA). A QA lane reads a closed ticket and its acceptance
criteria and tests it -- a sanity check, a scripted play route, or a full feature check -- **after** the release, never
holding it; a failure reopens the ticket or opens a bug. Its notes appear in the cycle's demo.

## The release routine, alongside

The same day's choices, from LaunchDarkly's Release Autopilot built ourselves: the push routine as a plan the ops lane
owns, risk-scored gates, guardrails (a budget overrun or a failed smoke test **stops** a push; a changed save layout or
a slowdown only **notifies**), a clean-up list after each release, and the lane recorded on every step.

## Tickets (opened 2026-11-25)

| | |
|---|---|
| T-640 | the push routine as a plan, with status, resume and the lane on every step (ops) |
| T-641 | risk-scored gates (ops) |
| T-642 | guardrails: budget and smoke test halt; save layout and slowdown notify (ops) |
| T-643 | the smoke test on every ROM release (ops) |
| T-644 | the clean-up list after each release (ops) |
| T-645 | the local risk question, after C-516 (ops) |
| T-646 | the three QA lanes (ops) |
| T-647 | cycles as Redmine versions, one week each (ops; builds on T-582) |
| T-648 | the FRM pages: demos, retros and the index (ops) |
| T-649 | the demo presentations' audio (audio) |
| E-27 | FRM on EUDAIMONIA, feedback and Submit (playground) |
| E-28 | Ask about this feature (playground) |
| E-29 | the dashboard's daemons speak (playground) |
| T-650 | Redmine's new statuses and workflow (ops) |
| T-651 | grooming the Revolution and Cycle Backlogs (ops) |
| T-652 | Code Review by two lanes' agents (ops) |
| T-653 | Requesting Feedback From: agents ask agents (ops) |
| E-30 | Awaiting Feedback answered on the dashboard (playground) |
| E-31 | the agents-talking widget (playground) |
