import os
import math
from pathlib import Path
from fastapi import FastAPI, Response

# default svg params
ICONS_COLS = 16
GAP = 48
ICON_SIZE = 256 + GAP
PADDING = 0
SCALE = 48 / 256

# svg files
FILES = os.listdir('./icons')
ICON_NAMES = {file.replace('.svg', '') for file in FILES}
ICONS = {file.replace('.svg', '').lower(): Path(f'./icons/{file}').read_text() for file in FILES}


def generate_svg(icon_names, cols, iconBgColor):
    svgs = [ICONS[x.lower()] for x in icon_names]
    width = min(cols * ICON_SIZE, len(icon_names) * ICON_SIZE) + PADDING - GAP
    height = math.ceil(len(icon_names) / cols) * ICON_SIZE + PADDING - GAP
    icon_bg_rect = f'<rect xmlns="http://www.w3.org/2000/svg" width="256" height="256" rx="56" fill="#{iconBgColor}"/>' if iconBgColor else ''
    return f"""
    <svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" version="1.1">
    <g transform="scale({SCALE})">
    {''.join([f'<g transform="translate({(index % cols) * ICON_SIZE + PADDING}, {math.floor(index / cols) * ICON_SIZE + PADDING})">{icon_bg_rect}{icon}</g>' for index, icon in enumerate(svgs)])}
    </g>
    </svg>
    """.strip()

app = FastAPI()

@app.get("/")
async def svg(icons: str = '', cols: int = 16, iconBgColor: str = None):
    """Merge icons to a svg

    Args:
        icons (str): icons name
        theme (str, optional): icons theme. Defaults to 'dark'.
        cols (int, optional): how many icons per line. Defaults to 16.

    Returns:
        _type_: svg file
    """
    icon_names = ICON_NAMES if not icons else icons.split(',')
    icon_names = list(filter(lambda x: x in [x.lower() for x in ICON_NAMES], [x.lower() for x in icon_names]))
    if not icon_names:
        return Response('', status_code=404)
    svg = generate_svg(icon_names, cols, iconBgColor)
    return Response(svg, media_type='image/svg+xml')


@app.get("/api/icons")
async def all():
    """List all icons

    Returns:
        _type_: icons dict
    """
    # files = [file for file in FILES]
    # native_icons = [{'name': file.replace('.svg', ''), 'themed': False} for file in list(filter(lambda x: len(x.split('.')) == 2, files))]
    # themed_icons_name = {file.split('.')[0] for file in list(filter(lambda x: len(x.split('.')) == 3, files))}
    # themed_icons = [{'name': name, 'themed': True} for name in themed_icons_name]
    return sorted(ICON_NAMES)
