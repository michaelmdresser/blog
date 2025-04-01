#!/usr/bin/env python

import os
from os.path import join, splitext, basename

posts_directory = "./posts"

output_directory = "./docs"
output_posts_directory = join(output_directory, "posts")

finished_posts = [
    "2021-11-27_how-to-parse-eve-chat-log.md",
    "2022-04-24_context-variable-log-level-koka-effects.org",
    "2023-03-11_custom-github-action-rapid-development.org",
]


index_md = """
---
title: "The blog of Michael Dresser"
---

Visit my home page at [michaelmdresser.com](https://michaelmdresser.com).

## Posts

"""

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
            if "title:" in line:
                title = line.replace("title:", "").strip()
                break

            # for .org files
            if "#+TITLE:" in line:
                title = line.replace("#+TITLE:", "").strip()
                break

    with open(full_post_path) as f:
        for line in f.readlines():
            if "date:" in line:
                date = line.replace("date:", "").strip()
                break

            # for .org files
            if "#+DATE:" in line:
                date = line.replace("#+DATE:", "").strip()
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
