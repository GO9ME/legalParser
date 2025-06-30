# 법률 문서 계층 구조화 모듈

이 프로젝트는 다양한 국가의 법률 텍스트 원문을 입력받아, 내용의 의미적 유사성을 기반으로 계층 구조를 자동 생성하고 이를 CSV와 JSON 파일로 출력하는 모듈입니다.

Hugging Face의 `AmitTewari/LegalPro-BERT-base` 모델을 사용하여 법률 텍스트의 임베딩을 추출하고, 계층적 군집화(Hierarchical Clustering)를 통해 구조를 생성합니다.

## 주요 기능

- **다국어 지원**: `legal_structures.json` 설정을 통해 여러 국가의 법률 구조에 유연하게 대응 가능
- **의미 기반 구조화**: 단순 텍스트 매칭이 아닌, 문맥을 이해하는 언어 모델을 통해 유사한 조항들을 그룹화
- **두 가지 출력 형식**: 분석 및 활용이 용이한 `CSV` 파일과 웹 등에서 사용하기 좋은 계층적 `JSON` 파일 동시 생성

## 요구사항

프로젝트 실행에 필요한 라이브러리는 `requirements.txt`에 명시되어 있습니다. 아래 명령어로 설치할 수 있습니다.

```bash
pip install -r requirements.txt
```

## 실행 방법

본 모듈은 2단계의 과정을 거쳐 실행됩니다.

### 1단계: 법률 텍스트 임베딩 생성

먼저, 원본 법률 텍스트 파일로부터 임베딩을 추출하여 `.pkl` 파일로 저장해야 합니다.

`embedding_generator.py` 스크립트를 아래와 같이 실행하세요.

```bash
python embedding_generator.py --country [국가코드] --input [입력파일] --output [출력파일.pkl]
```

- `--country`: 처리할 국가의 코드입니다. `legal_structures.json`에 정의된 코드를 사용해야 합니다. (예: `KOREA`, `USA`, `JAPAN`)
- `--input`: 분석할 법률 텍스트 파일의 경로입니다. (예: `law_text_output.txt`)
- `--output`(선택 사항): 생성될 임베딩 파일의 이름입니다. 기본값은 `legal_embeddings.pkl` 입니다.

**실행 예시:**
```bash
python embedding_generator.py --country KOREA --input law_text_output.txt
```

### 2단계: 계층 구조 생성 및 파일 출력

1단계에서 생성된 임베딩 파일을 사용하여 계층 구조를 만들고 최종 결과물을 파일로 저장합니다.

`structured_hierarchy_generator.py` 스크립트를 아래와 같이 실행하세요.

```bash
python structured_hierarchy_generator.py --embeddings_file [임베딩파일.pkl]
```

- `--embeddings_file`: 1단계에서 생성된 `.pkl` 파일의 경로입니다.
- `--distance_threshold`(선택 사항): 클러스터링의 거리 임계값입니다. 값이 작을수록 더 많은 클러스터로 잘게 나뉘고, 클수록 더 큰 덩어리로 묶입니다. (기본값: 1.0)

**실행 예시:**
```bash
python structured_hierarchy_generator.py --embeddings_file legal_embeddings.pkl --distance_threshold 0.8
```

## 설정 (`legal_structures.json`)

`legal_structures.json` 파일은 국가별 법률 체계와 조항을 분리하기 위한 정규식을 정의합니다. 새로운 국가를 추가하려면 이 파일에 해당 국가의 코드, 이름, 정규식(`split_regex`) 등을 추가하면 됩니다.

## 결과물

실행이 완료되면 다음 두 개의 파일이 생성됩니다.

1.  `structured_hierarchy.csv`: 모든 계층 구조를 테이블 형태로 저장한 파일. Excel이나 데이터 분석 도구에서 열어보기 좋습니다.
2.  `structured_hierarchy.json`: 중첩된(nested) 구조로 저장된 JSON 파일. 웹 프론트엔드에서 트리 구조를 시각화하는 등 개발에 활용하기 용이합니다. 