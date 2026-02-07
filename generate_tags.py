import re
from collections import defaultdict

SOURCE_FILE = "./images.html"

with open(SOURCE_FILE, "r", encoding="utf-8") as f:
    html = f.read()

# extract article blocks
articles = re.findall(
    r'(<article class="image-entry">.*?</article>)',
    html,
    flags=re.DOTALL
)

tag_map = defaultdict(list)

for article in articles:
    tags = re.findall(r'/cooper-undefined/tags/([a-z0-9_-]+)\.html', article)
    for tag in tags:
        tag_map[tag].append(article)

# shared head + header
head = re.search(r'(<head>.*?</head>)', html, re.DOTALL).group(1)
header = re.search(r'(<header>.*?</header>)', html, re.DOTALL).group(1)

def rewrite_image_paths(article_html):
    return re.sub(
        r'(src=")images/',
        r'\1/cooper-undefined/images/',
        article_html
    )

# clean + normalize head
# head = re.sub(r'<style>.*?</style>', '', head, flags=re.DOTALL)


# -------------------------
# generate individual tag pages
# -------------------------
for tag, entries in tag_map.items():
    rewritten_entries = [
        rewrite_image_paths(article) for article in entries
    ]

    tag_head = re.sub(
        r'<title>.*?</title>',
        f'<title>{tag.title()}</title>',
        head,
        flags=re.DOTALL
    )

    with open(f"./tags/{tag}.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
{tag_head}
<body class="page-tags">
{header}

<main>
  <p><a href="/cooper-undefined/tags.html">← All tags</a></p>
  <h1>{tag.title()}</h1>

  {''.join(rewritten_entries)}

</main>
</body>
</html>
""")

# -------------------------
# generate tags index page
# -------------------------
tags_head = re.sub(
    r'<title>.*?</title>',
    '<title>Tags</title>',
    head,
    flags=re.DOTALL
)

tag_links = "\n".join(
    f'      <li><a href="/cooper-undefined/tags/{tag}.html">{tag}</a></li>'
    for tag in sorted(tag_map.keys())
)

with open("./tags.html", "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html lang="en">
{tags_head}
<body class="page-tags">
{header}

<main>
  <h1>Tags</h1>

  <ul>
{tag_links}
  </ul>
</main>
</body>
</html>
""")

print(f"Generated {len(tag_map)} tag pages + tags index.")
