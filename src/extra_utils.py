

def extract_title(markdown):
    lines = markdown.split("\n")
    h1s = [line for line in lines if line.startswith("# ")]
    if h1s == []:
        raise Exception("No title (H1 header) to extract")
    return h1s[0][2:]
