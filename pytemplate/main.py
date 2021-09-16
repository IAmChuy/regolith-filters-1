import merge
import json
import sys
from itertools import chain
from pathlib import Path
import math
import uuid

def walk_json(data, parent=None, parent_key=None):
    '''
    Walks JSON file (data) yields tuples: key, parent_key, parent.

    Hint: To access child value use parent[parent_key][child_key], in first
    iteration 'parent' and 'parent_key' are None.
    '''
    if isinstance(data, dict):
        for k in data.keys():
            if isinstance(data[k], (dict, list)):
                yield from walk_json(data[k], parent=data, parent_key=k)
            yield k, parent_key, parent
    elif isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], (dict, list)):
                yield from walk_json(data[i], parent=data, parent_key=i)
            yield i, parent_key, parent


if __name__ == '__main__':
    config = json.loads(sys.argv[1])
    # Glob patters for finding JSON files to edit
    if 'bp_patterns' in config:
        bp_patterns = config['bp_patterns']
    else:
        bp_patterns = ['**/*.json']
    if 'rp_patterns' in config:
        rp_patterns = config['rp_patterns']
    else:
        rp_patterns = ['**/*.json']

    # File path to the templates folder
    templates_path = Path(config['templates_path'])

    # Trigger phrase
    if 'trigger_phrase' in config:
        trigger_phrase = config['trigger_phrase']
    else:
        trigger_phrase = "TEMPLATE"
    if 'sort_keys' in config:
        sort_keys = config['sort_keys']
    else:
        sort_keys = True
    if 'compact' in config:
        compact = config['compact']
    else:
        compact = False

    # Default scope for eval
    scope = {'true': True, 'false': False, 'math': math, 'uuid': uuid}
    if 'scope' in config:
        scope = scope | config['scope']
    # Resolve glob patterns
    bp_paths = []
    for i in bp_patterns:
        bp_paths.extend(j for j in Path('BP').glob(i))
    bp_paths = list(set(bp_paths))
    rp_paths = []
    for i in rp_patterns:
        rp_paths.extend(j for j in Path('RP').glob(i))
    rp_paths = list(set(rp_paths))

    fp: Path
    # Replace values in file using templates
    for fp in chain(bp_paths, rp_paths):
        if not fp.exists() or not fp.is_file():
            continue 
        try:
            with fp.open('r') as f:
                data = json.load(f)
        except:
            print(f"Unable to load file {fp.as_posix()}")
            continue
        # Gather points of iterests (things that will be replaced)
        points_of_interset = []
        for k, parent_k, parent in walk_json(data):
            if isinstance(k, str) and k.startswith(trigger_phrase):
                points_of_interset.append((k, parent_k, parent))
        for k, parent_k, parent in points_of_interset:
            try:
                template_name = k.split(":", 1)[1]
                template_path = templates_path / (template_name + '.py')
                with template_path.open('r') as f:
                    template = f.read()
            except:
                print(f"Unable to read template {k} from file file {fp.as_posix()}")
                continue
            if parent is None:  # Templating root
                curr_scope = scope | data[k]
                del data[k]
                data = merge.deep_merge_objects(data, eval(template, curr_scope))
                continue
            # Templating offspring
            curr_scope = scope | parent[parent_k][k]
            del parent[parent_k][k]
            parent[parent_k] = merge.deep_merge_objects(parent[parent_k], eval(template, curr_scope))
        with fp.open('w') as f:
            if compact:
                json.dump(data, f, indent='\t', sort_keys=sort_keys)
            else:
                json.dump(data, f, indent='\t', separators=(',', ':'))
