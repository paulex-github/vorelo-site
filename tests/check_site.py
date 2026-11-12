"""Offline checks for the public static website. Standard library only."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / "docs"
ALLOWED = {".nojekyll", "index.html", "guide.html", "privacy.html", "assets/style.css", "assets/mark.svg"}


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.links, self.ids = path, [], set()
        self.lang = self.title = self.main = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        assert tag not in {"script", "iframe", "form"}, f"Unexpected active content: {self.path}"
        assert not any(key.startswith("on") for key in attrs), f"Inline script: {self.path}"
        if "id" in attrs:
            assert attrs["id"] not in self.ids, f"Duplicate id in {self.path}"
            self.ids.add(attrs["id"])
        self.lang |= tag == "html" and attrs.get("lang") == "en"
        self.title |= tag == "title"
        self.main |= tag == "main"
        if tag == "img":
            assert "alt" in attrs, f"Image missing alt in {self.path}"
        for key in ("href", "src"):
            if key in attrs:
                self.links.append(attrs[key])


actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file()}
assert actual == ALLOWED, f"Public file allowlist mismatch: {actual ^ ALLOWED}"
assert not any(p.is_symlink() for p in ROOT.rglob("*")), "Symlinks are not allowed"
pages = {}
for path in ROOT.glob("*.html"):
    page = Page(path)
    page.feed(path.read_text(encoding="utf-8"))
    assert page.lang and page.title and page.main, f"Missing page landmarks in {path}"
    pages[path.resolve()] = page
for path, page in pages.items():
    for link in page.links:
        parsed = urlsplit(link)
        if parsed.scheme:
            assert parsed.scheme == "https", f"Unexpected scheme: {link}"
            assert parsed.hostname in {"paulex-github.github.io", "github.com", "wordpress.org", "docs.github.com"}, f"Unexpected external host: {link}"
            continue
        assert not parsed.netloc and not parsed.path.startswith("/"), f"Non-relative link: {link}"
        target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
        if target.is_dir():
            target = target / "index.html"
        assert target.is_relative_to(ROOT.resolve()) and target.is_file(), f"Missing/unsafe local link: {link}"
        if parsed.fragment:
            assert target in pages and unquote(parsed.fragment) in pages[target].ids, f"Missing anchor: {link}"
print(f"PASS: {len(pages)} HTML pages, local links/anchors, public file allowlist, no active content")
