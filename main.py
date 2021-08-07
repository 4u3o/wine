import argparse
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

parser = argparse.ArgumentParser(description='input data source')

parser.add_argument(
    '--source',
    '-s',
    default='wine2',
    help='data source (default = wine)'
)

args = parser.parse_args()

df = pd.read_excel(f'data/{args.source}.xlsx').fillna(value='')
dd = defaultdict(str)
sort_param = 'Категория'


def sort_by_param(df, param):
    columns = [x for x in df.columns.values if x != param]
    return (df.groupby(param)[columns]
            .apply(lambda x: x.to_dict('records', into=dd)))


if sort_param in df.columns:
    data = sort_by_param(df, sort_param)
else:
    data = df.to_dict('records', into=dd)


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.jinja')

rendered_page = template.render(
    data=data
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
