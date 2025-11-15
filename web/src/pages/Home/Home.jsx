import React, { useEffect, useState } from 'react';
import { Card, Row, Col, Button, Badge, Container } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { useMozoService } from '../../services/mozoService';
import Cargador from '../../components/common/Cargador';

const Home = () => {
  const navigate = useNavigate();
  const { getMozos, loading } = useMozoService();
  const [stats, setStats] = useState({
    totalMozos: 0,
    loading: true
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await getMozos();
        const mozosData = response.data || response;  // extraer data si existe, sino usar response directo
        setStats({
          totalMozos: Array.isArray(mozosData) ? mozosData.length : 0,
          loading: false
        });
      } catch (error) {
        setStats({ totalMozos: 0, loading: false });
      }
    };
    fetchStats();
  }, [getMozos]);

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
          <Card className="shadow-sm border-0">
            <Card.Body>
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h6 className="text-muted text-uppercase mb-2">Total Mozos</h6>
                  {stats.loading ? (
                    <Cargador size="sm" />
                  ) : (
                    <h2 className="mb-0">{stats.totalMozos}</h2>
                  )}
                </div>
                <div className="text-primary" style={{ fontSize: '3rem' }}>
                  👥
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

