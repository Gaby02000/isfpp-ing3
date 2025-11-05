import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Plantilla from './components/Layout/Plantilla';
import Home from './pages/Home/Home';
import Gestion from './pages/Gestion/Gestion';
import Mozos from './pages/Mozos/Mozos';
import AltaMozo from './pages/Mozos/AltaMozo';
import BajaMozo from './pages/Mozos/BajaMozo';
import ModificarMozo from './pages/Mozos/ModificarMozo';
import Mesas from './pages/Mesas/Mesas';
import Sectores from './pages/Sectores/Sectores';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <Router>
      <Plantilla>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/gestion" element={<Gestion />} />
          <Route path="/gestion/mozos" element={<Mozos />} />
          <Route path="/gestion/mozos/alta" element={<AltaMozo />} />
          <Route path="/gestion/mozos/baja" element={<BajaMozo />} />
          <Route path="/gestion/mozos/modificar" element={<ModificarMozo />} />
          <Route path="/gestion/mesas" element={<Mesas />} />
          <Route path="/gestion/sectores" element={<Sectores />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Plantilla>
    </Router>
  );
}

export default App;