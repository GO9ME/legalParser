# 파일명: restructure_law.py
import re
import argparse
import json
import os

def load_country_config(country_code, config_file="legal_structures.json"):
    """국가별 법률 구조 설정을 로드합니다."""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            full_config = json.load(f)
        # 국가 코드를 대문자로 비교하여 일관성 유지
        config = full_config.get(country_code.upper())
        if not config or 'patterns' not in config:
            print(f"오류: '{config_file}' 파일에서 '{country_code}'에 대한 설정 또는 'patterns'를 찾을 수 없습니다.")
            return None
        return config
    except FileNotFoundError:
        print(f"오류: 설정 파일 '{config_file}'을(를) 찾을 수 없습니다.")
        return None
    except json.JSONDecodeError:
        print(f"오류: '{config_file}' 파일이 올바른 JSON 형식이 아닙니다.")
        return None

def restructure_text(lines, country_config):
    """
    계층 패턴(항, 호, 목 등)이 등장하면, 그 줄의 나머지 내용까지 한 줄로 합침.
    즉, '① 내용...' 형태로 한 줄로 만듦.
    """
    hierarchy_patterns_dict = country_config.get('patterns', {})
    # 계층 패턴을 맨 앞에서만 찾도록 보정
    split_patterns = [p.lstrip('^').replace('\\s', '\\s*') for p in hierarchy_patterns_dict.values()]
    combined_pattern = re.compile('|'.join(split_patterns))
    cleanup_pattern = re.compile(r'조문체계도버튼연혁|조문체계도버튼|연혁|광고')

    final_lines = []
    buffer = ""
    for line in lines:
        line = cleanup_pattern.sub('', line).strip()
        if not line:
            continue

        # 계층 패턴(항, 호, 목 등)만 단독으로 등장하면, 다음 줄과 합침
        if combined_pattern.fullmatch(line) and buffer == "":
            buffer = line
            continue
        elif buffer:
            # buffer에 계층 패턴이 있고, 이번 줄이 내용이면 합쳐서 한 줄로 저장
            final_lines.append(f"{buffer} {line}")
            buffer = ""
        else:
            final_lines.append(line)
    # 혹시 마지막에 buffer만 남아있으면 추가
    if buffer:
        final_lines.append(buffer)
    return final_lines

def clean_lines(lines):
    # 불필요한 텍스트만 제거, 줄바꿈은 최대한 보존
    cleanup_pattern = re.compile(r'조문체계도버튼연혁|연혁|광고')
    return [cleanup_pattern.sub('', line).strip() for line in lines if line.strip()]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    parser.add_argument("--country", required=True)
    args = parser.parse_args()

    country_config = load_country_config(args.country)
    if not country_config:
        print("국가별 패턴 로드 실패")
        return

    with open(args.input_file, encoding='utf-8-sig') as f:
        lines = f.readlines()
    processed = restructure_text(lines, country_config)
    with open(args.output_file, 'w', encoding='utf-8') as f:
        for line in processed:
            f.write(line + '\n')
    print(f"전처리 완료: '{args.input_file}' -> '{args.output_file}'")

if __name__ == "__main__":
    main() 