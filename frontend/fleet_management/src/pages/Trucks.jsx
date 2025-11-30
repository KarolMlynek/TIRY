import { useEffect, useState } from 'react'
import axios from 'axios'
import useAuth from '../hooks/useAuth.js'
import TruckCard from '../components/TruckCard.jsx'

export default function Trucks() {
  const { token } = useAuth()
  const [trucks, setTrucks] = useState([])

  useEffect(() => {
    axios
      .get('/api/v1/trucks', {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setTrucks(res.data))
  }, [token])

  return (
    <div style={{ padding: 20 }}>
      <h2>Lista ciężarówek</h2>
      {trucks.map((t) => (
        <TruckCard key={t.id} truck={t} />
      ))}
    </div>

  )
}
