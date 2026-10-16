# gha-pages-docs-deploy

Markdown in `docs/` is turned into a small static site by `build.py`, tested, and deployed to **GitHub Pages** by a workflow. No branch holds generated files; the workflow publishes an artifact.

**Live site:** https://sup3rmar10.github.io/gha-pages-docs-deploy/

## Flow

```
unit tests -> build.py (docs/*.md -> site/*.html) -> upload Pages artifact -> deploy (not on pull requests)
```

## What ran (2026-10-16)

- Pages was switched to "build from a workflow" with `gh api -X POST repos/OWNER/REPO/pages -f build_type=workflow` **before the first push** (otherwise the deploy step has nowhere to go).
- The run succeeded, and the site returned **HTTP 200** with the built content (`intro.html` contains the rendered heading and list).
- The 4 unit tests (headings, HTML escaping, lists, code blocks) ran in CI before the build.

## Decisions

- **`deploy` has its own permissions** (`pages: write`, `id-token: write`); the build job needs only `contents: read`.
- **`concurrency` with `cancel-in-progress: false`:** a deployment is never cancelled half way.
- **`github-pages` environment** gives a deployment history and can carry protection rules.
- **The converter escapes all text.** A Markdown file must not be able to inject script into the site (there is a test for it).
- **`if: github.event_name != 'pull_request'`:** a pull request builds and tests but never deploys.

## Honest limits

- The pull-request path (build without deploy) was written but **not exercised**.
- `build.py` is a toy: no links, bold, tables or images. A real site uses a generator such as MkDocs or Hugo.
- No custom domain, no link checker, no preview environment for pull requests.
- Public Pages sites are public even when the source is private on some plans; check before publishing internal docs.

MIT licensed.
