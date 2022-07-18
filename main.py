import os
import math
from pathlib import Path
from fastapi import FastAPI, Response

ICONS_COLS = 15
ICON_SIZE = 300
PADDING = 44
SCALE = 48 / (ICON_SIZE - PADDING)
ICONS = { file.replace('Icon=', '').replace(', Mode=', '.').replace('.svg', '').lower(): Path(f'./icons/{file}').read_text() for file in os.listdir('./icons')}
ICON_NAMES = {x.split('.')[0] for x in ICONS.keys() }
THEMED_ICON_NAMES = {x.split('.')[0] for x in list(filter(lambda x: '.' in x, ICONS.keys()))}

def generate_svg(icon_names, cols):
    svgs = [ICONS[x] for x in icon_names]
    length = min(cols * ICON_SIZE, len(icon_names) * ICON_SIZE) - PADDING
    height = math.ceil(len(icon_names) / cols) * ICON_SIZE - PADDING
    scaledHeight = height * SCALE
    scaledWidth = length * SCALE
    return f"""
    <svg width="{scaledWidth}" height="{scaledHeight}" viewBox="0 0 {length} {height}" xmlns="http://www.w3.org/2000/svg" version="1.1">
    {''.join([f'<g transform="translate({(index % cols) * ICON_SIZE}, {math.floor(index / cols) * ICON_SIZE})">{icon}</g>' for index, icon in enumerate(svgs)])}
    </svg>
    """

themed_name = lambda name, theme: f'{name}.{theme}' if name in THEMED_ICON_NAMES else name

app = FastAPI()

@app.get("/")
async def icons(icons: str, theme: str = 'dark', cols: int = 15):
    icon_names = ICON_NAMES if 'all' == icons else icons.split(',')
    if theme not in ['dark', 'light']:
        return 'Theme must be either "light" or "dark"', 400
    icon_names = list(filter(lambda x: x in ICON_NAMES, icon_names))
    icon_names = [themed_name(x, theme) for x in icon_names]
    if not icon_names:
        return ''
    svg = generate_svg(icon_names, cols)
    return Response(svg, media_type='image/svg+xml')
