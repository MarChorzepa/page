# step-zero-context.md

**Date:** 2025-06-16
**Project:** Moje Przestrzenie — personal web page

## Project Overview
Fresh standalone personal website for private creative endeavors: writings, vibecoded projects, notes, memes, and random content. Deployable to any static host (GitHub Pages, Netlify, etc.).

## Tech Stack
- **Approach:** Static site generator with Python + Jinja2 templating
- **Template:** One `templates/base.html` with shared nav, footer, and layout
- **Content:** Folder-based (`content/teksty/`, `content/notatki/`, `content/galeria/`, `content/memy/`, `content/losowe/`)
- **Build script:** `build.py` — rebuilds all pages when content changes
- **Output:** Plain HTML/CSS/JS — no build step required for viewers
- **Font:** Inter (OFL, fully supports Polish characters)

## Pages
- `index.html` — Landing / main page
- `galeria.html` — Gallery (first 20 images from ładnie)
- `teksty.html` — Text listing page (auto-generates links to individual text posts)
- `tekst-*.html` — Individual text posts (unique URLs)
- `notatki.html` — Notes listing
- `memy.html` — Memes listing
- `losowe.html` — Empty placeholder for future expansion

## Features

### 1. Background Images
- Randomly tiled background from ładnie photos on every page load
- Multiple images tiled simultaneously (low-opacity collage)
- Images compressed for web (~300KB–500KB each, 53 total)
- Base peach overlay: `#FFF5E6`
- Opacity: 20% (adjustable in testing)

### 2. Navigation
- Top bar that floats over content
- Toggleable anchor button (anchored by default, user can unpin)
- Sections: **Galeria**, **Teksty**, **Notatki**, **Memy**, **Losowe**
- No current-page highlight
- No dropdowns/submenus
- Mobile hamburger menu

### 3. Color Palette
| Role | Hex |
|---|---|
| Background peach | `#FFF5E6` |
| Text primary | `#3D2B1F` |
| Text secondary | `#7A6B5F` |
| Primary green accent | `#6FAF3A` |
| Light green | `#C5E1A5` |
| Nav bar background | `#FFF8F0` |
| Nav border | `#E8DFD4` |
| Link color | `#558B2F` |
| Link hover | `#8BC34A` |
| Warm highlight | `#FFE0B2` |

### 4. MLG Easter Egg
- Universal click anywhere on page (except links/buttons)
- AWP shooting sound effect generated via Web Audio API (short burst, no external dependencies)
- Red crossmark appears at exact click location
- Designed as a fun callback, not annoying

### 5. Scalability
- Future: 50+ text posts, each with unique URL
- Auto-generate listing page for new content
- One template change updates all pages via `build.py`

## How to Add Content
1. Add text files to `content/teksty/` or `content/notatki/` (`.html` or `.md`)
2. Run `python build.py` to regenerate all pages
3. New posts automatically appear on listing pages with their own URLs

## How to Add Images
1. Add new photos to `images/` folder
2. Run `python build.py` to regenerate pages
3. Background and gallery will automatically include new images

## Acceptance Criteria
- All pages generated and working in browser
- Background changes randomly on every navigation
- MLG click effect functional (sound + crossmark)
- Polish characters render correctly (Inter font)
- Responsive design (works on mobile/desktop)
- Build script runs successfully
