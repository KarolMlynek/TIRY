import { useEffect, useState } from 'react'
import axios from 'axios'
import useAuth from '../hooks/useAuth.js'
import DriverCard from '../components/DriverCard.jsx'

export default function Drivers() {
  const { token } = useAuth()
  const [drivers, setDrivers] = useState([])
  const [trucks, setTrucks] = useState([])

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [form, setForm] = useState({ full_name:'', license_number:'', phone:'', company_id:'' })
  const [creating, setCreating] = useState(false)

  const [selectingDriver, setSelectingDriver] = useState(null)

  const headers = token ? { Authorization: `Bearer ${token}` } : {}

  useEffect(() => {
    if (!token) return
    setLoading(true)
    axios.get('/api/v1/drivers/', { headers })
      .then(res => setDrivers(res.data || []))
      .catch(() => setError('Błąd pobierania kierowców'))
      .finally(() => setLoading(false))
  }, [token])

  useEffect(() => {
    if (!token) return
    axios.get('/api/v1/trucks/', { headers })
      .then(res => setTrucks(res.data || []))
      .catch(() => console.warn("Nie udało się pobrać ciężarówek"))
  }, [token])


  const handleChange = e => setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))

  const handleCreate = async e => {
    e.preventDefault()
    if (!form.full_name) return alert('Podaj imię i nazwisko')
    setCreating(true)
    try {
      const payload = { 
        full_name: form.full_name,
        license_number: form.license_number || null,
        phone: form.phone || null,
        company_id: form.company_id ? Number(form.company_id) : null
      }
      const res = await axios.post('/api/v1/drivers/', payload, { headers })
      setDrivers(prev => [res.data, ...prev])
      setForm({ full_name:'', license_number:'', phone:'', company_id:'' })
    } catch {
      alert('Nie udało się dodać kierowcy')
    } finally {
      setCreating(false)
    }
  }


  const assignTruck = async (driverId, truckId) => {
    if (!truckId) return
    try {
      await axios.post(`/api/v1/drivers/${driverId}/assign_truck/${truckId}`, {}, { headers })
      setDrivers(prev =>
        prev.map(d => d.id === driverId ? { ...d, truck_id: Number(truckId) } : d)
      )
    } catch {
      alert("Nie udało się przypisać ciężarówki")
    }
    setSelectingDriver(null)
  }

  const unassignTruck = async (driverId) => {
    try {
      await axios.post(`/api/v1/drivers/${driverId}/remove_truck`, {}, { headers })
      setDrivers(prev =>
        prev.map(d => d.id === driverId ? { ...d, truck_id: null } : d)
      )
    } catch {
      alert("Nie udało się usunąć przypisania")
    }
  }


  return (
    <div className="container">
      <header className="header"><h1>Kierowcy</h1></header>

      <section>
        <h3>Dodaj nowego kierowcę</h3>
        <form onSubmit={handleCreate}>
          <input name="full_name" placeholder="Imię i nazwisko" value={form.full_name} onChange={handleChange}/>
          <input name="license_number" placeholder="Numer prawa jazdy" value={form.license_number} onChange={handleChange}/>
          <input name="phone" placeholder="Telefon" value={form.phone} onChange={handleChange}/>
          <input name="company_id" placeholder="ID firmy (opcjonalne)" value={form.company_id} onChange={handleChange}/>
          <button type="submit" disabled={creating}>{creating ? 'Dodawanie...' : 'Dodaj kierowcę'}</button>
        </form>
      </section>

      <section>
        <h3>Lista kierowców</h3>
        {loading ? <p>Ładowanie...</p> : error ? <p style={{color:'red'}}>{error}</p> :
          drivers.length === 0 ? <p>Brak zapisanych kierowców.</p> :
          <div className="grid">
            {drivers.map(d => (
              <DriverCard 
                key={d.id} 
                driver={d}
                onAssign={(driverId) => setSelectingDriver(driverId)}
                onUnassign={(driverId) => unassignTruck(driverId)}
              />
            ))}
          </div>
        }
      </section>

      {/* --- MODAL WYBORU CIĘŻARÓWKI --- */}
      {selectingDriver && (
        <div className="modal">
          <div className="modal-inner">
            <h3>Przypisz kierowcę do ciężarówki</h3>

            <select onChange={(e) => assignTruck(selectingDriver, e.target.value)}>
              <option value="">-- wybierz ciężarówkę --</option>
              {trucks.map(t => (
                <option key={t.id} value={t.id}>
                  {t.registration_number} (VIN: {t.vin})
                </option>
              ))}
            </select>

            <button onClick={() => setSelectingDriver(null)} style={{marginTop:'10px'}}>
              Anuluj
            </button>
          </div>
        </div>
      )}

    </div>
  )
}
