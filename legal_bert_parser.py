import re
import pandas as pd
import argparse
import json
from tqdm import tqdm

def load_country_config(country_code, config_file="legal_structures.json"):
    with open(config_file, encoding='utf-8') as f:
        config = json.load(f)
    return config[country_code.upper()]

def parse_law_structure(lines, country_config):
    hierarchy = country_config['hierarchy']
    patterns = [(level, re.compile(country_config['patterns'][level].replace('^', ''))) for level in hierarchy]
    stack = []  # (level, id)
    results = []
    id_counter = 1
    order_counters = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        matched = None
        for idx, (level, regex) in enumerate(patterns):
            if regex.match(line):
                matched = (level, idx)
                break

        if matched:
            level, level_idx = matched
            # 상위 계층 pop
            while stack and hierarchy.index(stack[-1][0]) >= level_idx:
                stack.pop()
            parent_id = stack[-1][1] if stack else -1
            order = order_counters.get(parent_id, 1)
            order_counters[parent_id] = order + 1

            results.append({
                'id': id_counter,
                'title_id': id_counter,
                'parent_id': parent_id,
                'depth': level_idx,
                'order': order,
                'type': level,
                'text': line
            })
            stack.append((level, id_counter))
            id_counter += 1
        else:
            # 내용은 가장 최근 계층이 부모
            parent_id = stack[-1][1] if stack else -1
            depth = hierarchy.index(stack[-1][0]) + 1 if stack else 0
            order = order_counters.get(parent_id, 1)
            order_counters[parent_id] = order + 1
            results.append({
                'id': id_counter,
                'title_id': id_counter,
                'parent_id': parent_id,
                'depth': depth,
                'order': order,
                'type': 'content',
                'text': line
            })
            id_counter += 1

    return pd.DataFrame(results, columns=['id', 'title_id', 'parent_id', 'depth', 'order', 'type', 'text'])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required=True)
    parser.add_argument("--country", required=True)
    parser.add_argument("--output_csv", required=True)
    args = parser.parse_args()

    config = load_country_config(args.country)
    with open(args.input_file, encoding='utf-8') as f:
        lines = f.readlines()
    df = parse_law_structure(lines, config)
    df.to_csv(args.output_csv, index=False, encoding='utf-8-sig')
    print(f"CSV 저장 완료: {args.output_csv}")

if __name__ == "__main__":
    main() 