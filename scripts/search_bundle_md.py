import os, re

cache_file = r'C:\Users\fury6\AppData\Local\Opera Software\Opera Air Stable\Default\Cache\Cache_Data\f_00a264'
with open(cache_file, 'rb') as fp:
    data = fp.read()

print(f'Total size: {len(data)}')

# Search for markdown import keywords
keywords = [b'importMarkdown', b'markdownTo', b'parseMarkdown', b'markdownImport', b'exportMarkdown', b'Heading 2', b'isHeading', b'headingLevel']
for kw in keywords:
    matches = [m.start() for m in re.finditer(re.escape(kw), data)]
    print(f'{kw.decode("latin1")}: {len(matches)} matches')
    for pos in matches[:2]:
        chunk = data[max(0, pos-150):min(len(data), pos+300)]
        print('  Snippet:', chunk.decode('latin1', errors='replace').replace('\n', ' '))
