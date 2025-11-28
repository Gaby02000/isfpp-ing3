import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Plantilla from './components/Layout/Plantilla';
import Home from './pages/Home/Home';
import Gestion from './pages/Gestion/Gestion';
import Mozos from './pages/Mozos/Mozos';
import Mesas from './pages/Mesas/Mesas';
import Sectores from './pages/Sectores/Sectores';
import Clientes from './pages/Clientes/Clientes';
import Productos from './pages/Productos/Productos';
import Secciones from './pages/Secciones/Secciones';
import MedioPagos from './pages/MedioPagos/MedioPagos';
import Reservas from './pages/Reservas/Reservas';
import Comandas from './pages/Comanda/Comandas';
import Pagos from './pages/Pagos/Pagos';
import Reportes from './pages/Reportes/Reportes';

import { useDocumentTitle } from './hooks/useDocumentTitle';
import 'bootstrap/dist/css/bootstrap.min.css';

function AppContent() {
  useDocumentTitle();
  
  return (
    <Plantilla>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/gestion" element={<Gestion />} />
        <Route path="/gestion/mozos" element={<Mozos />} />
        <Route path="/gestion/mesas" element={<Mesas />} />
        <Route path="/gestion/sectores" element={<Sectores />} />
        <Route path="/gestion/productos" element={<Productos />} />
        <Route path="/gestion/secciones" element={<Secciones/>} />
        <Route path="/gestion/medio-pagos" element={<MedioPagos />} />
        <Route path="/pagos" element={<Pagos />} />
        <Route path="/gestion/clientes" element={<Clientes />} />
        <Route path="/gestion/reservas" element={<Reservas />} />
        <Route path="/gestion/comandas" element={<Comandas />} />
                <Route path="/gestion/reportes" element={<Reportes />} />

        
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Plantilla>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
