# 프론트엔드 템플릿 모음

AI_100 대회에서 빠르게 사용할 수 있는 프론트엔드 템플릿 모음입니다.

## 목차
1. [React + Vite 기본 앱](#1-react--vite-기본-앱)
2. [Next.js 앱](#2-nextjs-앱)
3. [Vue 3 앱](#3-vue-3-앱)
4. [애니메이션 효과](#4-애니메이션-효과)
5. [차트 및 데이터 시각화](#5-차트-및-데이터-시각화)
6. [AI 챗봇 UI](#6-ai-챗봇-ui)
7. [파일 업로드 UI](#7-파일-업로드-ui)
8. [실시간 데이터 대시보드](#8-실시간-데이터-대시보드)

---

## 1. React + Vite 기본 앱

### 빠른 시작
```bash
npm create vite@latest my-react-app -- --template react
cd my-react-app
npm install
npm run dev
```

### App.jsx - 기본 템플릿
```jsx
import { useState } from 'react'
import './App.css'

function App() {
  const [input, setInput] = useState('')
  const [result, setResult] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    // API 호출 또는 처리 로직
    setResult(`처리 결과: ${input}`)
  }

  return (
    <div className="app-container">
      <h1>AI_100 데모 앱</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="입력하세요"
          className="input-field"
        />
        <button type="submit" className="submit-btn">
          실행
        </button>
      </form>

      {result && (
        <div className="result-box">
          <h2>결과</h2>
          <p>{result}</p>
        </div>
      )}
    </div>
  )
}

export default App
```

---

## 2. Next.js 앱

### 빠른 시작
```bash
npx create-next-app@latest my-next-app
cd my-next-app
npm run dev
```

### app/page.tsx - 메인 페이지
```tsx
'use client'

import { useState } from 'react'

export default function Home() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)

  const fetchData = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: 'test' })
      })
      const result = await response.json()
      setData(result)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen p-8">
      <h1 className="text-4xl font-bold mb-8">AI_100 Next.js 앱</h1>

      <button
        onClick={fetchData}
        disabled={loading}
        className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600"
      >
        {loading ? '처리 중...' : '데이터 가져오기'}
      </button>

      {data && (
        <div className="mt-8 p-6 bg-gray-100 rounded-lg">
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </main>
  )
}
```

### app/api/process/route.ts - API 라우트
```typescript
import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  const body = await request.json()

  // AI 처리 로직 (예: OpenAI API 호출)
  const result = {
    input: body.input,
    output: `처리된 결과: ${body.input}`,
    timestamp: new Date().toISOString()
  }

  return NextResponse.json(result)
}
```

---

## 3. Vue 3 앱

### 빠른 시작
```bash
npm create vue@latest my-vue-app
cd my-vue-app
npm install
npm run dev
```

### App.vue
```vue
<template>
  <div class="app">
    <h1>AI_100 Vue 앱</h1>

    <div class="input-section">
      <input
        v-model="inputText"
        @keyup.enter="processInput"
        placeholder="입력하세요"
      />
      <button @click="processInput">실행</button>
    </div>

    <div v-if="result" class="result">
      <h2>결과</h2>
      <p>{{ result }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const inputText = ref('')
const result = ref('')

const processInput = () => {
  // 처리 로직
  result.value = `처리 결과: ${inputText.value}`
}
</script>

<style scoped>
.app {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.input-section {
  display: flex;
  gap: 10px;
  margin: 20px 0;
}

input {
  flex: 1;
  padding: 10px;
  font-size: 16px;
}

button {
  padding: 10px 20px;
  background: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}
</style>
```

---

## 4. 애니메이션 효과

### Framer Motion (React)
```jsx
import { motion } from 'framer-motion'

function AnimatedComponent() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h1>애니메이션 제목</h1>
    </motion.div>
  )
}

// 리스트 애니메이션
function AnimatedList({ items }) {
  return (
    <motion.ul>
      {items.map((item, index) => (
        <motion.li
          key={item.id}
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: index * 0.1 }}
        >
          {item.text}
        </motion.li>
      ))}
    </motion.ul>
  )
}
```

### GSAP 애니메이션
```jsx
import { useEffect, useRef } from 'react'
import gsap from 'gsap'

function GSAPAnimation() {
  const boxRef = useRef(null)

  useEffect(() => {
    gsap.to(boxRef.current, {
      x: 300,
      rotation: 360,
      duration: 2,
      ease: 'bounce.out'
    })
  }, [])

  return <div ref={boxRef} className="box">애니메이션</div>
}
```

---

## 5. 차트 및 데이터 시각화

### Chart.js with React
```jsx
import { Line, Bar, Pie } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
)

function DataChart() {
  const data = {
    labels: ['1월', '2월', '3월', '4월', '5월'],
    datasets: [
      {
        label: '데이터셋 1',
        data: [12, 19, 3, 5, 2],
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
      }
    ]
  }

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'AI_100 데이터 시각화'
      }
    }
  }

  return (
    <div>
      <Line data={data} options={options} />
      <Bar data={data} options={options} />
    </div>
  )
}
```

### Recharts (더 간단한 대안)
```jsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

function SimpleChart() {
  const data = [
    { name: 'A', value: 400 },
    { name: 'B', value: 300 },
    { name: 'C', value: 600 },
  ]

  return (
    <LineChart width={600} height={300} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line type="monotone" dataKey="value" stroke="#8884d8" />
    </LineChart>
  )
}
```

---

## 6. AI 챗봇 UI

### React 챗봇 컴포넌트
```jsx
import { useState } from 'react'
import axios from 'axios'

function ChatBot() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      // OpenAI API 호출 예시
      const response = await axios.post('/api/chat', {
        message: input
      })

      const botMessage = { role: 'assistant', content: response.data.reply }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chatbot-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <div className="avatar">
              {msg.role === 'user' ? '👤' : '🤖'}
            </div>
            <div className="content">{msg.content}</div>
          </div>
        ))}
        {loading && (
          <div className="message assistant">
            <div className="avatar">🤖</div>
            <div className="content typing">생각 중...</div>
          </div>
        )}
      </div>

      <form onSubmit={sendMessage} className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="메시지를 입력하세요..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          전송
        </button>
      </form>
    </div>
  )
}

export default ChatBot
```

---

## 7. 파일 업로드 UI

### React Dropzone
```jsx
import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'

function FileUpload() {
  const onDrop = useCallback((acceptedFiles) => {
    // 파일 처리 로직
    acceptedFiles.forEach((file) => {
      const reader = new FileReader()

      reader.onload = () => {
        // 파일 내용 처리
        console.log(reader.result)
      }

      reader.readAsDataURL(file)
    })
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg'],
      'text/csv': ['.csv'],
      'application/json': ['.json']
    }
  })

  return (
    <div {...getRootProps()} className="dropzone">
      <input {...getInputProps()} />
      {isDragActive ? (
        <p>파일을 여기에 놓으세요...</p>
      ) : (
        <p>파일을 드래그하거나 클릭하여 업로드하세요</p>
      )}
    </div>
  )
}
```

---

## 8. 실시간 데이터 대시보드

### React with Socket.io
```jsx
import { useEffect, useState } from 'react'
import io from 'socket.io-client'

function RealtimeDashboard() {
  const [data, setData] = useState([])
  const [socket, setSocket] = useState(null)

  useEffect(() => {
    const newSocket = io('http://localhost:3001')
    setSocket(newSocket)

    newSocket.on('data-update', (newData) => {
      setData(prev => [...prev, newData].slice(-50)) // 최근 50개만 유지
    })

    return () => newSocket.close()
  }, [])

  return (
    <div className="dashboard">
      <h1>실시간 데이터 대시보드</h1>

      <div className="metrics">
        <div className="metric-card">
          <h3>총 데이터</h3>
          <p className="metric-value">{data.length}</p>
        </div>

        <div className="metric-card">
          <h3>최신 값</h3>
          <p className="metric-value">
            {data[data.length - 1]?.value || 'N/A'}
          </p>
        </div>
      </div>

      <div className="data-list">
        {data.map((item, index) => (
          <div key={index} className="data-item">
            {JSON.stringify(item)}
          </div>
        ))}
      </div>
    </div>
  )
}
```

---

## Tailwind CSS 설정

### tailwind.config.js
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        secondary: '#8b5cf6',
      }
    },
  },
  plugins: [],
}
```

### CSS 기본 스타일
```css
/* index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  .btn-primary {
    @apply bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition;
  }

  .card {
    @apply bg-white shadow-lg rounded-lg p-6;
  }

  .input-field {
    @apply border-2 border-gray-300 rounded-lg px-4 py-2 focus:border-blue-500 focus:outline-none;
  }
}
```

---

## 빠른 프로젝트 시작 명령어

### React + Vite + Tailwind
```bash
npm create vite@latest my-app -- --template react
cd my-app
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install axios framer-motion react-chartjs-2 chart.js
npm run dev
```

### Next.js + TypeScript + Tailwind
```bash
npx create-next-app@latest my-next-app --typescript --tailwind --app
cd my-next-app
npm install axios swr
npm run dev
```

### 필수 라이브러리만 빠르게 설치
```bash
npm install react react-dom
npm install axios
npm install framer-motion
npm install tailwindcss
npm install react-chartjs-2 chart.js
```

---

## 대회 팁

1. **빠른 프로토타이핑**: Vite + React가 가장 빠름
2. **풀스택 필요시**: Next.js 사용 (API 라우트 포함)
3. **애니메이션**: Framer Motion이 가장 직관적
4. **차트**: Recharts가 가장 간단, Chart.js가 기능 많음
5. **스타일링**: Tailwind CSS로 빠르게 UI 구성
6. **상태관리**: 간단한 경우 useState, 복잡하면 Zustand

행운을 빕니다! 🚀
