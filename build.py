"""Tiny Markdown-to-HTML builder (headings, lists, code blocks, paragraphs). Standard library only."""
import html
import pathlib
import sys


def md_to_html(text: str) -> str:
    out, para, items, in_code = [], [], [], False

    def flush_para():
        if para:
            out.append("<p>" + html.escape(" ".join(para)) + "</p>")
            para.clear()

    def flush_list():
        if items:
            out.append("<ul>" + "".join(f"<li>{html.escape(i)}</li>" for i in items) + "</ul>")
            items.clear()

    for line in text.splitlines():
        if line.startswith("```"):
            flush_para(); flush_list()
            out.append("</pre>" if in_code else "<pre>")
            in_code = not in_code
        elif in_code:
            out.append(html.escape(line))
        elif line.startswith("## "):
            flush_para(); flush_list(); out.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("# "):
            flush_para(); flush_list(); out.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("- "):
            flush_para(); items.append(line[2:])
        elif not line.strip():
            flush_para(); flush_list()
        else:
            flush_list(); para.append(line.strip())
    flush_para(); flush_list()
    return "\n".join(out)


def build(src="docs", dest="site"):
    pathlib.Path(dest).mkdir(exist_ok=True)
    names = []
    for md in sorted(pathlib.Path(src).glob("*.md")):
        name = md.stem
        names.append(name)
        body = md_to_html(md.read_text(encoding="utf-8"))
        page = f"<!doctype html><meta charset=utf-8><title>{name}</title><body>{body}"
        (pathlib.Path(dest) / f"{name}.html").write_text(page, encoding="utf-8")
    index = "".join(f'<li><a href="{n}.html">{n}</a></li>' for n in names)
    (pathlib.Path(dest) / "index.html").write_text(
        f"<!doctype html><meta charset=utf-8><title>docs</title><h1>Docs</h1><ul>{index}</ul>", encoding="utf-8")
    return names


if __name__ == "__main__":
    print("built:", build(*sys.argv[1:3]))
