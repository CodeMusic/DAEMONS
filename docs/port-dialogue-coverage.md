# Game Boy dialogue: where every block went

**569 blocks, all accounted for.** Regenerate with `python3 tools/port_dialogue.py`.

| | |
|---|---|
| matched to a Gen 3 block | **536** |
| handled elsewhere | **4** |
| vocabulary only — nothing to carry | **29** |
| still without a home | **0** |

## Matched

Paired on **vanilla against vanilla** — Gen 1's original line against Gen 3's,
each from its own fork's `upstream/master`. The winner has to beat the
runner-up, unless it scores above 0.85, where a tie is between twins.

**9** of them were placed by hand, in `MANUAL`, where the scoring could not
decide and a person could.

## Handled elsewhere

Two are ours outright and were placed as new `bg_events` — they replace no
vanilla line, so there was nothing to match them against. Two more were
merged: Gen 1 splits CAIRN's award and its explanation across two blocks and
Gen 3 says both in one, wrapped around the badge fanfare.

## Vocabulary only

These carry no writing of ours — their only edit was a rename, and
`port_vocab.py` and `port_oak.py` already made it on the Gen 3 side,
independently and everywhere. Porting them would change nothing.

- **CeruleanCity** — `CeruleanCityTrainerTipsText`
- **FuchsiaGym_2** — `FuchsiaGymRocker6EndBattleText`
- **MrFujisHouse** — `MrFujisHouseMrFujiIThinkThisMayHelpYourQuestText`
- **OaksLab** — `OaksLabOak1YourPokemonCanFightText`
- **Route11** — `Route11Youngster2EndBattleText`
- **Route14** — `Route14CooltrainerM4AfterBattleText`, `Route14CooltrainerM5AfterBattleText`
- **Route15** — `Route15Beauty2AfterBattleText`
- **Route16** — `Route16Biker4AfterBattleText`
- **Route22** — `Route22Rival1VictoryText`
- **Route22Gate** — `Route22GateGuardGoRightAheadText`, `Route22GateGuardNoBoulderbadgeText`
- **SSAnne1FRooms** — `SSAnne1FRoomsCooltrainerFBattleText`, `SSAnne1FRoomsGentleman1BattleText`, `SSAnne1FRoomsGentleman3Text`, `SSAnne1FRoomsYoungsterAfterBattleText`
- **SSAnne2F** — `SSAnne2FRivalText`, `SSAnne2FWaiterText`
- **SSAnne2FRooms** — `SSAnne2FRoomsGentleman4Text`
- **SSAnneB1FRooms** — `SSAnneB1FRoomsFisherBattleText`, `SSAnneB1FRoomsSailor3AfterBattleText`
- **SafariZoneWestRestHouse** — `SafariZoneWestRestHouseCooltrainerMText`
- **SaffronGates** — `SaffronGateGuardYouCanGoOnThroughText`
- **SaffronGym** — `SaffronGymChanneler2AfterBattleText`
- **SaffronPokecenter** — `SaffronPokecenterGentlemanText`
- **UndergroundPathRoute7Copy** — `UndergroundPathRoute7CopyUnusedGirlText`, `UndergroundPathRoute7CopyUnusedGoesUnderSaffronText`, `UndergroundPathRoute7CopyUnusedMiddleAgedManText`, `UndergroundPathRoute7CopyUnusedTeamRocketHadAHideoutText`
