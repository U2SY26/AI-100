import { useState, useRef, useEffect } from 'react'
import axios from 'axios'

/**
 * AI 챗봇 인터페이스 컴포넌트
 * AI_100 대회용 빠른 시작 템플릿
 */
function ChatInterface() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: '안녕하세요! 무엇을 도와드릴까요?' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  // 메시지가 추가될 때마다 스크롤 아래로
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      // API 호출 예시 - 실제 엔드포인트로 교체 필요
      const response = await axios.post('/api/chat', {
        message: input,
        history: messages
      })

      const botMessage = {
        role: 'assistant',
        content: response.data.reply || '응답을 생성할 수 없습니다.'
      }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Error:', error)
      const errorMessage = {
        role: 'assistant',
        content: '오류가 발생했습니다. 다시 시도해주세요.'
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const clearChat = () => {
    setMessages([
      { role: 'assistant', content: '대화가 초기화되었습니다. 다시 질문해주세요!' }
    ])
  }

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4">
      {/* 헤더 */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-6 rounded-t-lg shadow-lg">
        <h1 className="text-2xl font-bold">AI 챗봇</h1>
        <p className="text-sm opacity-90">AI_100 데모 인터페이스</p>
      </div>

      {/* 메시지 영역 */}
      <div className="flex-1 bg-white border-x border-gray-200 overflow-y-auto p-6 space-y-4">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}
          >
            <div className={`flex items-start max-w-xs lg:max-w-md ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
              {/* 아바타 */}
              <div className={`flex-shrink-0 ${msg.role === 'user' ? 'ml-3' : 'mr-3'}`}>
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white font-bold">
                  {msg.role === 'user' ? '👤' : '🤖'}
                </div>
              </div>

              {/* 메시지 버블 */}
              <div
                className={`px-4 py-3 rounded-2xl shadow-md ${
                  msg.role === 'user'
                    ? 'bg-blue-500 text-white rounded-tr-none'
                    : 'bg-gray-100 text-gray-800 rounded-tl-none'
                }`}
              >
                <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
              </div>
            </div>
          </div>
        ))}

        {/* 로딩 인디케이터 */}
        {loading && (
          <div className="flex justify-start animate-fade-in">
            <div className="flex items-start max-w-xs">
              <div className="mr-3">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white font-bold">
                  🤖
                </div>
              </div>
              <div className="px-4 py-3 rounded-2xl rounded-tl-none bg-gray-100">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* 입력 영역 */}
      <div className="bg-white border-x border-b border-gray-200 rounded-b-lg shadow-lg p-4">
        <form onSubmit={sendMessage} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="메시지를 입력하세요..."
            disabled={loading}
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors duration-200 font-semibold"
          >
            전송
          </button>
          <button
            type="button"
            onClick={clearChat}
            className="px-4 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors duration-200"
          >
            🗑️
          </button>
        </form>
      </div>
    </div>
  )
}

export default ChatInterface
