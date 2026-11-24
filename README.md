# LucideBlox

A revival of [frappedevs/lucideblox](https://github.com/frappedevs/lucideblox), powered by my own image-to-Lua conversion tool, [I2B64](https://github.com/solal0/I2B64).

LucideBlox brings the entire [Lucide](https://lucide.dev/) icon library to Roblox without relying on uploaded Roblox image assets. Each icon is individually stored as a Base64-encoded Lua file and can be loaded on demand using `EditableImage`.

## Features

- Access to the entire Lucide icon library.
- 64×64 resolution with transparent backgrounds.
- Recolorable through `ImageColor3`.
- Individual icon loading without downloading the entire library.
- No dependency on Roblox asset IDs.

## Usage

```lua
local Utils = loadstring(game:HttpGet("https://raw.githubusercontent.com/solal0/Luau/refs/heads/main/Tools/Utils.luau"))()

local function GetIcon(Name)
    return Utils.toImage(loadstring(game:HttpGet("https://raw.githubusercontent.com/solal0/LucideBlox/refs/heads/main/lua/"..Name..".lua"))()).Image
end

ImageLabel.ImageContent = GetIcon("settings")
```

Browse the [Lucide icon library](https://lucide.dev/icons/) to find available icon names.

Requires an environment supporting `loadstring`, `game:HttpGet` and `EditableImage`.

## Updates

LucideBlox aims to stay up to date with Lucide's official releases. I will try to publish an update for every new version of Lucide, keeping the collection synchronized with upstream additions and changes.

## Credits

- [frappedevs/lucideblox](https://github.com/frappedevs/lucideblox) — Original project and inspiration.
- [lucide-icons/lucide](https://github.com/lucide-icons/lucide) — Original icon library.
- [solal0/I2B64](https://github.com/solal0/I2B64) — Image encoding and decoding tool used by this project.

## License

All icons belong to their respective creators and are distributed under the original [Lucide license](https://lucide.dev/license).
