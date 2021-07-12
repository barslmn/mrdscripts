import pandas as pd
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', required=True, help='Directory with tsv files')
args = parser.parse_args()
table_dir = args.directory

columns = {
    'Clone Abundance': 'count',
    'Clone Frequency': 'frequency',
    'Clonotype Sequence': 'CDR3nt',
    'CDR3 Translation': 'CDR3aa',
    'Predicted V Region': 'V',
    'Predicted D Region': 'D',
    'Predicted J Region': 'J',
}

table_path = Path(table_dir)
for table in table_path.glob('*.tsv'):
    df = pd.read_csv(table, sep='\t')
    df = df[columns.keys()]
    df.rename(columns=columns, inplace=True)
    vdj_path = table_path.joinpath('vdjtools_tables')
    vdj_path.mkdir(parents=True, exist_ok=True)
    df.to_csv(vdj_path.joinpath(table.name), sep='\t', index=False)
