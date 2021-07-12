import argparse
import requests
import urllib
import json
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', required=True, help='Specify username')
parser.add_argument('-p', '--password', required=True, help='Specify password')
parser.add_argument('-s', '--sample_url', required=True, help='Specify sample-url link')
parser.add_argument('-o', '--output_dir', required=True, help='Specify output directory')
args = parser.parse_args()

username = args.username
password = args.password
sample_url = args.sample_url
output_dir = args.output_dir

output_dir = Path(output_dir)
output_dir.mkdir(parents=True, exist_ok=True)

def parse_sample_url(url):
    url = urllib.parse.urlparse(url)
    job, sample = list(map(lambda x: ''.join(filter(str.isdigit, x)), url.path.split('sample')))
    return '://'.join([url.scheme, url.netloc]), f'/rest_api/jobs/{job}/samples/{sample}'

def api(path):
    auth = requests.auth.HTTPBasicAuth(username, password)
    response = requests.get(urllib.parse.urljoin(host, path), auth=auth)
    return response

host, path = parse_sample_url(sample_url)
response = json.loads(api(path).text)
chains = response['results']['ir']['chains']
for chain in chains:
    response = json.loads(api(urllib.parse.urlparse(chain['detail_url']).path).text)
    file_name = response['source_file_url'].split('/')[-1]
    response = api(urllib.parse.urlparse(response['source_file_url']).path)
    with open(output_dir.joinpath(file_name), 'w') as f:
        f.write(response.text)
