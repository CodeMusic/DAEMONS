# gfx/

Original sprite work. **No commercial assets, ever.**

Constraints, from vision.md 8.3:

- 2bpp, four shades, 56×56 maximum for daemon front sprites
- Front and back for every daemon
- Overworld sprites are 16×16 — silhouette has to carry at that size

This is the project's largest block of labor and the reason for the vertical
slice: **12 daemons before 151.** AI generation can rough out silhouettes, but
expect manual cleanup — the Game Boy palette and tile constraints are unforgiving.

## Layout (mirrors pokered)

```
front/      daemon front sprites
back/       daemon back sprites
overworld/  16x16 overworld sprites
ui/         title screen, menus, Index chrome
```
