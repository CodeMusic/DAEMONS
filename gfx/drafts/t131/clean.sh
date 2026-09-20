#!/bin/bash
# T-131's twelve: clean each picked draft into gfx/drafts/t131/clean/, per PICKS.txt. Run from the repo root.
cd /Users/christopherhicks/Projects/DAEMONS
A=gfx/drafts/t131/alt
C=gfx/drafts/t131/clean
mkdir -p $C
while read -r name view stem; do
  [ -z "$name" ] && continue
  python3 tools/cleandraft.py $A/$stem.png $C/${name}_${view}.png --streaks 2>&1 | tail -1 | sed "s|^|  ${name}_${view}  |"
done <<'LIST'
poll front poll_front_1917
poll back poll_back_42
watchdog front watchdog_front_1917
watchdog back watchdog_back_r27
pilot front pilot_front_r27
pilot back pilot_back_r27
sounding front sounding_front_42
sounding back sounding_back_r27
starved front starved_front_r27
starved back starved_back_r21917
quota front quota_front_r27
quota back quota_back_r37
fakeroot front fakeroot_front_r21917
fakeroot back fakeroot_back_r31917
warning front warning_front_1917
warning back warning_back_1917
cache front cache_front_42
cache back cache_back_r27
triton front triton_front_1917
triton back triton_back_r27
phoenix front phoenix_front_42
phoenix back phoenix_back_r27
LIST
