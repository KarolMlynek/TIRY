import { Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Trucks from './pages/Trucks.jsx'
import Drivers from './pages/Drivers.jsx'
import useAuth from './hooks/useAuth.js'

export default function App() {
  const { token } = useAuth()

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      {token ? (
        <>
          <Route path="/" element={<Dashboard />} />
          <Route path="/trucks" element={<Trucks />} />
          <Route path="/drivers" element={<Drivers />} />
        </>
      ) : (
        <Route path="*" element={<Navigate to="/login" />} />
      )}
    </Routes>
  )
}
