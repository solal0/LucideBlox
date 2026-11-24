# LucideBlox

LucideBlox is a collection of [Lucide](https://lucide.dev/) icons converted into Roblox-compatible images using [I2B64](https://github.com/solal0/I2B64).

Each icon is stored as a Base64-encoded Lua file and can be loaded directly into an `ImageLabel` or `ImageButton` without uploading image assets to Roblox.

## Features

- 2,104 icons from Lucide v1.79.0
- 64×64 resolution with transparent backgrounds
- White icons that can be recolored using `ImageColor3`
- Load individual icons on demand

## Usage

```lua
local Utils = loadstring(game:HttpGet("https://raw.githubusercontent.com/solal0/Luau/refs/heads/main/Tools/Utils.luau"))()

local function GetIcon(Name)
    return Utils.toImage(loadstring(game:HttpGet("https://raw.githubusercontent.com/solal0/LucideBlox/refs/heads/main/lua/"..Name..".lua"))()).Image
end

ImageLabel.ImageContent = GetIcon("settings")
```

Use the original icon name in kebab-case, without the `.lua` extension. Browse the [Lucide icon library](https://lucide.dev/icons/) to find icon names.

The example requires a Luau environment supporting `loadstring`, `game:HttpGet` and `EditableImage`.

## Credits

- [Lucide](https://github.com/lucide-icons/lucide) — original icons.
- [I2B64](https://github.com/solal0/I2B64) — image encoding and decoding.

The original icons are distributed under the [Lucide license](https://lucide.dev/license) (ISC, with Feather-derived icons under MIT).
