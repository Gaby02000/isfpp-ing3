import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import GestionMozos from './components/Mozos/GestionMozos';
import AltaMozo from './components/Mozos/AltaMozo';
import 'bootstrap/dist/css/bootstrap.min.css';

// Placeholder components for Baja and Modificar
const BajaMozo = () => (
  <div className="container mt-4">
    <h2>Baja de Mozo</h2>
    <div className="alert alert-info">Funcionalidad en desarrollo</div>
  </div>
);

const ModificarMozo = () => (
  <div className="container mt-4">
    <h2>Modificar Mozo</h2>
    <div className="alert alert-info">Funcionalidad en desarrollo</div>
  </div>
);

const Home = () => (
  <div className="jumbotron mt-4">
    <h1 className="display-4">Sistemas Distribuidos</h1>
    <p className="lead">Microservicio ejemplo: panel de administración.</p>
    <hr className="my-4" />
  </div>
);

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/gestion-mozos" element={<GestionMozos />} />
          <Route path="/alta-mozo" element={<AltaMozo />} />
          <Route path="/baja-mozo" element={<BajaMozo />} />
          <Route path="/modificar-mozo" element={<ModificarMozo />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;