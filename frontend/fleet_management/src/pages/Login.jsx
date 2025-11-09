import { useState } from 'react'
import axios from 'axios'
import useAuth from '../hooks/useAuth.js'

export default function Login() {
  const { login } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const data = new URLSearchParams()
      data.append('username', email)
      data.append('password', password)
      const res = await axios.post('/api/v1/auth/token', data, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      })
      login(res.data.access_token)
      window.location.href = '/'
    } catch (err) {
      setError('Nieprawidłowe dane logowania')
    }
  }

  return (
    <div style={{ padding: 40 }}>
      <h2>Logowanie</h2>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <br />
        <input
          placeholder="Hasło"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <br />
        <button type="submit">Zaloguj</button>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </form>
    </div>
  )
}
