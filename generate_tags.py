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
    # images/IMG_*.jpeg -> ../cooper-undefined/images/IMG_*.jpeg
    return re.sub(
        r'(src=")images/',
        r'\1/cooper-undefined/images/',
        article_html
    )

# Update head to remove any <style> blocks and include style.css
head = re.sub(r'<style>.*?</style>', '', head, flags=re.DOTALL)
head = re.sub(r'</head>', '    <link href="/style.css" rel="stylesheet" type="text/css" media="all">\n</head>', head)
head = re.sub(r'<strong>cooper</strong>', '<a href="/index.html"><strong>cooper</strong></a>', head)

# generate tag pages
for tag, entries in tag_map.items():
    rewritten_entries = [
        rewrite_image_paths(article) for article in entries
    ]

    head = re.sub(r'<title>.*?</title>', f'<title>{tag.title()}</title>', head, flags=re.DOTALL)

    with open(f"./cooper-undefined/tags/{tag}.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
{head}
<body class="page-tags">
{header}

<main>
  <p><a href="/tags.html">← All tags</a></p>
  <h1>{tag.title()}</h1>

  {''.join(rewritten_entries)}

</main>
</body>
</html>
""")

print(f"Generated {len(tag_map)} tag pages.")
