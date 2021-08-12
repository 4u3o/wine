import argparse
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

parser = argparse.ArgumentParser(description='input data source')

parser.add_argument(
    '--source',
    '-s',
    default='wine3',
    help='data source (default = wine)'
)

args = parser.parse_args()

df = pd.read_excel(f'data/{args.source}.xlsx',
                   na_filter=False)
wines = df.to_dict('records')

groups_wines = defaultdict(list)

for wine in wines:
    groups_wines[wine['Категория']].append(wine)

groups_wines = sorted(groups_wines.items())

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.jinja')

rendered_page = template.render(
    data=groups_wines
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
