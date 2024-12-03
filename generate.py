import os
import json
from io import StringIO

base_url = 'https://cwts.mooneze.org/#'
word_path = "./words"

word_path = os.path.abspath(word_path)

words = []

current_id = 0

for file_name in os.listdir(word_path):
    print(f"Loading from {file_name}")
    file_path = os.path.join(word_path, file_name)

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    name = ''

    pos = []
    desc = []
    examples = []

    flag = None

    for line in lines:

        content = line.strip()

        if content.startswith('# '):
            name = content.split('# ')[1]
        elif content == '## pos':
            flag = 'pos'
        elif content == '## desc':
            flag = 'desc'
        elif content == '## examples':
            flag = 'examples'
        else:
            if content == '':
                continue

            if flag == 'pos':
                pos.append(content)
            elif flag == 'desc':
                desc.append(content)
            elif flag == 'examples':
                if content.startswith('- '):
                    examples.append(content.split('- ')[1])

    words.append({
        'id': current_id,
        'name': name,
        'pos': ' '.join(pos),
        'description': ' '.join(desc),
        'examples': examples
    })

    current_id += 1

print(f"Writing, length: {len(words)}")

with open('db.json', 'w', encoding='utf-8') as f:
    f: StringIO

    json.dump(words, f, indent=2, separators=(',', ': '), ensure_ascii=False)

print("Done.")
print("Writing sitemap")

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(
        '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n'
        '<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n'
        '    <url>\n'
        f'        <loc>{base_url}/</loc>\n'
        '    </url>\n'
    )
    for word in words:
        f.write(
            '    <url>\n'
            f'        <loc>{base_url}/result?word={word["name"]}</loc>\n'
            '    </url>\n'
        )
    f.write('</urlset>')

print("Done.")
