const icons = require('./icons.json')
const shortNames = require('./short-names.json')
const iconNameList = Array.from(new Set(Object.keys(icons).map(i => i.split('.')[0])))
const themedIcons = Array.from(new Set(Object.keys(icons).filter(i => i.includes('.')).map(i => i.split('.')[0])))

const ICONS_COLS = 15
const ICON_SIZE = 300
const PADDING = 44
const SCALE = 48 / (ICON_SIZE - PADDING)

function generateSvg(iconNames, cols) {
    const iconSvgList = iconNames.map(i => icons[i])
    const length = Math.min(cols * ICON_SIZE, iconNames.length * ICON_SIZE) - PADDING
    const height = Math.ceil(iconSvgList.length / cols) * ICON_SIZE - PADDING
    const scaledHeight = height * SCALE
    const scaledWidth = length * SCALE
    return `
<svg width="${scaledWidth}" height="${scaledHeight}" viewBox="0 0 ${length} ${height}" xmlns="http://www.w3.org/2000/svg" version="1.1">
${iconSvgList.map((icon, index) => `<g transform="translate(${(index % cols) * ICON_SIZE}, ${Math.floor(index / cols) * ICON_SIZE})">${icon}</g>`)}
</svg>
  `
}

function parseShortNames(names, theme = 'dark') {
    return names.map(name => {
        if (iconNameList.includes(name)) {
            return name + (themedIcons.includes(name) ? `.${theme}` : '')
        } else if (Object.keys(shortNames).includes(name)) {
            return shortNames[name] + (themedIcons.includes(shortNames[name]) ? `.${theme}` : '')
        }
    })
}

async function handleRequest(request) {
    const { pathname, searchParams } = new URL(request.url)
    if (pathname === '/') {
        const iconParam = searchParams.get('i') || searchParams.get('icons')
        if (!iconParam) {
            return new Response("You didn't specify any icons!", { status: 400 })
        }
        const iconShortNames = 'all' === iconParam ? iconNameList : iconParam.split(',')
        const theme = searchParams.get('t') || searchParams.get('theme')
        if (theme && theme !== 'dark' && theme !== 'light') {
            return new Response('Theme must be either "light" or "dark"', { status: 400 })
        }
        const iconNames = parseShortNames(iconShortNames, theme || undefined)
        if (!iconNames) {
            return new Response()
        }
        const cols = searchParams.get('c') || searchParams.get('cols') || ICONS_COLS
        const svg = generateSvg(iconNames, cols)
        return new Response(svg, { headers: { 'Content-Type': 'image/svg+xml' } })
    } else {
        return new Response("", { status: 404 })
    }
}

addEventListener('fetch', event => {
    event.respondWith(
        handleRequest(event.request).catch(err => new Response(err.stack, { status: 500 }))
    )
})
