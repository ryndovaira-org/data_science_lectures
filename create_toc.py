import json
import os
from glob import glob

filepaths = [y for x in os.walk('.') for y in glob(os.path.join(x[0], '*.ipynb'))]

filepaths.sort()
print(filepaths)

toc = ''

for filepath in filepaths:
    if 'checkpoints' in filepath or 'hw' in filepath:
        continue

    filepath_prepared = filepath.replace('_', ' ').replace('.ipynb', '').replace('./', '').split('/')
    print(filepath_prepared)
    dir_lvl_1 = filepath_prepared[0].split(' ')[1].title()
    toc += '1. ' + dir_lvl_1
    tab_count = 1
    for inner_name in filepath_prepared[2:]:
        toc += '\n' + '\t' * tab_count + '1. ' + inner_name.title().split(' ')[1].title()
        with open(filepath) as f:
            file_content = json.loads(f.read())

            markdown_cells = ['\n' + x['source'][0].strip().replace(' ', '1. ', 1).replace('#', '\t')
                              for x in file_content['cells']
                              if x['cell_type'] == 'markdown' and len(x['source']) > 0 and x['source'][0][0] == '#']

            toc += ''.join(markdown_cells)

    with open('./TOC.md', 'w') as toc_md:
        toc_md.write(toc)
