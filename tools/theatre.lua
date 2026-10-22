-- The theatre's remote (T-136): drive mGBA from a file, frame-exact, and capture what it shows.
--
-- mGBA 0.10.5 has no --script (engineAi/README.md), so load this once from the Scripting window
-- (Tools > Scripting..., then File > Load script...), or type into that window's own input line
--     dofile("/Users/christopherhicks/Projects/DAEMONS/tools/theatre.lua")
-- which needs no file dialog. Quitting mGBA unloads it. It then polls a command file every 10 frames:
--
--     <dir>/theatre.cmd       written by you; a new first line "id N" starts a new batch
--     <dir>/theatre.done     written here: "done N" once batch N has run
--
-- One command per line, run in order:
--     hold A 6          hold a button (A B L R START SELECT UP DOWN LEFT RIGHT) for N frames, then release
--     press R           put a button down and LEAVE it down while later commands run (a shot mid-hold)
--     release R         and let it go
--     wait 30           let N frames pass
--     shot name         save a screenshot as <dir>/name.png
--     burst name 12 4   save 12 screenshots, one every 4 frames: <dir>/name_00.png ... (an animation, as frames)
--     pburst name 40    every frame for 40 frames: a screenshot AND palette RAM, <dir>/name_00.png + name_00.pal
--                       (1024 bytes, BG then OBJ) -- for a colour that should not be on screen (T-254)
--     poke16 ADDR N     write a 16-bit value into memory (the theatre's sTheatreMove, from the .elf's symbols)
--     poke8 ADDR N      write one byte (sTheatreTurn: 1 films a two-turn routine's second half)
--     peek 32 ADDR name read 8/16/32 bits and append "name value" to <dir>/peek.txt
--     trace name 120 32:ADDR 8:ADDR d8:ADDR ...
--                       every frame for 120 frames, one line of the values to <dir>/name.trace (8/16/32 bits;
--                       d8 reads the 32-bit pointer at ADDR and then the byte it points to) -- for counting
--                       frames: T-392 P2 measured each routine's signature past its picture this way
--     load /abs/x.gba   another ROM (and its save), from the top; reset; savestate PATH / loadstate PATH
--     reload            run this file again (a fix to the script, without a hand at the Scripting window)
--
-- REFUSED, not acted on (2026-10-21): a poke outside EWRAM, IWRAM, palette, VRAM or OAM; a peek or trace address
-- outside the GBA's memory map; a `load` whose path is not absolute or not there. The batch stops and theatre.done
-- reads "done N refused: why" (tools/theatre_walk.py raises it).
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

local function finish(err)
  local f = io.open(DONE, "w")
  if f then f:write("done " .. tostring(lastId) .. (err and (" refused: " .. err) or "") .. "\n"); f:close() end
end

-- Guards (2026-10-21: a `load` with a relative path took the theatre down, and it had to be started again by hand).
-- A command that would act on something outside the GBA's memory map, or load a ROM by a path that is not absolute
-- and present, is REFUSED: the rest of the batch is dropped and theatre.done says why ("done N refused: ..."), which
-- tools/theatre_walk.py raises as an error. Nothing is read, written or loaded.
local READABLE = {   -- {first, last}: EWRAM, IWRAM, I/O, palette, VRAM, OAM, ROM
  {0x02000000, 0x0203FFFF}, {0x03000000, 0x03007FFF}, {0x04000000, 0x040003FF}, {0x05000000, 0x050003FF},
  {0x06000000, 0x06017FFF}, {0x07000000, 0x070003FF}, {0x08000000, 0x09FFFFFF},
}
local function addrOK(a, size, writing)
  if type(a) ~= "number" or a ~= math.floor(a) then return false end
  local last = a + (size or 8) // 8 - 1
  for i, r in ipairs(READABLE) do
    if a >= r[1] and last <= r[2] then return not (writing and (i == 3 or i == 7)) end   -- never write I/O or ROM
  end
  return false
end
local function isFile(path)
  local f = io.open(path, "rb")
  if f then f:close() return true end
  return false
end
local SELF = debug.getinfo(1, "S").source:gsub("^@", "")   -- this file, for `reload`
local function refuse(why)
  console:log("theatre: REFUSED " .. why)
  queue = {}
  busy = nil
  finish(why)
end

-- Loading the script again replaces the running copy instead of adding a second frame callback beside it.
if THEATRE_CALLBACK then callbacks:remove(THEATRE_CALLBACK) end
THEATRE_CALLBACK = callbacks:add("frame", function()
  frame = frame + 1
  if busy then
    busy.left = busy.left - 1
    if busy.kind == "pburst" then
      emu:screenshot(string.format("%s/%s_%02d.png", DIR, busy.name, busy.n))
      local f = io.open(string.format("%s/%s_%02d.pal", DIR, busy.name, busy.n), "wb")
      if f then f:write(emu:readRange(0x05000000, 1024)); f:close() end
      busy.n = busy.n + 1
    end
    if busy.kind == "trace" then
      local vals = {}
      for _, sp in ipairs(busy.specs) do
        local v
        if sp.deref then
          local p = emu:read32(sp.addr)
          v = addrOK(p, 8) and emu:read8(p) or 0   -- a pointer that is not (yet) one reads as 0, never followed
        elseif sp.size == 32 then v = emu:read32(sp.addr)
        elseif sp.size == 16 then v = emu:read16(sp.addr)
        else v = emu:read8(sp.addr) end
        vals[#vals + 1] = string.format("%x", v)
      end
      busy.file:write(table.concat(vals, " ") .. "\n")
      if busy.left == 0 then busy.file:close() end
    end
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
  elseif w[1] == "press" and KEYS[w[2]] then
    emu:addKey(KEYS[w[2]])
    if #queue == 0 then finish() end
  elseif w[1] == "release" and KEYS[w[2]] then
    emu:clearKey(KEYS[w[2]])
    if #queue == 0 then finish() end
  elseif w[1] == "wait" then
    busy = { kind = "wait", left = tonumber(w[2]) or 1 }
  elseif (w[1] == "poke16" or w[1] == "poke8") and not (addrOK(tonumber(w[2]), w[1] == "poke16" and 16 or 8, true)
                                                     and tonumber(w[3])) then
    refuse(table.concat(w, " ") .. ": not a writable GBA address and a value")
  elseif w[1] == "peek" and not ((w[2] == "8" or w[2] == "16" or w[2] == "32") and addrOK(tonumber(w[3]), tonumber(w[2]))) then
    refuse(table.concat(w, " ") .. ": not a GBA address (peek 8|16|32 ADDR NAME)")
  elseif w[1] == "load" and not (w[2] and w[2]:sub(1, 1) == "/" and isFile(table.concat(w, " ", 2))) then
    refuse(table.concat(w, " ") .. ": a ROM is loaded only by an absolute path to a file that is there")
  elseif w[1] == "poke16" then
    -- write a 16-bit value into the game's memory: `poke16 0x0203xxxx 105` sets the theatre's routine directly.
    -- Stepping to it with the D-pad drifts, because the theatre ignores input while an animation is still
    -- playing, and a long one swallows the steps that follow it (T-142's first sheet showed the wrong routines).
    emu:write16(tonumber(w[2]), tonumber(w[3]))
    if #queue == 0 then finish() end
  elseif w[1] == "poke8" then
    -- one byte: the theatre's sTheatreTurn, so a two-turn routine's second half can be filmed
    emu:write8(tonumber(w[2]), tonumber(w[3]))
    if #queue == 0 then finish() end
  elseif w[1] == "peek" then
    -- read memory into <dir>/peek.txt: `peek 32 0x03005008 name` appends "name value". For finding where the player
    -- is (gSaveBlock1Ptr -> location) when driving the game somewhere rather than filming the theatre.
    local size, addr = tonumber(w[2]), tonumber(w[3])
    local v = size == 32 and emu:read32(addr) or size == 16 and emu:read16(addr) or emu:read8(addr)
    local f = io.open(DIR .. "/peek.txt", "a")
    if f then f:write((w[4] or "?") .. " " .. string.format("0x%x", v) .. "\n"); f:close() end
    if #queue == 0 then finish() end
  elseif w[1] == "load" then
    -- T-386: put another ROM in the theatre without touching its window (mGBA 0.10's emu:loadFile): the save beside it
    -- comes too, and the game starts from the top. `load /path/theatre_release.gba`. The path may hold spaces.
    local path = table.concat(w, " ", 2)
    local ok = emu:loadFile(path)
    if ok then emu:autoloadSave(); emu:reset() end
    console:log("theatre: load " .. path .. (ok and "" or " FAILED"))
    if #queue == 0 then finish() end
  elseif w[1] == "reload" then
    -- this script again, from its own file (a fix to it needs no hand at the Scripting window); the batch ends here
    queue = {}
    finish()
    dofile(SELF)
    return
  elseif w[1] == "reset" then
    emu:reset()
    if #queue == 0 then finish() end
  elseif w[1] == "savestate" or w[1] == "loadstate" then
    -- a moment to come back to: a route can start from one instead of playing up to it (`loadstate <dir>/x.ss`)
    local path = table.concat(w, " ", 2)
    local ok
    if w[1] == "savestate" then ok = emu:saveStateFile(path) else ok = emu:loadStateFile(path) end
    if not ok then console:log("theatre: " .. w[1] .. " " .. path .. " FAILED") end
    if #queue == 0 then finish() end
  elseif w[1] == "shot" then
    emu:screenshot(DIR .. "/" .. w[2] .. ".png")
    if #queue == 0 then finish() end
  elseif w[1] == "trace" then
    local specs = {}
    for i = 4, #w do
      local kind, addr = w[i]:match("^(d?%d+):(.+)$")
      -- T-430: a spec that is not a number is dropped, not read: emu:read8(nil) raised every frame and stalled the
      -- remote until the script was loaded again by hand (2026-10-21, "8:0x0x030028f0")
      if tonumber(addr) and addrOK(tonumber(addr), (kind or ""):sub(1, 1) == "d" and 32 or tonumber((kind or "32"):match("%d+"))) then
        specs[#specs + 1] = { size = tonumber((kind or "32"):match("%d+")), deref = (kind or ""):sub(1, 1) == "d",
                              addr = tonumber(addr) }
      else
        console:log("theatre: trace spec " .. w[i] .. " is not an address; skipped")
      end
    end
    busy = { kind = "trace", left = tonumber(w[3]) or 60, specs = specs,
             file = io.open(DIR .. "/" .. w[2] .. ".trace", "w") }
  elseif w[1] == "pburst" then
    busy = { kind = "pburst", name = w[2], n = 0, left = tonumber(w[3]) or 30 }
  elseif w[1] == "burst" then
    local count, every = tonumber(w[3]) or 8, tonumber(w[4]) or 4
    busy = { kind = "burst", name = w[2], n = 0, every = every, left = count * every }
  else
    console:log("theatre: unknown command " .. table.concat(w, " "))
    if #queue == 0 then finish() end
  end
end)

console:log("theatre: watching " .. CMD)
