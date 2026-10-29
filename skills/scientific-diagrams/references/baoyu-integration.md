# Adaptation of baoyu-article-illustrator

Source: Jim Liu, `JimLiu/baoyu-skills`, skill version 1.117.4, repository commit
`1567581c26ec29f4216c6e6835415bf30343b0e3` (inspected 2026-10-29).
See `THIRD_PARTY_NOTICES.md` and `upstream.json` for license and source hashes.

## Architecture inspected

The entrypoint selects content Type × Style × optional Palette, discovers runtime
raster backends, and links to a detailed workflow. Supporting resources separate
style presets/gallery, individual styles, palettes, prompt-construction templates,
preferences/first-time setup, usage, a system prompt, and Codex rendering guidance.
Preferences live in project/XDG/home `EXTEND.md`; project wins. The workflow checks
preferences/references, analyzes the article, confirms settings, saves an outline,
saves structured prompts before rendering, generates images, then inserts them.
Reference usage is classified as direct, style, or palette. Revisions update
prompts and preserve flawed candidates. Current upstream explicitly forbids
substituting SVG/code for the raster backend and defaults to confirmation before
generation. Those rules govern the original raster skill.

## Integration boundary

This skill independently adapts the **planning and revision** structure under MIT.
It does not invoke upstream to produce scientific vectors, impersonate its backend,
or require the upstream installation. A user who invokes upstream for raster work
still gets upstream behavior. Here, a saved figure brief + source + toy data replace
the raster prompt contract, and editable SVG replaces the bitmap deliverable.

| Upstream idea | Scientific adaptation |
| --- | --- |
| Analyze article and choose positions | Identify explanatory need and manuscript anchor, or freeze existing content for polish |
| Type × Style × Palette | Information structure × restrained visual grammar × stable entity colors |
| Saved outline and prompts | Saved outline/brief, source, data, and evidence manifest |
| Reference classification | Distinguish content evidence from style/palette inspiration |
| Image generation and insertion | Deterministic vector render, visual/semantic checks, authorized manuscript integration |
| Prompt-driven revisions | Source-driven revisions; preserve before/after review |

If the user explicitly requests interoperability with existing preferences, read
their provided/project `EXTEND.md` and reuse compatible language, colors, and style
intent. Do not automatically copy its watermark, hand lettering, aspect ratio,
image backend, or density into publication figures. Missing preferences are not a
setup blocker here. Conflicting request-level choices win.

No upstream executable code or full style catalog is vendored. The adaptation
keeps attribution and the original MIT text. Updating upstream is an explicit
maintenance task: inspect the new revision, update source hashes/architecture
notes, and recheck this boundary; do not fetch upstream on every figure run.
