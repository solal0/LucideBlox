# LucideBlox

A revival of [frappedevs/lucideblox](https://github.com/frappedevs/lucideblox), using my own [I2B64](https://github.com/solal0/I2B64) image-to-Lua conversion tool to bring Lucide icons to Roblox.

Instead of storing every icon in a separate Lua file, LucideBlox provides a single Lua file containing the icon library and its helper functions. Load it once, then retrieve icons by name.

## Features

- The Lucide icon library, converted into Roblox-compatible image content.
- A single Lua file containing the icons and library functions.
- Retrieve individual icons by their Lucide name.
- Transparent backgrounds and recolorable white icons.
- No need to upload each icon as a Roblox asset.

## Usage

```lua
-- studio
local LucideBlox = require(game.ReplicatedStorage.LucideBlox)
local image = LucideBlox.GetImage("settings")

-- other
local LucideBlox = loadstring(game:HttpGet("https://github.com/solal0/LucideBlox/releases/latest/download/LucideBlox.lua"))()
local image = LucideBlox.GetImage("settings")
```

Use the icon's Lucide name in kebab-case. Browse the [Lucide icon library](https://lucide.dev/icons/) to find icon names.

`GetImage` returns Roblox `Content` suitable for `ImageLabel.ImageContent` or `ImageButton.ImageContent`.

The example requires a Luau environment supporting `loadstring`, `game:HttpGet` and `EditableImage`.

## Updates

I intend to keep LucideBlox as close to the upstream Lucide project as possible, publishing updates for new Lucide releases rather than maintaining only one fixed version. Update frequency depends on upstream releases and the time needed to convert and publish each version.

## Credits

- [frappedevs/lucideblox](https://github.com/frappedevs/lucideblox) — original project and inspiration.
- [lucide-icons/lucide](https://github.com/lucide-icons/lucide) — original icon library.
- [solal0/I2B64](https://github.com/solal0/I2B64) — image-to-Lua conversion tool.
- [solal0/Luau](https://github.com/solal0/Luau) — image conversion utilities.

## License

Lucide's icons are distributed under their respective upstream licenses. See the [Lucide license information](https://lucide.dev/license).
