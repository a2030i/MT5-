import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../services/auth';

interface Props {
  children: React.ReactNode;
}

const NAV = [
  { to: '/dashboard', icon: '📊', label: 'لوحة التحكم' },
  { to: '/trade', icon: '💹', label: 'تداول' },
  { to: '/positions', icon: '📈', label: 'الصفقات المفتوحة' },
  { to: '/history', icon: '📜', label: 'سجل الصفقات' },
  { to: '/analytics', icon: '📉', label: 'تحليل الأداء' },
  { to: '/settings', icon: '⚙️', label: 'الإعدادات' },
];

export default function DashboardLayout({ children }: Props) {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <>
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/dashboard" className="logo">
            <div className="logo-icon">م</div>
            <span>مُرشد</span>
          </Link>
          <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
            <span className="badge badge-success">
              <span className="live-dot"></span>متصل بـ MT5
            </span>
            <span style={{ color: 'var(--color-text-muted)', fontSize: 14 }}>
              {user?.full_name || 'المستخدم'}
            </span>
            <button onClick={handleLogout} className="btn btn-ghost btn-sm">خروج</button>
          </div>
        </div>
      </nav>

      <div className="dashboard-layout">
        <aside className="sidebar">
          {NAV.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className={`sidebar-link ${pathname === item.to ? 'active' : ''}`}
            >
              <span style={{ fontSize: 20 }}>{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          ))}
        </aside>
        <main className="dashboard-content">{children}</main>
      </div>
    </>
  );
}
