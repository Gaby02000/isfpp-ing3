import React, { useEffect, useState } from 'react';
import { Card, Row, Col, Button, Badge, Container } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { useReservaService } from '../../services/reservaService';
import Cargador from '../../components/common/Cargador';

const Home = () => {
  const navigate = useNavigate();
  const { getReservas, loading } = useReservaService();
  const [stats, setStats] = useState({
    reservasHoy: 0,
    loading: true
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        // Obtener reservas del día de hoy en horario de Argentina (UTC-3)
        // Función helper para obtener inicio y fin del día en horario argentino
        const getFechasArgentina = () => {
          const ahora = new Date();
          
          // Obtener fecha/hora actual en Argentina usando Intl.DateTimeFormat
          const formatter = new Intl.DateTimeFormat('en-CA', {
            timeZone: 'America/Argentina/Buenos_Aires',
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
          });
          
          // Obtener partes de la fecha en Argentina
          const partes = formatter.formatToParts(ahora);
          const year = parseInt(partes.find(p => p.type === 'year').value);
          const month = parseInt(partes.find(p => p.type === 'month').value) - 1; // Mes es 0-indexed
          const day = parseInt(partes.find(p => p.type === 'day').value);
          
          // Crear fecha de inicio del día (00:00:00) en Argentina
          // Argentina está en UTC-3, así que 00:00 ARG = 03:00 UTC
          const inicioDia = new Date(Date.UTC(year, month, day, 3, 0, 0));
          
          // Crear fecha de fin del día (23:59:59) en Argentina
          // 23:59:59 ARG = 02:59:59 UTC del día siguiente
          const finDia = new Date(Date.UTC(year, month, day, 2, 59, 59));
          finDia.setUTCDate(finDia.getUTCDate() + 1);
          
          return { inicioDia, finDia };
        };
        
        const { inicioDia, finDia } = getFechasArgentina();
        
        // Convertir a ISO para enviar al backend
        const fechaDesde = inicioDia.toISOString();
        const fechaHasta = finDia.toISOString();
        
        const response = await getReservas({
          cancelado: 'activo',
          fecha_desde: fechaDesde,
          fecha_hasta: fechaHasta
        });
        
        const reservasData = response.data || [];
        setStats({
          reservasHoy: Array.isArray(reservasData) ? reservasData.length : 0,
          loading: false
        });
      } catch (error) {
        setStats({ reservasHoy: 0, loading: false });
      }
    };
    fetchStats();
  }, [getReservas]);

  const quickActions = [
    {
      title: 'Gestión',
      description: 'Accede a las diferentes áreas de gestión del sistema',
      icon: '⚙️',
      path: '/gestion',
      variant: 'primary'
    }
  ];

  return (
    <Container fluid className="py-4">
      <Row className="mb-4">
        <Col>
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <h1 className="display-4 mb-2">Panel de Administración</h1>
              <p className="lead text-muted">
                Sistema de Gestión de Mozos - UNPSJB
              </p>
            </div>
          </div>
        </Col>
      </Row>

      <Row className="mb-4">
        <Col md={4}>
          <Card className="shadow-sm border-0 border-start border-4 border-warning">
            <Card.Body>
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h6 className="text-muted text-uppercase mb-2">Reservas Hoy</h6>
                  {stats.loading ? (
                    <Cargador size="sm" />
                  ) : (
                    <h2 className="mb-0 text-warning">{stats.reservasHoy}</h2>
                  )}
                  <small className="text-muted">Reservas activas para hoy</small>
                </div>
                <div className="text-warning" style={{ fontSize: '3rem' }}>
                  📅
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={4}>
          <Card className="shadow-sm border-0 bg-primary text-white">
            <Card.Body>
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h6 className="text-white-50 text-uppercase mb-2">Sistema Activo</h6>
                  <h2 className="mb-0">Operativo</h2>
                </div>
                <div style={{ fontSize: '3rem' }}>
                  ✅
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={4}>
          <Card className="shadow-sm border-0 bg-success text-white">
            <Card.Body>
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h6 className="text-white-50 text-uppercase mb-2">Última Actualización</h6>
                  <h6 className="mb-0">Hoy</h6>
                </div>
                <div style={{ fontSize: '3rem' }}>
                  📊
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="mb-4">
        <Col>
          <h3 className="mb-4">Acciones Rápidas</h3>
        </Col>
      </Row>
      <Row>
        {quickActions.map((action, index) => (
          <Col md={6} lg={3} key={index} className="mb-4">
            <Card 
              className="shadow-sm border-0 h-100 hover-card"
              style={{ transition: 'transform 0.2s', cursor: 'pointer' }}
              onClick={() => navigate(action.path)}
            >
              <Card.Body className="d-flex flex-column">
                <div className="text-center mb-3">
                  <div style={{ fontSize: '3rem' }}>{action.icon}</div>
                </div>
                <Card.Title className="text-center">
                  <div className="mb-2">
                    {action.title}
                    {action.badge !== undefined && (
                      <Badge bg={action.variant} className="ms-2">
                        {action.badge}
                      </Badge>
                    )}
                  </div>
                  {action.subtitle && (
                    <div>
                      <small className="text-muted d-block">{action.subtitle}</small>
                    </div>
                  )}
                </Card.Title>
                <Card.Text className="text-muted text-center flex-grow-1">
                  {action.description}
                </Card.Text>
                <Button 
                  variant={action.variant} 
                  as={Link} 
                  to={action.path}
                  className="w-100"
                >
                  Acceder
                </Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      <Row className="mt-5">
        <Col>
          <Card className="shadow-sm border-0 bg-light">
            <Card.Body className="p-4">
              <h4 className="mb-3">Bienvenido al Sistema de Gestión</h4>
              <p className="mb-2">
                Este sistema permite gestionar de manera eficiente todos los mozos del establecimiento.
              </p>
              <p className="mb-0">
                Utiliza el menú de navegación o las acciones rápidas para acceder a las diferentes funcionalidades.
              </p>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Home;

