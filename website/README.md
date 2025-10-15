# Casa Vazquez Website

Vue 3 + TypeScript + Vite single-page app for Casa Vazquez (Weinbar & Cocktails in Münster).

## Requirements

- Node.js 18/20/22 LTS recommended (Vite 6 requires >= 18)
- npm 9+

## Getting started

1. Install dependencies
	- `npm ci` (preferred if lockfile present) or `npm i`
2. Start dev server
	- `npm run dev`
3. Type-check + build
	- `npm run build`
4. Preview production build
	- `npm run preview`

## Project structure

- `src/` application code
  - `views/` pages (LandingPage, WineMenu, DrinkMenu, SnackMenu, Showroom, WineTasting, Legals)
  - `components/` shared UI (NavigationBar, BaseModal, etc.)
  - `data/` menu data (blancos, tintos, rosados, notifications, vinos)
  - `assets/` images, styles (SCSS), fonts
  - `router/` Vue Router config (base `/casavazquez/`)

## Notable features

- Wine Tasting page with stories and a Leaflet/OpenStreetMap map showing wine regions
- Hidden admin tool (`/admin/flyer-sectors`) with Leaflet-based flyer distribution sectors (unlock via triple-click on the Impressum heading)
- Top toasts/announcements on menu pages
- Image assets bundled via Vite; local bottles in `src/assets/images/tinified (6)`
- Router scroll behavior resets to top on navigation

## Environment & Build

- Vite base is set to `/casavazquez/` in `vite.config.ts` for correct asset paths on GitHub Pages or similar
- Strict TypeScript settings via `@vue/tsconfig`
- Hidden route remains off the public navigation; trigger it by triple-clicking “Impressum” on the landing page.

## Scripts

- `dev`       start the development server
- `build`     type-check and build production bundle
- `preview`   preview the build locally
- `deploy`    deploy `dist/` via gh-pages (configure repository beforehand)

## Deployment tips

- Ensure repository settings allow deploying to GitHub Pages from the `gh-pages` branch
- Verify `base` in `vite.config.ts` matches your publish path

## Legal notice (DE)

- Impressum & Datenschutz: available under `/legals` and via the “Info” link in the bottom navigation
- Jugendschutz: kein Ausschank/Verkauf alkoholischer Getränke an U18
- Icons: © icons8.com (see footer attribution)

## Troubleshooting

- Marker icons on maps: handled via Vite `?url` imports and custom divIcon
- If images don’t appear, confirm the path casing and that assets reside under `src/assets`
- For Node engine warnings, use Node 18/20/22 LTS

## License

Proprietary — for internal use by Casa Vazquez. Icons per their respective licenses.
