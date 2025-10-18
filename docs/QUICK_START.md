# AI_100 대회 빠른 시작 가이드

## 🚀 대회 시작하자마자 할 일

### 1단계: 문제 파악 (첫 5분)

```bash
# 1. 문제 유형 확인
- [ ] 데이터 분석/시각화
- [ ] 머신러닝/딥러닝
- [ ] 웹 앱 개발
- [ ] AI API 활용
- [ ] 챗봇 구현

# 2. 입출력 형식 확인
- [ ] 입력 데이터 형식
- [ ] 출력 형식 및 제출 방법
- [ ] 평가 지표
```

### 2단계: 환경 선택 및 템플릿 복사 (5-10분)

#### 옵션 A: Python 백엔드/ML

```bash
# 데이터 분석
python quick_start_templates.py

# Streamlit 앱
streamlit run app.py

# Jupyter 노트북
jupyter notebook
```

#### 옵션 B: JavaScript 프론트엔드

```bash
# React 빠른 시작
npm create vite@latest my-app -- --template react
cd my-app
npm install
npm install axios framer-motion tailwindcss chart.js react-chartjs-2
npm run dev

# Next.js (API 포함 풀스택)
npx create-next-app@latest my-app --typescript --tailwind
cd my-app
npm run dev
```

#### 옵션 C: 하이브리드 (백엔드 + 프론트엔드)

```bash
# 터미널 1: Python FastAPI 백엔드
uvicorn main:app --reload --port 8000

# 터미널 2: React 프론트엔드
npm run dev
```

---

## 📋 시나리오별 빠른 템플릿

### 시나리오 1: AI 챗봇 구현

**기술 스택**: React + OpenAI API

```bash
# 1. 프로젝트 생성
npm create vite@latest ai-chatbot -- --template react
cd ai-chatbot
npm install
npm install axios openai

# 2. 컴포넌트 복사
cp ../src/components/ChatInterface.jsx src/components/

# 3. API 키 설정
cp ../.env.example .env
# .env 파일에서 OPENAI_API_KEY 설정

# 4. 실행
npm run dev
```

### 시나리오 2: 데이터 시각화 대시보드

**기술 스택**: React + Chart.js

```bash
# 1. 프로젝트 생성
npm create vite@latest dashboard -- --template react
cd dashboard
npm install
npm install chart.js react-chartjs-2

# 2. 컴포넌트 복사
cp ../src/components/DataDashboard.jsx src/components/

# 3. 실행
npm run dev
```

### 시나리오 3: 데이터 분석 및 ML

**기술 스택**: Python + Pandas + Scikit-learn

```python
# quick_analysis.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# 데이터 로드
df = pd.read_csv('data.csv')

# 빠른 분석
print(df.head())
print(df.info())
print(df.describe())

# 간단한 모델
X = df.drop('target', axis=1)
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)
print(f"Accuracy: {model.score(X_test, y_test)}")
```

```bash
python quick_analysis.py
```

### 시나리오 4: Streamlit 인터랙티브 앱

**기술 스택**: Streamlit + Python

```python
# app.py
import streamlit as st
import pandas as pd

st.title("AI_100 데모 앱")

uploaded_file = st.file_uploader("CSV 파일 업로드", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)
    st.write(df.describe())

    if st.button("분석 실행"):
        st.success("분석 완료!")
```

```bash
streamlit run app.py
```

### 시나리오 5: LLM API 활용

**기술 스택**: Python + OpenAI

```python
# llm_demo.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def chat(message):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

print(chat("Hello!"))
```

```bash
python llm_demo.py
```

---

## ⚡ 초고속 체크리스트

### 시작 전 (0분)
- [ ] API 키 준비 완료 (OpenAI, Anthropic 등)
- [ ] 인터넷 연결 확인
- [ ] Python 및 Node.js 환경 확인

### 문제 확인 (0-10분)
- [ ] 문제 유형 파악
- [ ] 입출력 형식 확인
- [ ] 평가 지표 확인
- [ ] 제공 데이터 확인

### 초기 설정 (10-20분)
- [ ] 프로젝트 폴더 생성
- [ ] 템플릿 복사
- [ ] 필요한 라이브러리만 설치
- [ ] 기본 구조 확인

### 개발 (20-100분)
- [ ] 베이스라인 구현 (30분 목표)
- [ ] 첫 번째 제출 (50분 목표)
- [ ] 개선 및 최적화

### 마무리 (100-120분)
- [ ] 최종 테스트
- [ ] 에러 확인
- [ ] 제출

---

## 🎯 프로 팁

### 시간 절약 팁

1. **템플릿 활용**: 처음부터 코딩하지 말고 템플릿 복사
2. **라이브러리 최소화**: 필요한 것만 설치
3. **베이스라인 우선**: 완벽한 것보다 작동하는 것 먼저
4. **점진적 개선**: 작은 단위로 테스트하며 개선

### 기술 스택 선택 가이드

| 요구사항 | 추천 스택 | 이유 |
|---------|----------|------|
| 빠른 프로토타입 | Streamlit | 코드 최소, UI 자동 생성 |
| 인터랙티브 UI | React + Vite | 빠른 개발, 풍부한 라이브러리 |
| 풀스택 필요 | Next.js | API 라우트 포함 |
| 데이터 분석 | Jupyter | 탐색적 분석에 최적 |
| ML 모델 | scikit-learn | 빠르고 간단 |
| LLM 활용 | OpenAI API | 안정적이고 빠름 |
| 애니메이션 | Framer Motion | 간단하고 강력 |
| 차트 | Chart.js | 사용 쉬움 |

### 자주 쓰는 명령어

```bash
# Python
python script.py
streamlit run app.py
jupyter notebook
uvicorn main:app --reload

# Node.js
npm create vite@latest
npm install
npm run dev
npm run build

# Git (필요시)
git init
git add .
git commit -m "Initial commit"
```

### 디버깅 체크리스트

- [ ] API 키가 올바르게 설정되었는가?
- [ ] 필요한 라이브러리가 모두 설치되었는가?
- [ ] 포트가 이미 사용 중이지 않은가?
- [ ] 파일 경로가 올바른가?
- [ ] CORS 에러가 발생하지 않는가? (프론트-백엔드 연동 시)

---

## 🔥 초스피드 모드 (정말 급할 때)

### 1분 안에 시작하기

#### Python
```bash
python quick_start_templates.py
```

#### React
```bash
npm create vite@latest demo -- --template react && cd demo && npm install && npm run dev
```

#### Streamlit
```bash
streamlit run app.py
```

### 코드 스니펫 즐겨찾기

```python
# 데이터 로드
import pandas as pd
df = pd.read_csv('data.csv')

# OpenAI
from openai import OpenAI
client = OpenAI(api_key="...")
response = client.chat.completions.create(model="gpt-4o-mini", messages=[...])

# FastAPI
from fastapi import FastAPI
app = FastAPI()
@app.post("/predict")
async def predict(data: dict):
    return {"result": "..."}
```

```jsx
// React 기본
import { useState } from 'react'
const [data, setData] = useState(null)

// API 호출
const response = await fetch('/api/endpoint', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data)
})

// Chart.js
import { Line } from 'react-chartjs-2'
<Line data={chartData} options={options} />
```

---

## 🎓 리소스

- [quick_start_templates.py](quick_start_templates.py) - Python 템플릿
- [frontend_templates.md](frontend_templates.md) - React/Vue/Next.js 템플릿
- [src/components/](src/components/) - 재사용 가능한 컴포넌트
- [README.md](README.md) - 전체 문서

**행운을 빕니다! 화이팅! 🚀**
