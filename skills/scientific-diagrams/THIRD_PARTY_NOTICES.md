# Third-party notices

This skill adapts workflow concepts and organization from **baoyu-article-illustrator**,
by Jim Liu, in JimLiu/baoyu-skills, licensed under the MIT License.

- Repository: https://github.com/JimLiu/baoyu-skills
- Inspected commit: `1567581c26ec29f4216c6e6835415bf30343b0e3`
- Skill version in that revision: `1.117.4`
- Source subtree: `skills/baoyu-article-illustrator/`
- Copyright (c) 2026 Jim Liu
- The original permission and warranty text is preserved verbatim in `LICENSE.baoyu`.

Adapted ideas: article/figure placement analysis, Type × Style × Palette separation,
saved outline/rendering instructions, reference classification, and revision records.
The instructions were rewritten for scientific-diagram polishing and deterministic
vectors. No upstream runtime, generated images, full prompt templates, or style
catalog is bundled. This work is not endorsed by the upstream author. The original
skill retains its raster-only workflow; this is a separate adaptation.

The helper code and synthetic worked examples are original contributions under MIT.
No private manuscript drawing code, prose, data, screenshots, or figure assets are
included. The case-study requirements are summarized from author-provided local
materials; filenames and hashes provide evidence without distributing those files.
Their rights are not relicensed by this repository. Source links in the case-study
provenance describe implementation evidence, not dependencies or copied code.

Matplotlib and Pillow are runtime dependencies, not vendored source. Matplotlib's
bundled DejaVu fonts are selected from the installed package; no font files are
included in skill.zip. Dependencies retain their own licenses. Any exported PDF
embeds the installed font subsets; preserve font licensing if redistributing fonts
separately. The package does not add a watermark or upstream branding to figures.
