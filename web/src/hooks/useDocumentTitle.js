import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const pageTitles = {
  '/': 'Panel de Administración - UNPSJB',
  '/gestion': 'Panel de Gestión - UNPSJB',
  '/gestion/mesas': 'Gestión de Mesas - UNPSJB',
  '/gestion/mozos': 'Gestión de Mozos - UNPSJB',
  '/gestion/sectores': 'Gestión de Sectores - UNPSJB',
  '/gestion/productos': 'Gestión de Productos - UNPSJB',
  '/gestion/secciones': 'Gestión de Secciones - UNPSJB',
  '/gestion/medio-pagos': 'Medios de Pago - UNPSJB',
  '/gestion/clientes': 'Gestión de Clientes - UNPSJB'
};

export const useDocumentTitle = () => {
  const location = useLocation();

  useEffect(() => {
    const getPageTitle = () => {
      for (const [path, title] of Object.entries(pageTitles)) {
        if (location.pathname === path) {
          return title;
        }
        if (path !== '/' && location.pathname.startsWith(path)) {
          return title;
        }
      }
      return 'Sistema de Gestión - UNPSJB';
    };

    document.title = getPageTitle();
  }, [location.pathname]);
};

