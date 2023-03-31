import json
import os
from glob import glob


def get_filepaths():
    file_paths = [y for x in os.walk(".") for y in glob(os.path.join(x[0], "*.ipynb"))]
    file_paths.sort()
    return file_paths


def prepare_inner_title(raw_json_part: dict):
    title = raw_json_part["source"][0].strip()
    # if len(title) > 3 and title[0:3] == '## ':
    #     return '\n\t\t' + title.replace('#', '').replace(' ', '1. ', 1)
    if len(title) > 2 and title[0:2] == "# ":
        return f"{title.replace('#', '').strip()}"


def is_md_title(raw_json_part: dict):
    return (
        raw_json_part["cell_type"] == "markdown"
        and len(raw_json_part["source"]) > 0
        and raw_json_part["source"][0][0] == "#"
    )


def parse_inner_level(string: str):
    file_titles = string.split(" ", 1)
    if len(file_titles) > 1:
        title = f"\n\t1. "
        # title = f"\n\t1. {file_titles[1].capitalize()}"
        with open(filepath) as f:
            file_content = json.loads(f.read())

            markdown_cells = [
                prepare_inner_title(x) for x in file_content["cells"] if is_md_title(x)
            ]

        title += "".join([cell for cell in markdown_cells if cell is not None])
        return title
    else:
        return ""


if __name__ == "__main__":
    filepaths = get_filepaths()
    toc = ""
    dir_lvl_1_titles = set()
    for filepath in filepaths:
        if "checkpoints" in filepath:
            continue

        filepath_prepared = (
            filepath.replace("_", " ")
            .replace(".ipynb", "")
            .replace("./", "")
            .split("/")
        )
        dir_lvl_1 = filepath_prepared[0].split(" ", 1)[1].replace("_", " ").title()
        if dir_lvl_1 not in dir_lvl_1_titles:
            dir_lvl_1_len = len(dir_lvl_1_titles)
            toc += ("\n" if dir_lvl_1_len else "") + f"1. {dir_lvl_1}"
            dir_lvl_1_titles.add(dir_lvl_1)
        for inner_name in filepath_prepared[1:]:
            toc += parse_inner_level(string=inner_name)

        with open("./TOC.md", "w") as toc_md:
            toc_md.write(toc)
