"""
AI_100 대회 빠른 시작 템플릿 모음
각 유형별로 빠르게 시작할 수 있는 코드 템플릿
"""

# ==================== 1. 데이터 분석 템플릿 ====================
def data_analysis_template():
    """데이터 분석 및 시각화 템플릿"""
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns

    # 데이터 로드
    # df = pd.read_csv('data.csv')

    # 기본 탐색
    # print(df.head())
    # print(df.info())
    # print(df.describe())

    # 시각화
    # plt.figure(figsize=(10, 6))
    # sns.heatmap(df.corr(), annot=True)
    # plt.show()

    pass


# ==================== 2. 머신러닝 분류 템플릿 ====================
def ml_classification_template():
    """머신러닝 분류 문제 템플릿"""
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, classification_report
    import pandas as pd

    # 데이터 준비
    # X = df.drop('target', axis=1)
    # y = df['target']

    # 학습/테스트 분리
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 모델 학습
    # model = RandomForestClassifier(n_estimators=100, random_state=42)
    # model.fit(X_train, y_train)

    # 예측 및 평가
    # y_pred = model.predict(X_test)
    # print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
    # print(classification_report(y_test, y_pred))

    pass


# ==================== 3. LLM API 활용 템플릿 ====================
def llm_api_template():
    """LLM API 활용 템플릿 (OpenAI)"""
    from openai import OpenAI
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": "Hello!"}
    #     ]
    # )

    # print(response.choices[0].message.content)

    pass


# ==================== 4. Streamlit 웹앱 템플릿 ====================
def streamlit_app_template():
    """Streamlit 웹앱 템플릿"""
    # 파일명: app.py 로 저장 후 실행: streamlit run app.py

    template_code = '''
import streamlit as st
import pandas as pd

st.title("AI_100 데모 앱")

# 사이드바
st.sidebar.header("설정")
option = st.sidebar.selectbox("옵션 선택", ["옵션1", "옵션2", "옵션3"])

# 메인 영역
st.header("데이터 업로드")
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("데이터 미리보기:")
    st.dataframe(df.head())

    st.write("기본 통계:")
    st.write(df.describe())

# 버튼과 입력
user_input = st.text_input("텍스트 입력")
if st.button("실행"):
    st.write(f"입력된 값: {user_input}")
'''

    return template_code


# ==================== 5. Gradio 인터페이스 템플릿 ====================
def gradio_interface_template():
    """Gradio 인터페이스 템플릿"""
    import gradio as gr

    def process_function(text_input):
        """처리 함수"""
        # 여기에 실제 처리 로직 작성
        return f"처리 결과: {text_input}"

    # 인터페이스 생성
    # interface = gr.Interface(
    #     fn=process_function,
    #     inputs=gr.Textbox(label="입력"),
    #     outputs=gr.Textbox(label="출력"),
    #     title="AI_100 데모",
    #     description="간단한 Gradio 인터페이스"
    # )

    # interface.launch(share=True)

    pass


# ==================== 6. 텍스트 분류 (Transformers) 템플릿 ====================
def text_classification_template():
    """Hugging Face Transformers 텍스트 분류 템플릿"""
    from transformers import pipeline

    # 사전학습 모델 사용
    # classifier = pipeline("sentiment-analysis")
    # result = classifier("I love this!")
    # print(result)

    # 한국어 모델 사용 예시
    # classifier = pipeline("sentiment-analysis", model="beomi/kcbert-base")
    # result = classifier("정말 좋아요!")
    # print(result)

    pass


# ==================== 7. 이미지 분류 템플릿 ====================
def image_classification_template():
    """이미지 분류 템플릿"""
    from transformers import pipeline
    from PIL import Image

    # 이미지 분류 파이프라인
    # classifier = pipeline("image-classification")
    # image = Image.open("image.jpg")
    # results = classifier(image)
    # print(results)

    pass


# ==================== 8. FastAPI 서버 템플릿 ====================
def fastapi_server_template():
    """FastAPI 서버 템플릿"""
    # 파일명: main.py 로 저장 후 실행: uvicorn main:app --reload

    template_code = '''
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    text: str
    value: int = 0

@app.get("/")
async def root():
    return {"message": "Hello AI_100!"}

@app.post("/predict")
async def predict(item: Item):
    # 여기에 예측 로직 작성
    result = {"input": item.text, "prediction": "결과"}
    return result

@app.get("/health")
async def health():
    return {"status": "ok"}
'''

    return template_code


# ==================== 9. 데이터 전처리 유틸리티 ====================
def data_preprocessing_utils():
    """데이터 전처리 유틸리티 함수들"""
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import StandardScaler, LabelEncoder

    def handle_missing_values(df):
        """결측치 처리"""
        # 숫자형: 평균으로 채우기
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

        # 범주형: 최빈값으로 채우기
        categorical_cols = df.select_dtypes(include=['object']).columns
        df[categorical_cols] = df[categorical_cols].fillna(df[categorical_cols].mode().iloc[0])

        return df

    def encode_categorical(df, columns):
        """범주형 변수 인코딩"""
        le = LabelEncoder()
        for col in columns:
            df[col] = le.fit_transform(df[col].astype(str))
        return df

    def normalize_features(df, columns):
        """특성 정규화"""
        scaler = StandardScaler()
        df[columns] = scaler.fit_transform(df[columns])
        return df

    pass


# ==================== 10. 한국어 텍스트 처리 ====================
def korean_text_processing():
    """한국어 텍스트 처리 템플릿"""
    # from konlpy.tag import Okt

    # okt = Okt()

    # text = "안녕하세요. 한국어 텍스트 처리 예제입니다."

    # # 형태소 분석
    # morphs = okt.morphs(text)
    # print(morphs)

    # # 명사 추출
    # nouns = okt.nouns(text)
    # print(nouns)

    # # 품사 태깅
    # pos = okt.pos(text)
    # print(pos)

    pass


if __name__ == "__main__":
    print("AI_100 대회 빠른 시작 템플릿 준비 완료!")
    print("\n사용 가능한 템플릿:")
    print("1. data_analysis_template() - 데이터 분석")
    print("2. ml_classification_template() - 머신러닝 분류")
    print("3. llm_api_template() - LLM API 활용")
    print("4. streamlit_app_template() - Streamlit 웹앱")
    print("5. gradio_interface_template() - Gradio 인터페이스")
    print("6. text_classification_template() - 텍스트 분류")
    print("7. image_classification_template() - 이미지 분류")
    print("8. fastapi_server_template() - FastAPI 서버")
    print("9. data_preprocessing_utils() - 데이터 전처리")
    print("10. korean_text_processing() - 한국어 텍스트 처리")
