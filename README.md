# Kudzaiishe Muza — Portfolio

Static single-page portfolio converted to a proper website structure.

Structure:

- `index.html` — entry point (now links to external CSS/JS)
- `css/styles.css` — extracted styles
- `js/script.js` — extracted JavaScript (animations + form handler)
- `images/` — image assets (unchanged)

How to preview:

Open `index.html` in your browser, or serve the folder with a static server:

```powershell
# from project root
npx serve .
```

Next suggestions: add meta tags, optimise images, or wire contact form to a backend.

## Deploying to Vercel

This project is ready to deploy as a static site on Vercel. I added a `vercel.json` config to ensure the site serves `index.html` for all routes.

Two quick ways to deploy:

- Using the Vercel dashboard (recommended):

	1. Push this repository to GitHub, GitLab, or Bitbucket.
	2. Sign in to https://vercel.com and import the repository.
	3. Vercel will auto-detect the static project and deploy.

- Using the Vercel CLI:

```powershell
# install the CLI if you don't have it
npm install -g vercel

# login (opens browser)
vercel login

# deploy from project root
vercel

# preview locally
vercel dev
```

Notes:
- `vercel.json` sets a static build and routes all requests to `index.html` (SPA-friendly).
- If you prefer a build step, switch the `builds` config to `@vercel/static-build` and add a `build` script in `package.json` that outputs to a `public/` folder.
