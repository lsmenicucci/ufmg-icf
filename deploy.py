from pathlib import Path
from subprocess import run
import json
import os

# read .env 
env = Path('.env').read_text()
env = env.split('\n')
env = [ line for line in env if "=" in line ]
env = { line.split('=')[0]: line.split('=')[1] for line in env }

PRES_RUN_CMD=env['PRES_RUN_CMD']
PRES_BUILD_CMD=env['PRES_BUILD_CMD']
PRES_DIR=env['PRES_DIR']
PRES_BUILD_DIR=env['PRES_BUILD_DIR']
PRES_DEPLOY_DIR=env['PRES_DEPLOY_DIR']

# find folders with index.html on it
here = Path(__file__).parent
presentations = (here / PRES_DIR).glob('*/index.html')

links = {}
for presentation in presentations:
    os.chdir(presentation.parent) 
    print(f'Building {presentation.parent}') 
    cmd = f'{PRES_BUILD_CMD} index.html' 
    run(cmd, shell=True)

    print(f'Deploying {presentation.parent}')
    deploy_dir = here / PRES_DEPLOY_DIR / presentation.parent.name
    deploy_dir.mkdir(parents=True, exist_ok=True)
    cmd = f'cp -r {PRES_BUILD_DIR}/* {deploy_dir}'
    run(cmd, shell=True) 

    name = presentation.parent.name

    # read meta
    meta_path = Path.cwd() / 'meta.json'
    if meta_path.exists():
        meta = json.loads(meta_path.read_text())
        name = meta.get('title', name)

    links[name] = f"/{presentation.parent.name}/index.html"

os.chdir(here / PRES_DEPLOY_DIR)

print("Copying index.html")
cmd = f'cp {here / "index.html"} {here / PRES_DEPLOY_DIR}'
run(cmd, shell=True)

print('Writing links.json')
with open('links.json', 'w') as f:
    json.dump(links, f, indent=4)
