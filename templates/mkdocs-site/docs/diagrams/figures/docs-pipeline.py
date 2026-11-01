"""How a page reaches the site: pages and code go in, checks run, MkDocs builds, mike publishes.

Reads: From left to right. Pages under docs/ and the code they describe are the inputs. Two generators turn code
into documentation: figkit draws the figures and gen.py fills the generated tables, and both run with --check in CI
so a committed figure or table that no longer matches the code fails the pull request. MkDocs builds the site in
strict mode, Doxygen builds the API reference, the two are merged and the link checker runs on the result. On a push
to main or a version tag, mike publishes the merged site to the gh-pages branch under a version folder.
"""

from figkit import Fig

SOURCES = [
    "mkdocs.yml",
    "tools/figkit/build.py",
    "tools/docs/gen.py",
    "tools/docs/mkdocs_hooks.py",
]


def build(_data):
    f = Fig(
        "docs-pipeline",
        "From code to site",
        alt="Pages and code feed figkit and the table generator, MkDocs builds the site in strict mode, the Doxygen "
        "API is merged in, links are checked and mike publishes to gh-pages.",
        width=1200,
        kicker="Documentation pipeline",
        subtitle="Everything a reader sees is either written once or generated from the code, and CI checks both.",
        profile="overview",
        legend=[("blue", "input"), ("violet", "generator, checked in CI"), ("brand", "build"), ("green", "publish")],
    )
    w, col = 230, 300
    pages = f.card(0, 0, w, "Pages", ["docs/**/*.md"], tone="blue", mono=True)
    code = f.card(0, pages.b + 40, w, "Code", ["headers, tables, YAML"], tone="blue")
    fk = f.card(col, code.y - 46, w, "figkit", ["figures from code"], tone="violet")
    gen = f.card(col, fk.b + 20, w, "gen.py", ["tables from code"], tone="violet")
    mk = f.card(2 * col, 0, w, "MkDocs", ["build --strict"], tone="brand", accent=True)
    dox = f.card(2 * col, gen.y, w, "Doxygen", ["API under api/"], tone="brand")
    pub = f.card(3 * col, mk.y + 70, f.body_w - 3 * col, "mike", ["gh-pages, one folder per version"],
                 tone="green", accent=True)
    f.connect(pages, mk, "right", "left", bt=(pages.cy - mk.y) / mk.h, tone="blue")
    f.connect(code, fk, "right", "left", tone="blue")
    f.connect(code, gen, "right", "left", tone="blue")
    f.connect(fk, mk, "right", "left", bt=0.65, tone="violet")
    f.connect(gen, mk, "right", "left", bt=0.9, tone="violet")
    f.connect(mk, pub, "right", "left", bt=0.3, tone="brand")
    f.connect(dox, pub, "right", "left", bt=0.75, tone="brand")
    f.edge_label(pub.cx, pub.b + 30, "merged, then links checked")
    return f
