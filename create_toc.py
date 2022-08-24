import json
import os
from glob import glob


def get_filepaths():
    file_paths = [y for x in os.walk('.') for y in glob(os.path.join(x[0], '*.ipynb'))]
    file_paths.sort()
    return file_paths


def prepare_inner_title(raw_json_part: dict):
    title = raw_json_part['source'][0].strip()
    if len(title) > 1 and title[1] == '#':

        return '\n' + title.replace('#', '\t')  # .replace(' ', '- ', 1)
    else:
        # return ' (**' + title.replace('#', '').strip() + '**)'
        return f" ({title.replace('#', '').strip()})"


def is_md_title(raw_json_part: dict):
    return raw_json_part['cell_type'] == 'markdown' \
           and len(raw_json_part['source']) > 0 \
           and raw_json_part['source'][0][0] == '#'


def parse_inner_level(string: str):
    title = ('\n' if string[0:2] != '00' or string[0:2] != '01' else '') + '\t' + string.title()
    with open(filepath) as f:
        file_content = json.loads(f.read())

        markdown_cells = [prepare_inner_title(x)
                          for x in file_content['cells']
                          if is_md_title(x)]

    title += ''.join(markdown_cells)
    return title


if __name__ == '__main__':
    filepaths = get_filepaths()
    toc = ''
    dir_lvl_1_titles = set()
    for filepath in filepaths:
        if 'checkpoints' in filepath or 'hw' in filepath:
            continue

        filepath_prepared = filepath.replace('_', ' ').replace('.ipynb', '').replace('./', '').split('/')
        dir_lvl_1 = filepath_prepared[0].split(' ', 1)[1].replace('_', ' ').title()
        if dir_lvl_1 not in dir_lvl_1_titles:
            dir_lvl_1_len = len(dir_lvl_1_titles)
            toc += ('\n' if dir_lvl_1_len else '') + f"{dir_lvl_1_len:02d} {dir_lvl_1}\n"
            dir_lvl_1_titles.add(dir_lvl_1)
        for inner_name in filepath_prepared[2:]:
            toc += parse_inner_level(string=inner_name)

        with open('./TOC.txt', 'w') as toc_md:
            toc_md.write(toc)
