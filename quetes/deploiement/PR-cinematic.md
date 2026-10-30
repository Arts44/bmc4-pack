# Brouillon de PR pour dcvke/CinematicInteractions — à ne pas envoyer sans accord d'Arthur

**Titre :** fix(forge): ask block protection before starting a station on the server

On Forge 1.20.1 the BEGIN and WINDOW actions of `StationActionPayload` open a
station after checking only its kind, spectator mode and distance. The real use is
cancelled by the mod, so a server with a claim or lock mod never asks it: a player
can open furnaces, brewing stands, jukeboxes and so on inside someone else's claim.

`Sessions` now applies `player.mayInteract`, then posts a `RightClickBlock` on the
server before opening anything. `StationEvents` ends that event where it ends a real
use, so listeners after it do not run for a use that is not happening. A refusal
closes the scene and any session the player still had.

The probe flag is only read on the server side: in singleplayer the client and the
integrated server share `Sessions`' static fields.

Known limit: `valid()` does not ask again. A session opened while the player was
allowed (during a raid, on our server) survives the end of that permission as long
as the player stays within 6 blocks. Asking on every tick would fire the listeners
every time, so this change leaves it.

Forge only, in `//? if forge` blocks. Fabric and NeoForge are not changed; they may
need the same check.

Tested: build of `:1.20.1-forge`. Not tested in game yet.
