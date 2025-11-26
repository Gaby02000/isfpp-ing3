import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Card, Alert } from 'react-bootstrap';
import Cargador from '../../components/common/Cargador';
import { useReporteService } from '../../services/reporteService';

// Importar charts
import VentasMensualesChart from './components/VentasMensualesChart';
import ProductosMasVendidosChart from './components/ProductosMasVendidosChart';
import ReservasPorDiaChart from './components/ReservasPorDiaChart';
import PagosPorMedioChart from './components/PagosPorMedioChart';
import SectorUsoChart from './components/SectorUsoChart';
import MozoFacturacionChart from './components/MozoFacturacionChart';
import ReservasCanceladasChart from './components/ReservasCanceladasChart';

const Reportes = () => {
  const {
    getVentasMensuales,
    getProductosMasVendidos,
    getReservasPorDia,
    getMediosPago,
    getUsoSectores,
    getFacturacionMozos,
    loading
  } = useReporteService();

  const [ventasMensuales, setVentasMensuales] = useState([]);
  const [productosVendidos, setProductosVendidos] = useState([]);
  const [reservasDia, setReservasDia] = useState([]);
  const [mediosPago, setMediosPago] = useState([]);
  const [sectoresUso, setSectoresUso] = useState([]);
  const [facturacionMozos, setFacturacionMozos] = useState([]);
  const [alert, setAlert] = useState(null);

  useEffect(() => {
    loadReportes();
  }, []);

  const loadReportes = async () => {
    try {
      const [
        ventasResp,
        productosResp,
        reservasResp,
        mediosResp,
        sectoresResp,
        mozosResp
      ] = await Promise.all([
        getVentasMensuales(),
        getProductosMasVendidos(),
        getReservasPorDia(),
        getMediosPago(),
        getUsoSectores(),
        getFacturacionMozos()
      ]);

      setVentasMensuales(ventasResp.data || []);
      setProductosVendidos(productosResp.data || []);
      setReservasDia(reservasResp.data || []);
      setMediosPago(mediosResp.data || []);
      setSectoresUso(sectoresResp.data || []);
      setFacturacionMozos(mozosResp.data || []);
    } catch (error) {
      setAlert({ variant: 'danger', message: error.message || 'Error cargando reportes' });
    }
  };

  if (loading) return <Cargador />;

  return (
    <Container fluid className="py-4">
      <h2 className="mb-4">Dashboard de Reportes</h2>

      {alert && (
        <Alert variant={alert.variant} dismissible onClose={() => setAlert(null)}>
          {alert.message}
        </Alert>
      )}

      <Row className="mb-4">
        <Col md={6}>
          <Card>
            <Card.Header>Ventas Mensuales</Card.Header>
            <Card.Body>
              <VentasMensualesChart data={ventasMensuales} />
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card>
            <Card.Header>Productos Más Vendidos</Card.Header>
            <Card.Body>
              <ProductosMasVendidosChart data={productosVendidos} />
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="mb-4">
        <Col md={6}>
          <Card>
            <Card.Header>Reservas por Día</Card.Header>
            <Card.Body>
              <ReservasPorDiaChart data={reservasDia} />
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card>
            <Card.Header>Medios de Pago</Card.Header>
            <Card.Body>
              <PagosPorMedioChart data={mediosPago} />
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="mb-4">
        <Col md={6}>
          <Card>
            <Card.Header>Uso de Sectores</Card.Header>
            <Card.Body>
              <SectorUsoChart data={sectoresUso} />
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card>
            <Card.Header>Facturación de Mozos</Card.Header>
            <Card.Body>
              <MozoFacturacionChart data={facturacionMozos} />
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="mb-4">
        <Col md={12}>
          <Card>
            <Card.Header>Reservas Canceladas</Card.Header>
            <Card.Body>
              <ReservasCanceladasChart data={[]} /> {/* Aquí podés pasar datos reales si los agregás */}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Reportes;
