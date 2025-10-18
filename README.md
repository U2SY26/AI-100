# AI_100 대회 준비 환경

카카오임팩트 AI_100 대회를 위한 준비 환경입니다.

## 설치 완료된 라이브러리

### Python 백엔드 라이브러리

#### 데이터 처리 & 분석
- pandas, numpy, scipy
- matplotlib, seaborn, plotly

### 머신러닝 & 딥러닝
- scikit-learn, xgboost, lightgbm
- torch, tensorflow
- transformers (Hugging Face)

### LLM API
- openai
- anthropic

### 웹 개발 & UI
- streamlit
- gradio
- flask, fastapi

### 자연어 처리
- nltk, konlpy
- sentence-transformers

### 컴퓨터 비전
- opencv-python
- pillow

#### 유틸리티
- requests, python-dotenv
- jupyter, notebook
- beautifulsoup4, selenium

### JavaScript/TypeScript 프론트엔드 라이브러리

#### 프레임워크
- React 18.3 + Vite
- Next.js 15
- Vue 3
- Svelte 5

#### 애니메이션 & 효과
- Framer Motion
- GSAP
- Animate.css
- AOS (Animate On Scroll)
- React Spring

#### UI 라이브러리
- Tailwind CSS + DaisyUI
- Material-UI (MUI)
- Ant Design
- Headless UI

#### 차트 & 시각화
- Chart.js + React-Chartjs-2
- Recharts
- D3.js
- Plotly.js

#### 상태관리
- Zustand
- Jotai
- Recoil
- React Query / TanStack Query

#### 폼 처리
- React Hook Form
- Formik
- Yup / Zod (유효성 검사)

#### 유틸리티
- Axios / SWR (데이터 페칭)
- React Router DOM
- React Icons / Lucide React
- Date-fns / Day.js / Moment
- Lodash
- React Markdown
- Socket.io Client
- React Dropzone
- React Toastify / Sonner

#### 앱 개발
- React Native
- Expo
- Electron

## 빠른 시작

### Python 백엔드

### 1. 템플릿 사용하기
```python
python quick_start_templates.py
```

### 2. Streamlit 앱 실행
```bash
streamlit run app.py
```

### 3. Gradio 인터페이스
```python
python gradio_app.py
```

### 4. FastAPI 서버
```bash
uvicorn main:app --reload
```

### 5. Jupyter Notebook
```bash
jupyter notebook
```

### JavaScript 프론트엔드

#### 1. React + Vite 앱 시작
```bash
npm run dev:react
# 또는 새 프로젝트
npm create vite@latest my-app -- --template react
```

#### 2. Next.js 앱 시작
```bash
npm run dev:next
# 또는 새 프로젝트
npx create-next-app@latest my-next-app
```

#### 3. 컴포넌트 사용
```jsx
// src/components/ChatInterface.jsx - AI 챗봇
// src/components/DataDashboard.jsx - 데이터 대시보드
```

#### 4. 프론트엔드 템플릿 가이드
[frontend_templates.md](frontend_templates.md) 참고

## API 키 설정

1. `.env.example` 파일을 `.env`로 복사
2. 실제 API 키 입력

```bash
cp .env.example .env
```

## 대회 팁

### 시간 관리
- **0-10분**: 문제 정확히 이해
- **10-30분**: 데이터 탐색 및 전략 수립
- **30-110분**: 구현 및 개선
- **110-120분**: 테스트 및 제출 준비

### 체크리스트
- [ ] 문제 요구사항 정확히 파악
- [ ] 데이터 형식 및 특성 확인
- [ ] 평가 지표 확인
- [ ] 간단한 베이스라인 먼저 구현
- [ ] 점진적으로 개선
- [ ] 제출 전 최종 테스트

## 주요 템플릿

### 데이터 분석
`quick_start_templates.py`의 `data_analysis_template()` 참고

### ML 분류
`quick_start_templates.py`의 `ml_classification_template()` 참고

### LLM 활용
`quick_start_templates.py`의 `llm_api_template()` 참고

### 웹앱 구축
`quick_start_templates.py`의 `streamlit_app_template()` 또는 `gradio_interface_template()` 참고

## 행운을 빕니다! 🚀
