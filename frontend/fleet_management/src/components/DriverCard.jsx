export default function DriverCard({ driver, onAssign, onUnassign }) {
  return (
    <div className="card">
      <strong>{driver.full_name}</strong>

      <div>
        {driver.license_number
          ? `Prawo jazdy: ${driver.license_number}`
          : 'Brak numeru prawa jazdy'}
      </div>

      {driver.phone && <div>Telefon: {driver.phone}</div>}
      {driver.company_id && (
        <div style={{ fontSize: '12px', color: '#555' }}>
          Firma ID: {driver.company_id}
        </div>
      )}

      {/* Jeśli kierowca ma przypisaną ciężarówkę → pokaż dane ciężarówki */}
      {driver.truck ? (
        <>
          <div style={{ marginTop: '10px' }}>
            <strong>Przypisany do ciężarówki:</strong><br />
            Tablica: {driver.truck.registration_number}<br /> 
            Marka: {driver.truck.brand || '—'}<br /> 
            Model: {driver.truck.model || '—'}<br /> 
            VIN: {driver.truck.vin}
          </div>

          <button
            onClick={() => onUnassign(driver.id)}
            style={{ marginTop: '10px' }}
          >
            Usuń przypisanie
          </button>
        </>
      ) : (
        <button
          onClick={() => onAssign(driver.id)}
          style={{ marginTop: '10px' }}
        >
          Przypisz do ciężarówki
        </button>
      )}
    </div>
  );
}
