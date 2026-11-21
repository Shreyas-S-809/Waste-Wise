import { Outlet, useLocation } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';

export default function AppLayout() {
  const location = useLocation();

  return (
    <div className="app-shell">
      <Sidebar />
      <div className="main-viewport">
        <Header />
        <main className="app-workspace">
          <div
            key={location.pathname}
            className="page-morph-enter"
            style={{ width: '100%', height: '100%', minHeight: 0, display: 'flex', flexDirection: 'column' }}
          >
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
