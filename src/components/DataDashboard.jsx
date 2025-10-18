import { useState, useEffect } from 'react'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

/**
 * 데이터 대시보드 컴포넌트
 * AI_100 대회용 빠른 시작 템플릿
 */
function DataDashboard() {
  const [data, setData] = useState([])
  const [stats, setStats] = useState({
    total: 0,
    average: 0,
    max: 0,
    min: 0
  })

  // 랜덤 데이터 생성 (실제로는 API에서 가져오기)
  useEffect(() => {
    const interval = setInterval(() => {
      const newValue = Math.random() * 100
      const timestamp = new Date().toLocaleTimeString()

      setData(prev => {
        const newData = [...prev, { value: newValue, time: timestamp }].slice(-20)

        // 통계 계산
        const values = newData.map(d => d.value)
        setStats({
          total: values.length,
          average: (values.reduce((a, b) => a + b, 0) / values.length).toFixed(2),
          max: Math.max(...values).toFixed(2),
          min: Math.min(...values).toFixed(2)
        })

        return newData
      })
    }, 2000)

    return () => clearInterval(interval)
  }, [])

  const chartData = {
    labels: data.map(d => d.time),
    datasets: [
      {
        label: '실시간 데이터',
        data: data.map(d => d.value),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
        fill: true
      }
    ]
  }

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top'
      },
      title: {
        display: true,
        text: '실시간 데이터 모니터링'
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100
      }
    }
  }

  return (
    <div className="container-custom py-8">
      <h1 className="text-4xl font-bold mb-8 gradient-text">데이터 대시보드</h1>

      {/* 통계 카드 */}
      <div className="grid-responsive mb-8">
        <div className="card bg-gradient-to-br from-blue-500 to-blue-600 text-white animate-scale-in">
          <div className="text-sm opacity-90">총 데이터 포인트</div>
          <div className="text-3xl font-bold mt-2">{stats.total}</div>
        </div>

        <div className="card bg-gradient-to-br from-green-500 to-green-600 text-white animate-scale-in" style={{ animationDelay: '0.1s' }}>
          <div className="text-sm opacity-90">평균 값</div>
          <div className="text-3xl font-bold mt-2">{stats.average}</div>
        </div>

        <div className="card bg-gradient-to-br from-purple-500 to-purple-600 text-white animate-scale-in" style={{ animationDelay: '0.2s' }}>
          <div className="text-sm opacity-90">최대 값</div>
          <div className="text-3xl font-bold mt-2">{stats.max}</div>
        </div>

        <div className="card bg-gradient-to-br from-orange-500 to-orange-600 text-white animate-scale-in" style={{ animationDelay: '0.3s' }}>
          <div className="text-sm opacity-90">최소 값</div>
          <div className="text-3xl font-bold mt-2">{stats.min}</div>
        </div>
      </div>

      {/* 차트 */}
      <div className="card animate-fade-in">
        <Line data={chartData} options={chartOptions} />
      </div>

      {/* 데이터 테이블 */}
      <div className="card mt-8 animate-slide-up">
        <h2 className="card-header">최근 데이터</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  시간
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  값
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  상태
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {data.slice(-10).reverse().map((item, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {item.time}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {item.value.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`badge ${
                      item.value > 75 ? 'badge-success' :
                      item.value > 50 ? 'badge-warning' :
                      'badge-danger'
                    }`}>
                      {item.value > 75 ? '높음' : item.value > 50 ? '보통' : '낮음'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default DataDashboard
