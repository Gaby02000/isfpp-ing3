import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Plantilla from './components/Layout/Plantilla';
import Home from './pages/Home/Home';
import Gestion from './pages/Gestion/Gestion';
import Mozos from './pages/Mozos/Mozos';
import Mesas from './pages/Mesas/Mesas';
import Sectores from './pages/Sectores/Sectores';
import Productos from './pages/Productos/Productos';
import Secciones from './pages/Secciones/Secciones';
import MedioPagos from './pages/MedioPagos/MedioPagos';
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