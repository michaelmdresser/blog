#!/usr/bin/env python

import os
from os.path import join, splitext, basename

posts_directory = "./posts"

output_directory = "./docs"
output_posts_directory = join(output_directory, "posts")

finished_posts = [
    "2021-11-27_how-to-parse-eve-chat-log.md",
]


index_md = '''
---
title: "Michael Dresser's blog"
---

Visit my home page at [michaeldresser.io](https://michaeldresser.io).

## Posts

'''

# Reversed for stack-listing on the index
for post in reversed(finished_posts):
    full_post_path = join(posts_directory, post)

    post_html_name = splitext(post)[0] + ".html"
    output_post_path = join(output_posts_directory, post_html_name)
    output_post_path_relative = join("posts", post_html_name)

    print(f"Converting {full_post_path} to {output_post_path}")
    os.system(
        f"pandoc \\"
        f"--data-dir='_pandoc' \\"
        f"--template='_pandoc/templates/post.html' \\"
        f"--css='/style.css' \\"
        f"--standalone \\"
        f"-o {output_post_path} {full_post_path}"
    )

    title = None
    date = None
    # super hacky header YAML parsing
    with open(full_post_path) as f:
        for line in f.readlines():
            if 'title:' in line:
                title = line.replace("title:", "").strip()
                break

    with open(full_post_path) as f:
        for line in f.readlines():
            if 'date:' in line:
                date = line.replace("date:", "").strip()
                break

    if title is None:
        raise Exception(f"failed to find title for post: {full_post_path}")

    if date is None:
        raise Exception(f"failed to find date for post: {full_post_path}")

    index_md += f"- {date} - [{title}]({output_post_path_relative}) \n"

    with open("/tmp/BLOG_index.md", "w") as f:
        f.write(index_md)

    index_html_file = join(output_directory, "index.html")
    os.system(
        f"pandoc \\"
        f"--data-dir='_pandoc' \\"
        f"--template='_pandoc/templates/index.html' \\"
        f"--css=style.css \\"
        f"--standalone \\"
        f"-o '{index_html_file}' '/tmp/BLOG_index.md'"
    )
