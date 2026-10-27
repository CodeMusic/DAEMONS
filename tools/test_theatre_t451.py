"""T-451 offline tests: the theatre tools' limits, ping, and the door-mat warp, against a fake theatre.

    python3 tools/test_theatre_t451.py          (about 25 s; no mGBA, no theatre, no save)

Nothing here talks to mGBA. The transport tests use a temp dir as .theatre/ with a thread that answers (or does not);
the walker tests replace run/peek with a simulated player on the real maps' collision and behaviours.
"""
import importlib, os, sys, tempfile, threading, time, json, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
WHICH = "new"
sys.path.insert(0, HERE)
import theatre_walk as tw                                        # noqa: E402
tw.ROOT, tw.GBA = REPO, os.path.join(REPO, "engineGba")


# -- a simulated player ------------------------------------------------------------------------------------------------
GROUPS = json.load(open(os.path.join(tw.GBA, "data/maps/map_groups.json")))


def index_of(name):
    for gi, gname in enumerate(GROUPS["group_order"]):
        if name in GROUPS[gname]:
            return gi, GROUPS[gname].index(name)
    raise KeyError(name)


class Sim:
    """FireRed's field input, as much of it as a mat needs: a hold under 8 frames facing elsewhere only turns; a hold
    otherwise walks a tile each 16 frames it lasts (a started step finishes); standing on a tile with the button held
    the way the player faces, an ARROW warp there fires (TryArrowWarp), and stepping onto a step-on warp fires."""

    def __init__(self, mapname, x, y, facing="DOWN"):
        self.m = tw.Map(mapname)
        self.warps = {(w["x"], w["y"]) for w in self.m.json.get("warp_events") or []}
        self.map, self.x, self.y, self.facing = index_of(mapname), x, y, facing
        self.presses = 0
        self.warped_from = None

    def passable(self, x, y):
        return self.m.inside(x, y) and not (self.m.cell(x, y) >> 10) & 3 and (x, y) not in self.m.still

    def fire(self, how):
        self.warped_from = (self.x, self.y)
        self.map, self.x, self.y = (99, 99), 5, 5                       # somewhere else

    def hold(self, d, n):
        self.presses += 1
        if self.map == (99, 99):
            return
        if self.facing != d and n < 8:
            self.facing = d
            return
        self.facing = d
        left = n
        while left > 0:
            b = self.m.behaviour(self.x, self.y)
            if (self.x, self.y) in self.warps and tw_press(b) == d:
                return self.fire("press")
            nx, ny = self.x + tw.DIRS[d][0], self.y + tw.DIRS[d][1]
            if not self.passable(nx, ny):
                return
            self.x, self.y = nx, ny
            left -= 16
            if (nx, ny) in self.warps and self.m.behaviour(nx, ny) in STEP:
                return self.fire("step")

    # tw.run / tw.peek stand-ins
    def run(self, *cmds):
        for c in cmds:
            w = c.split()
            if w[0] == "hold" and w[1] in tw.DIRS:
                self.hold(w[1], int(w[2]))

    def peek(self, reads):
        vals = {"sb1": 0x02020000, "x": self.x, "y": self.y, "group": self.map[0], "num": self.map[1],
                "flags": 0, "avatar": 1, "p": 0x02020000, "b": 0}
        return {n: vals.get(n, 0) for _, _, n in reads}


PRESS = {0x62: "RIGHT", 0x63: "LEFT", 0x64: "UP", 0x65: "DOWN", 0x6C: "RIGHT", 0x6E: "RIGHT", 0x6D: "LEFT", 0x6F: "LEFT"}
STEP = {0x60, 0x61, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x6B, 0x71}


def tw_press(b):
    return PRESS.get(b)


def install(sim):
    tw.run, tw.peek = sim.run, sim.peek
    # map_name for the fake "elsewhere" map
    real = tw.map_name.__wrapped__ if hasattr(tw.map_name, "__wrapped__") else tw.map_name

    def map_name(g, n):
        return "ELSEWHERE" if (g, n) == (99, 99) else real(g, n)
    map_name.__wrapped__ = real
    tw.map_name = map_name


def choose(m, here, dest):
    if hasattr(tw, "choose_warp"):
        return tw.choose_warp(m, here, dest)
    hits = [w for w in m.json["warp_events"] if w["dest_map"] == dest]
    tiles = {(w["x"], w["y"]) for w in hits}
    return min(hits, key=lambda w: (m.path(here, (w["x"], w["y"])) is None,
                                    -sum((w["x"] + dx, w["y"]) in tiles for dx in (-1, 1)),
                                    len(m.path(here, (w["x"], w["y"])) or ())))


def warp_out(mapname, start, dest="MAP_CELADON_CITY"):
    """Play `warp DEST` from START on the simulated map. Returns (result, sim): result is the state, or the exit text."""
    sim = Sim(mapname, *start)
    install(sim)
    g = tw.Game(False)
    m = tw.Map(mapname, walking=True) if WHICH == "new" else tw.Map(mapname)
    best = choose(m, start, dest)
    try:
        return tw.walk(g, (best["x"], best["y"]), into_warp=True), sim, best
    except SystemExit as e:
        return "EXIT: %s" % e, sim, best


class MatTests(unittest.TestCase):
    def test_restaurant_from_the_coin_case_man(self):
        """mom-tour stop 9: after talking to the man at (1,2) the player stands at (1,3); the path to the mat runs
        along row 9 and arrives on the arrow tile (6,9) from the side."""
        res, sim, best = warp_out("CeladonCity_Restaurant", (1, 3))
        print("\n  restaurant: chose %s, %s, %d presses, fired from %s" % ((best["x"], best["y"]),
              res if isinstance(res, str) else "warped", sim.presses, sim.warped_from))
        self.assertNotIsInstance(res, str)
        self.assertEqual(sim.warped_from, (6, 9))

    def test_game_corner_from_the_counter(self):
        """mom-tour stop 9: from around the room to the mat; its arrow is the LEFT end."""
        for start in ((3, 7), (8, 11), (12, 12), (9, 12), (11, 12), (14, 13), (16, 5)):
            res, sim, best = warp_out("CeladonCity_GameCorner", start)
            print("\n  game corner from %s: chose %s, %s, %d presses, fired from %s" % (start, (best["x"], best["y"]),
                  res if isinstance(res, str) else "warped", sim.presses, sim.warped_from))
            self.assertNotIsInstance(res, str)
            self.assertEqual(sim.warped_from, (9, 13))

    def test_players_house(self):
        res, sim, best = warp_out("PalletTown_PlayersHouse_1F", (8, 4), "MAP_PALLET_TOWN")
        print("\n  player's house: chose %s, fired from %s" % ((best["x"], best["y"]), sim.warped_from))
        self.assertEqual(sim.warped_from, (4, 8))


# -- the transport: limits and ping --------------------------------------------------------------------------------------
@unittest.skipIf(WHICH == "orig", "the new transport only")
class TransportTests(unittest.TestCase):
    def setUp(self):
        importlib.reload(tw)
        tw.ROOT, tw.GBA = REPO, os.path.join(REPO, "engineGba")
        self.dir = tempfile.mkdtemp(prefix="theatre_")
        tw.THEATRE = self.dir
        tw.BATCH_SLACK = 1
        self.stop = threading.Event()

    def tearDown(self):
        self.stop.set()

    def responder(self, delay=0.0, refuse=False, frames_per_s=600):
        """A fake theatre.lua: reads theatre.cmd every 20 ms, 'plays' it at FRAMES_PER_S, writes theatre.done."""
        def loop():
            last = None
            while not self.stop.is_set():
                try:
                    text = open(os.path.join(self.dir, "theatre.cmd")).read()
                except OSError:
                    text = ""
                bid = text.split("\n", 1)[0][3:] if text.startswith("id ") else None
                if bid and bid != last:
                    last = bid
                    cmds = text.split("\n")[1:-1]
                    time.sleep(delay + tw.batch_frames(cmds) / frames_per_s)
                    open(os.path.join(self.dir, "theatre.done"), "w").write(
                        "done %s%s\n" % (bid, " refused: poke8 0x0 1: not a writable GBA address" if refuse else ""))
                time.sleep(0.02)
        threading.Thread(target=loop, daemon=True).start()

    def test_batch_frames(self):
        self.assertEqual(tw.batch_frames(["hold A 6", "wait 50", "burst x 12 4", "shot a", "load /x.gba"]),
                         6 + 50 + 48 + 1 + tw.LOAD_FRAMES)

    def test_ping_answered_fast(self):
        self.responder()
        t = time.monotonic()
        tw.ping(5)
        self.assertLess(time.monotonic() - t, 1.0)

    def test_ping_unanswered_fails_in_its_seconds(self):
        t = time.monotonic()
        with self.assertRaises(tw.TheatreDown) as cm:
            tw.ping(1.5)
        took = time.monotonic() - t
        print("\n  ping, nobody listening: %.2f s -- %s" % (took, cm.exception))
        self.assertLess(took, 2.5)
        self.assertIn("not answering", str(cm.exception))
        self.assertIn("theatre.lua", str(cm.exception))

    def test_run_unanswered_is_down_not_forever(self):
        t = time.monotonic()
        with self.assertRaises(tw.TheatreDown):
            tw.run("hold A 6", "wait 30")                       # 36 frames: 1 + 3 * 0.6 = 2.8 s
        self.assertLess(time.monotonic() - t, 4)

    def test_refused_is_a_theatre_error(self):
        self.responder(refuse=True)
        with self.assertRaises(tw.TheatreError) as cm:
            tw.run("poke8 0x0 1")
        self.assertNotIsInstance(cm.exception, tw.TheatreDown)

    def test_limit_stops_a_loop_that_never_ends(self):
        """The shape of the old bug: a loop that keeps pressing and never gets there. limit() ends it."""
        self.responder()
        t, n = time.monotonic(), 0
        with self.assertRaises(tw.TheatreTimeout) as cm:
            with tw.limit(1.0, "stop 9"):
                while True:
                    tw.run("hold RIGHT 12", "wait 16")
                    n += 1
        print("\n  endless loop under limit(1 s): stopped after %d batches, %.2f s -- %s"
              % (n, time.monotonic() - t, cm.exception))
        self.assertLess(time.monotonic() - t, 2.0)
        self.assertIn("stop 9", str(cm.exception))

    def test_limit_caps_a_long_batch(self):
        """A batch longer than the limit left is cut at the limit, and reported as the limit, not as the theatre down."""
        self.responder(frames_per_s=60)
        t = time.monotonic()
        with self.assertRaises(tw.TheatreTimeout):
            with tw.limit(1.0, "stop 3"):
                tw.run("wait 600")                                # ten seconds of frames
        self.assertLess(time.monotonic() - t, 2.0)

    def test_nested_limits_the_nearest_wins(self):
        self.responder()
        with tw.limit(30, "stop 1"):
            with self.assertRaises(tw.TheatreTimeout) as cm:
                with tw.limit(0.5, "walking"):
                    while True:
                        tw.run("wait 1")
            self.assertIn("walking", str(cm.exception))
            tw.run("wait 1")                                       # the outer limit still has time

    @unittest.skipIf(WHICH == "orig", "new only")
    def test_walk_bounded_by_circles(self):
        """A player that bounces between two tiles forever (the old mat): walk() exits on the twelfth return."""
        importlib.reload(tw)
        tw.ROOT, tw.GBA = REPO, os.path.join(REPO, "engineGba")
        sim = Sim("CeladonCity_Restaurant", 5, 9)
        install(sim)
        orig_hold = sim.hold

        def bounce(d, n):                                          # every press lands on the other tile
            sim.presses += 1
            sim.x = 6 if sim.x == 5 else 5
        sim.hold = bounce
        g = tw.Game(False)
        with self.assertRaises(SystemExit) as cm:
            tw.walk(g, (8, 5))
        print("\n  bouncing player: %s after %d presses" % (cm.exception, sim.presses))
        self.assertIn("circle", str(cm.exception))


@unittest.skipIf(WHICH == "orig", "the new runner only")
class RouteTests(TransportTests):
    """theatre_route.py: a stop past its limit fails and the route goes on; a theatre that stops answering ends the run."""

    def runner(self):
        import theatre_route as tr
        importlib.reload(tr)
        tr.tw = tw
        r = object.__new__(tr.Runner)
        r.out = tempfile.mkdtemp(prefix="route_")
        r.stop_seconds, r.release, r.said = tr.STOP_SECONDS, False, []
        r.capture = lambda *a, **k: None
        return tr, r

    def test_stop_past_its_limit_fails_with_a_message(self):
        self.responder()
        tr, r = self.runner()

        def step(line):                                  # a step that never gets there
            while True:
                tw.run("hold RIGHT 12", "wait 16")
        r.step = step
        t = time.monotonic()
        failed, sheet, said = r.play(9, {"stop": "the GAME CORNER", "timeout": 1, "steps": ["warp MAP_CELADON_CITY"]})
        print("\n  stop with timeout 1: %.2f s -- %s" % (time.monotonic() - t, failed))
        self.assertLess(time.monotonic() - t, 3)
        self.assertIn("stop 9 ran past its limit of 1 s", failed)

    def test_theatre_down_mid_stop_raises(self):
        tr, r = self.runner()                             # no responder: the first batch goes unanswered
        r.step = lambda line: tw.run("wait 30")
        t = time.monotonic()
        with self.assertRaises(tw.TheatreDown) as cm:
            r.play(1, {"stop": "one", "steps": ["wait 30"]})
        print("\n  theatre down mid-stop: %.2f s -- %s" % (time.monotonic() - t, cm.exception))
        self.assertLess(time.monotonic() - t, 4)

    def test_route_main_pings_first(self):
        tr, r = self.runner()
        route = os.path.join(self.dir, "r.json")
        json.dump({"rom": "debug", "stops": [{"stop": "one", "steps": ["wait 10"]}]}, open(route, "w"))
        sys.argv = ["theatre_route.py", route]
        t = time.monotonic()
        with self.assertRaises(SystemExit) as cm:
            tr.main()
        print("\n  route with nobody listening: %.2f s -- %s" % (time.monotonic() - t, cm.exception))
        self.assertLess(time.monotonic() - t, tw.PING_SECONDS + 1.5)
        self.assertIn("not answering", str(cm.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
