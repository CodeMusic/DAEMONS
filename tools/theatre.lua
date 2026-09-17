-- The theatre's remote (T-136): drive mGBA from a file, frame-exact, and capture what it shows.
--
-- mGBA 0.10.5 has no --script (engineAi/README.md), so load this once from the Scripting window
-- (Tools > Scripting..., then File > Load script...). It then polls a command file every 10 frames:
--
--     <dir>/theatre.cmd       written by you; a new first line "id N" starts a new batch
--     <dir>/theatre.done     written here: "done N" once batch N has run
--
-- One command per line, run in order:
--     hold A 6          hold a button (A B L R START SELECT UP DOWN LEFT RIGHT) for N frames, then release
--     wait 30           let N frames pass
--     shot name         save a screenshot as <dir>/name.png
--     burst name 12 4   save 12 screenshots, one every 4 frames: <dir>/name_00.png ... (an animation, as frames)
--     poke16 ADDR N     write a 16-bit value into memory (the theatre's sTheatreMove, from the .elf's symbols)
--
-- Why a file and not keystrokes: a key tapped into the window from outside lands on about half the
-- frames the game polls, and a menu cannot be driven by input that may or may not arrive. A button
-- held here is held for exactly the frames asked.

-- <dir> is .theatre/ at the repo root (gitignored), found from where this script lives.
local HERE = debug.getinfo(1, "S").source:match("^@(.*)/[^/]*$") or "."
local DIR = HERE .. "/../.theatre"
local CMD, DONE = DIR .. "/theatre.cmd", DIR .. "/theatre.done"
local KEYS = { A = C.GBA_KEY.A, B = C.GBA_KEY.B, L = C.GBA_KEY.L, R = C.GBA_KEY.R,
               START = C.GBA_KEY.START, SELECT = C.GBA_KEY.SELECT,
               UP = C.GBA_KEY.UP, DOWN = C.GBA_KEY.DOWN, LEFT = C.GBA_KEY.LEFT, RIGHT = C.GBA_KEY.RIGHT }

local lastId, queue, busy, frame = nil, {}, nil, 0

-- A batch already in the command file when the script loads is OLD: reloading once replayed a finished
-- 620-command capture from the top. Remember its id so only a batch written after loading runs.
do
  local f = io.open(CMD, "r")
  if f then lastId = (f:read("a") or ""):match("^id (%S+)"); f:close() end
end

local function readBatch()
  local f = io.open(CMD, "r")
  if not f then return end
  local text = f:read("a"); f:close()
  local id = text:match("^id (%S+)")
  if not id or id == lastId then return end
  lastId, queue = id, {}
  for line in text:gmatch("[^\n]+") do
    local w = {}
    for t in line:gmatch("%S+") do w[#w + 1] = t end
    if w[1] ~= "id" and w[1] then queue[#queue + 1] = w end
  end
  console:log("theatre: batch " .. id .. ", " .. #queue .. " commands")
end

local function finish()
  local f = io.open(DONE, "w")
  if f then f:write("done " .. tostring(lastId) .. "\n"); f:close() end
end

-- Loading the script again replaces the running copy instead of adding a second frame callback beside it.
if THEATRE_CALLBACK then callbacks:remove(THEATRE_CALLBACK) end
THEATRE_CALLBACK = callbacks:add("frame", function()
  frame = frame + 1
  if busy then
    busy.left = busy.left - 1
    if busy.kind == "burst" and busy.left % busy.every == 0 then
      emu:screenshot(string.format("%s/%s_%02d.png", DIR, busy.name, busy.n))
      busy.n = busy.n + 1
    end
    if busy.left > 0 then return end
    if busy.kind == "hold" then emu:clearKey(busy.key) end
    busy = nil
    if #queue == 0 then finish() end
    return
  end
  if #queue == 0 then
    if frame % 10 == 0 then readBatch() end
    return
  end
  local w = table.remove(queue, 1)
  if w[1] == "hold" and KEYS[w[2]] then
    emu:addKey(KEYS[w[2]])
    busy = { kind = "hold", key = KEYS[w[2]], left = tonumber(w[3]) or 4 }
  elseif w[1] == "wait" then
    busy = { kind = "wait", left = tonumber(w[2]) or 1 }
  elseif w[1] == "poke16" then
    -- write a 16-bit value into the game's memory: `poke16 0x0203xxxx 105` sets the theatre's routine directly.
    -- Stepping to it with the D-pad drifts, because the theatre ignores input while an animation is still
    -- playing, and a long one swallows the steps that follow it (T-142's first sheet showed the wrong routines).
    emu:write16(tonumber(w[2]), tonumber(w[3]))
    if #queue == 0 then finish() end
  elseif w[1] == "shot" then
    emu:screenshot(DIR .. "/" .. w[2] .. ".png")
    if #queue == 0 then finish() end
  elseif w[1] == "burst" then
    local count, every = tonumber(w[3]) or 8, tonumber(w[4]) or 4
    busy = { kind = "burst", name = w[2], n = 0, every = every, left = count * every }
  else
    console:log("theatre: unknown command " .. table.concat(w, " "))
    if #queue == 0 then finish() end
  end
end)

console:log("theatre: watching " .. CMD)
