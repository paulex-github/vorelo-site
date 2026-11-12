# Vorelo — public website and documentation

An independent, static documentation site for **Vorelo — Two-Way Job Board**,
a free WordPress plugin available on
[WordPress.org](https://wordpress.org/plugins/vorelo-job-board/).

This repository contains public-facing website content only. It does not contain
the plugin source, premium modules, internal documents, credentials or user data.

## GitHub Pages setup

In this repository, open **Settings → Pages → Build and deployment**:

1. Source: **Deploy from a branch**.
2. Branch: **main**.
3. Folder: **/docs**.
4. Save and check the Pages deployment result.

Expected address after successful deployment:
<https://paulex-github.github.io/vorelo-site/>.
This README is not evidence that Pages is enabled or that deployment succeeded.
No custom domain is configured.

## Editing and checking

- Published files live in `docs/`; all assets and navigation use relative paths.
- Plain HTML and CSS; no framework, JavaScript, package installation or build.
- Run `python3 -B tests/check_site.py` to check local links and the public file allowlist.
- Preview with `python3 -m http.server 8000 --bind 127.0.0.1 --directory docs`.
- Changes pushed to `main` publish after Pages has been enabled.

## Brand assets

The header logo and favicon are unmodified copies of the plugin's published
WordPress.org icons (256px and 128px respectively), verified on 12 November 2026.
The offline checks verify their SHA-256 hashes and their use on all pages.
Do not introduce a separate logo for the documentation website.

Only document features present in the WordPress.org edition. Do not publish
roadmap promises, customer names, screenshots with private data, internal security
reports or sales/checkout functionality here. No analytics, forms or remote fonts
are included. See the public privacy note for GitHub hosting information.

Support and feedback: <https://wordpress.org/support/plugin/vorelo-job-board/>.
Never post passwords, CVs or private candidate/employer information in public reports.
