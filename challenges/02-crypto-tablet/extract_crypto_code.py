"""
암호 석판 이미지에서 코드 추출
OCR 또는 수동 입력으로 코드 추출
"""

import pytesseract
from PIL import Image
import re

def extract_code_from_image(image_path):
    """이미지에서 OCR로 코드 추출"""
    try:
        # Tesseract 경로 설정 (Windows)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        # 이미지 로드
        img = Image.open(image_path)

        # OCR 수행 (코드 인식을 위한 설정)
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(img, config=custom_config)

        return text
    except Exception as e:
        print(f"OCR 오류: {e}")
        return None

def manual_code_entry():
    """이미지를 보고 수동으로 코드 입력"""

    # 이미지에서 보이는 코드를 직접 타이핑
    # 첫 줄부터 정확하게 입력
    code = """#include<stdio.h>//char*c_s="S";printf(c_s);char*c_n="N";printf(c_n);char*c_v="V";r=lambda x:input("TURNAROUND");char*a="G";i=input;a+="NO";q="TL";b="R";b+="W";a+=b;q+="AH";q=q[::-1];a=a[::-1];p=lambda x:print(x,end=b[:0])or(exit());"""char*;
void(p)(char**x){printf(x);};int(main)(){char*c_e="E";p(c_e);char*c_q="Q";p(c_q);char*c_x="X";p(c_x);p("CURSED");char*c_u="";if(i()!=q)
                                                                                                                                        :p(a);83j;
eval;#char                                                                                                                                                   c[8888];c;
8//8;eval;            hex;j=          input;             r="A";                  i=input;                    8;i=input;p=print;8;
eval;8//8;         8;r=            "H";                   False;              r="L";                          888;r="T";r+="Q";88;     ([]);eval;
eval;8//8;         r=r+            "C";                   i=input;                88j;                                8+8;            8//8;eval;
8+*8;8+*8;         r=r+            "T";                   p=print;                8+8;                                8+3;            ([]);8//8;
([]);([8]);         r=r+            "Q";                   r=r+    "Z";                8+3;                                888;            open;8+*8;
8+*8;8+*8;8//8;   p=print;r+="S";88;     r=r+    "B";                888;                                83j;            8//8;open;
8//8;eval;         True;r+="E";False;  r=r+    "S";                r=r+                                8+3;            eval;8//8;
8+*8;8//8;         r=r+            "X";                   r=r+    "T";                len;                                8+8;            eval;([]);
8+*8;8//8;         r=r+            "V";                   abs;r+="R";88;              8+8;                                8/8;            ([]);([]);
8+*8;8//8;         r=r+            "C";                   83j;r="A";838;              8/8;                                8/3;            open;eval;
open;8//8;         r=r+            "I";                   r=r+    "T";                8/3;                                88j;            open;([]);
([]);eval;         r=r+            "Q";                   r=r+            "P";                p=print;r+="1";8+8;             8+8;            ([]);([]);
8+*8;8+*8;         r+="O"          ;pass;         8;pass          ;pass;         8j;r+="0";8//8;pass;         38;p(r);        open;([]);
eval;([]);                                                                                                                                                                                                                                ([]);8//8;
eval;([]);([]);eval;8+*8;([]);eval;8+*8;([]);eval;8+*8;open;8+*8;open;eval;eval;8//8;8+*8;eval;8//8;8//8;([]);8+*8;8//8;([]);open;8//8;
eval;8+*8;([]);([]);eval;eval;open;([]);eval;8//8;8//8;8//8;([]);open;eval;([]);eval;eval;eval;8//8;open;8+*8;8//8;([]);eval;8//8;open;8+*8;8//8;
open;eval;8+*8;8//8;eval;8+*8;8//8;8//8;8//8;([]);8+*8;8//8;open;8+*8;8+*8;8//8;8//8;open;([]);([]);eval;"""

    return code

if __name__ == "__main__":
    print("암호 석판 코드 추출 중...")

    # OCR 시도
    # ocr_code = extract_code_from_image("ai_top_100_crypto.png")

    # 수동 입력
    code = manual_code_entry()

    # 코드 저장
    with open("crypto_extracted.c", "w", encoding="utf-8") as f:
        f.write(code)

    print("코드가 crypto_extracted.c에 저장되었습니다.")
    print("\n첫 100자:")
    print(code[:100])
