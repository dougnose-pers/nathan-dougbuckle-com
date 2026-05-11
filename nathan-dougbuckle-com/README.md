# nathan.dougbuckle.com

Private index for pieces Doug is sharing with Nathan Pollock (Katapult).

## Pages

- `/` — placeholder index, lists available pages
- `/horizon-press-release/` — six-months-from-now retrospective on the Horizon quarterly intelligence program (Nov 2026 dated)

## Deploy (first time)

Follows the same pattern as `benny.dougbuckle.com`. Use the **personal** accounts on both sides:
- Cloudflare: `doug.buckle@gmail.com`
- GitHub: `dougnose-pers`

### Steps

1. **Create the GitHub repo** (logged into `dougnose-pers`):
   - Repo name: `nathan-dougbuckle-com`
   - Private
   - Don't initialise with a README (this folder already has one)

2. **Push this folder up:**
   ```bash
   cd "nathan-dougbuckle-com"
   git remote add origin https://github.com/dougnose-pers/nathan-dougbuckle-com.git
   git branch -M main
   git push -u origin main
   ```

3. **Connect Cloudflare to the repo** (logged into the gmail Cloudflare account):
   - Workers & Pages → Create → "Import a repository" / "Connect to Git"
   - Select `dougnose-pers/nathan-dougbuckle-com`
   - Project name: `nathan-dougbuckle-com`
   - Framework preset: **None** (static HTML)
   - Build command: (leave blank)
   - Build output directory: `/` (or leave default)
   - Deploy

4. **Wire the custom domain:**
   - Open the new Worker → Domains & Routes → Add → Custom domain
   - Enter: `nathan.dougbuckle.com`
   - Cloudflare auto-creates the CNAME on the `dougbuckle.com` zone (because both Worker and zone are in the same gmail account)
   - SSL provisions in ~1–2 minutes

5. **Verify** `https://nathan.dougbuckle.com` loads the index, and `/horizon-press-release/` loads the Horizon page.

## Adding new pages later

- Make a new folder e.g. `studio-pitch/` with an `index.html` inside it
- Add an entry to the `<ul class="entries">` list in the root `index.html`
- `git add . && git commit -m "Add studio-pitch page" && git push`
- Cloudflare auto-deploys on push to `main`

## Notes

- All pages use Inter + Fragment Mono from Google Fonts (loaded inline). No build step.
- The hero image (`horizon-hero.png`) is the team photo Nathan supplied, sitting next to its HTML page.
- `noindex, nofollow` on the index page — Google won't index this domain.
