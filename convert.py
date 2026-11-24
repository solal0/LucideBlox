
import base64
import struct
from itertools import groupby
from io import BytesIO
from pathlib import Path

import resvg_py
from PIL import Image

SIZE = 64
COLOR = "#FFFFFF"

ROOT = Path(__file__).resolve().parent
ICONS = ROOT / "icons"
OUTPUT = ROOT / "LucideBlox.lua"

def encode(image):
    image = image.convert("RGBA")
    width,height = image.size
    palette = {}
    indices = []
    for pixel in image.getdata():
        rgba = tuple(round(v*99/255) for v in pixel)
        indices.append(palette.setdefault(rgba,len(palette)))
    data = bytearray(struct.pack(">HHH",width,height,len(palette)))
    for rgba in palette:
        data.extend(rgba)
    for index,group in groupby(indices):
        count = sum(1 for _ in group)
        while count:
            run = min(count,65535)
            data.extend(struct.pack(">HH",run,index))
            count -= run
    return base64.b64encode(data).decode("ascii")

def render_svg(path):
    svg = path.read_text(encoding="utf-8").replace("currentColor",COLOR)
    png = resvg_py.svg_to_bytes(svg_string=svg,width=SIZE,height=SIZE)
    with Image.open(BytesIO(png)) as image:
        image = image.convert("RGBA")
        if image.getchannel("A").getbbox() is None:
            raise ValueError(f"Empty SVG rendering: {path.name}")
        return encode(image)

def main():
    if not 1 <= SIZE <= 1024:
        raise ValueError("SIZE must be between 1 and 1024.")
    icons = sorted(ICONS.glob("*.svg"))
    if not icons:
        raise FileNotFoundError(f"No SVG icons found in {ICONS}")

    entries = []
    for i,path in enumerate(icons,1):
        entries.append(f'    ["{path.stem}"] = "{render_svg(path)}"')
        if i % 100 == 0 or i == len(icons):
            print(f"\rConverting: {i}/{len(icons)}",end="",flush=True)

    entries_text = ",\n".join(entries)

    lua = f'''local function decode(data)
    local alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    data = string.gsub(data,"[^"..alphabet.."=]","")
    return (data:gsub(".",function(x)
        if x == "=" then return "" end
        local r,f = "",(alphabet:find(x)-1)
        for i = 6,1,-1 do
            r = r..(f%2^i-f%2^(i-1)>0 and "1" or "0")
        end
        return r
    end):gsub("%d%d%d?%d?%d?%d?%d?%d?",function(x)
        if #x ~= 8 then return "" end
        local c = 0
        for i = 1,8 do
            c = c+(x:sub(i,i) == "1" and 2^(8-i) or 0)
        end
        return string.char(c)
    end))
end

local function toImage(base64)
    local data = decode(base64)
    local pos = 1

    local function u8()
        local v = string.byte(data,pos)
        pos += 1
        return v
    end

    local function u16()
        return u8()*256+u8()
    end

    local width,height = u16(),u16()
    local paletteCount = u16()
    local palette = table.create(paletteCount)

    for i = 1,paletteCount do
        palette[i-1] = {{u8(),u8(),u8(),u8()}}
    end

    local pixelCount = width*height
    local out = buffer.create(pixelCount*4)
    local p = 0

    while pos <= #data-3 and p < pixelCount do
        local count,index = u16(),u16()
        local c = palette[index]
        if not c then error("LucideBlox: invalid palette index") end

        local r = math.floor(c[1]*255/99+0.5)
        local g = math.floor(c[2]*255/99+0.5)
        local b = math.floor(c[3]*255/99+0.5)
        local a = math.floor(c[4]*255/99+0.5)

        for _ = 1,count do
            if p >= pixelCount then break end
            local i = p*4
            buffer.writeu8(out,i,r)
            buffer.writeu8(out,i+1,g)
            buffer.writeu8(out,i+2,b)
            buffer.writeu8(out,i+3,a)
            p += 1
        end
    end

    if p ~= pixelCount then
        error("LucideBlox: incomplete image data")
    end

    local image = game:GetService("AssetService"):CreateEditableImage({{
        Size = Vector2.new(width,height)
    }})
    image:WritePixelsBuffer(Vector2.new(0,0),Vector2.new(width,height),out)

    return {{
        Image = Content.fromObject(image),
        Raw = image,
        X = width,
        Y = height
    }}
end

local Icons = {{
{entries_text}
}}

local Cache = {{}}
local LucideBlox = {{}}

function LucideBlox.GetImageData(name)
    if not Icons[name] then return nil end
    if not Cache[name] then Cache[name] = toImage(Icons[name]) end
    return Cache[name]
end

function LucideBlox.GetImage(name)
    local data = LucideBlox.GetImageData(name)
    return data and data.Image
end

function LucideBlox.GetRawImage(name)
    local data = LucideBlox.GetImageData(name)
    return data and data.Raw
end

function LucideBlox.GetBase64(name)
    return Icons[name]
end

function LucideBlox.HasIcon(name)
    return Icons[name] ~= nil
end

function LucideBlox.GetIconNames()
    local names = {{}}
    for name in pairs(Icons) do
        names[#names+1] = name
    end
    table.sort(names)
    return names
end

function LucideBlox.GetCount()
    local count = 0
    for _ in pairs(Icons) do
        count += 1
    end
    return count
end

return LucideBlox
'''

    OUTPUT.write_text(lua,encoding="utf-8")
    print(f"\nGenerated: {OUTPUT}")
    print(f"Icons: {len(icons)}")
    print(f"Size: {OUTPUT.stat().st_size/1024/1024:.2f} MB")

if __name__ == "__main__":
    main()
