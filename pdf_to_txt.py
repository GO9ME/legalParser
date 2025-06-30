import fitz  # PyMuPDF
import argparse
import os

def pdf_to_txt(pdf_path, txt_path):
    # PDF 열기
    doc = fitz.open(pdf_path)
    with open(txt_path, 'w', encoding='utf-8') as f:
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            # 페이지별로 줄바꿈 추가
            f.write(text)
            f.write('\n')
    print(f"PDF -> TXT 변환 완료: {pdf_path} -> {txt_path}")

def main():
    parser = argparse.ArgumentParser(description="PDF 파일을 TXT로 변환")
    parser.add_argument("pdf_file", help="입력 PDF 파일 경로")
    parser.add_argument("txt_file", help="출력 TXT 파일 경로")
    args = parser.parse_args()

    if not os.path.exists(args.pdf_file):
        print(f"PDF 파일이 존재하지 않습니다: {args.pdf_file}")
        return

    pdf_to_txt(args.pdf_file, args.txt_file)

if __name__ == "__main__":
    main() 