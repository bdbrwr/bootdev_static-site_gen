from block_markdown import markdown_to_html_node
import os


def read_file(path):
    with open(path) as f:
        contents = f.read()
    return contents


def extract_title(markdown):
    lines = markdown.split("\n")
    h1s = [line for line in lines if line.startswith("# ")]
    if h1s == []:
        raise Exception("No title (H1 header) to extract")
    return h1s[0][2:]


def generate_page(from_path, template_path, to_path):
    print(f" * Generating page from {from_path} to {to_path} using {template_path}")

    md = read_file(from_path)
    template = read_file(template_path)

    content = markdown_to_html_node(md)
    content_html = content.to_html()

    title = extract_title(md)

    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)

    with open(to_path, "w") as f:
        f.write(html)


def generate_pages_recursive(source_dir, template_path, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    for filename in os.listdir(source_dir):
        from_path = os.path.join(source_dir, filename)
        to_path = os.path.join(dest_dir, filename)
        if os.path.isfile(from_path):
            to_path = to_path.replace(".md", ".html")
            generate_page(from_path, template_path, to_path)
        else:
            generate_pages_recursive(from_path, template_path, to_path)