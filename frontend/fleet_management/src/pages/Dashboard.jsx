import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import useAuth from '../hooks/useAuth.js'

export default function Dashboard() {
  const { token, logout } = useAuth()
  const [trucksCount, setTrucksCount] = useState(null)
  const [driversCount, setDriversCount] = useState(null)
  const [loading, setLoading] = useState(true)
   const [stats, setStats] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!token) return
    setLoading(true)
    api.get('/stats/', { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setStats(res.data))
      .catch(() => setError('Błąd pobierania statystyk'))
      .finally(() => setLoading(false))

    const headers = { Authorization: `Bearer ${token}` }
    const tReq = axios.get('/api/v1/trucks/', { headers })
    const dReq = axios.get('/api/v1/drivers/', { headers })

    Promise.all([tReq, dReq])
      .then(([tRes, dRes]) => {
        setTrucksCount(Array.isArray(tRes.data) ? tRes.data.length : 0)
        setDriversCount(Array.isArray(dRes.data) ? dRes.data.length : 0)
      })
      .catch((err) => {
        console.error(err)
        setError('Błąd podczas pobierania danych. Sprawdź backend i token.')
      })
      .finally(() => setLoading(false))
  }, [token])
  if (!token) return <div>Zaloguj się</div>
  
  return (
    <div style={{ padding: 20 }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Dashboard floty</h1>
        <div>
          <Link to="/trucks" style={{ marginRight: 12 }}>Ciężarówki</Link>
          <Link to="/drivers" style={{ marginRight: 12 }}>Kierowcy</Link>
          <button onClick={() => { logout(); window.location.href = '/login' }}>Wyloguj</button>
        </div>
      </header>

      {loading ? (
        <p>Ładowanie danych...</p>
      ) : error ? (
        <p style={{ color: 'red' }}>{error}</p>
      ) : (
        <section style={{ marginTop: 20, display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 16 }}>
          <div style={{ border: '1px solid #ddd', borderRadius: 8, padding: 16 }}>
            <h3>Łączna liczba pojazdów</h3>
            <p style={{ fontSize: 28, margin: '8px 0' }}>{trucksCount}</p>
            <small>Aktywne wpisy w systemie</small>
          </div>

          <div style={{ border: '1px solid #ddd', borderRadius: 8, padding: 16 }}>
            <h3>Łączna liczba kierowców</h3>
            <p style={{ fontSize: 28, margin: '8px 0' }}>{driversCount}</p>
            <small>Przypisani do firm / floty</small>
          </div>

          <div style={{ border: '1px solid #ddd', borderRadius: 8, padding: 16 }}>
            <h3>Akcje</h3>
            <p>
              <Link to="/trucks">Zarządzaj ciężarówkami</Link><br/>
              <Link to="/drivers">Zarządzaj kierowcami</Link>
            </p>
            <small>Dodawaj, edytuj lub przeglądaj szczegóły</small>
          </div>
        </section>
      )}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {stats && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 12 }}>
          <div style={{ padding:12, border:'1px solid #ddd', borderRadius:8 }}>
            <h3>Pojazdy</h3>
            <p style={{ fontSize:24 }}>{stats.trucks_count}</p>
            <Link to="/trucks">Zarządzaj</Link>
          </div>
          <div style={{ padding:12, border:'1px solid #ddd', borderRadius:8 }}>
            <h3>Kierowcy</h3>
            <p style={{ fontSize:24 }}>{stats.drivers_count}</p>
            <Link to="/drivers">Zarządzaj</Link>
          </div>
          <div style={{ padding:12, border:'1px solid #ddd', borderRadius:8 }}>
            <h3>Nadchodzące przeglądy (7d)</h3>
            <p style={{ fontSize:24 }}>{stats.upcoming_maintenances_7d}</p>
            <Link to="/maintenance">Kalendarz serwisów</Link>
          </div>
          <div style={{ padding:12, border:'1px solid #ddd', borderRadius:8 }}>
            <h3>Zaległe serwisy</h3>
            <p style={{ fontSize:24 }}>{stats.overdue_maintenances}</p>
          </div>
        </div>
      )}

      <footer style={{ marginTop: 24, color: '#666' }}>
        <small>Demo — Fleet Management</small>
      </footer>
    </div>
  )
}
