import { useEffect, useState } from 'react';
import DashboardLayout from '../components/DashboardLayout';
import { analyticsApi, mt5Api } from '../services/api';

export default function Analytics() {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { load(); }, []);

  const load = async () => {
    try {
      const accs = await mt5Api.listAccounts();
      if (!accs.data[0]) return;
      const res = await analyticsApi.getPerformance(accs.data[0].id, 30);
      setStats(res.data);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <p style={{ textAlign: 'center', padding: 40 }}>جاري التحميل...</p>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <h1 style={{ fontSize: 28, marginBottom: 24 }}>تحليل الأداء (آخر 30 يوم)</h1>
      <div className="grid grid-4" style={{ marginBottom: 24 }}>
        <div className="stat-card">
          <div className="stat-label">إجمالي الصفقات</div>
          <div className="stat-value"><span className="num">{stats?.total_trades || 0}</span></div>
        </div>
        <div className="stat-card">
          <div className="stat-label">معدل النجاح</div>
          <div className="stat-value price-up"><span className="num">{stats?.win_rate || 0}%</span></div>
        </div>
        <div className="stat-card">
          <div className="stat-label">صافي الربح</div>
          <div className={`stat-value ${(stats?.net_profit || 0) >= 0 ? 'price-up' : 'price-down'}`}>
            <span className="num">${stats?.net_profit?.toFixed(2) || '0.00'}</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-label">عامل الربح</div>
          <div className="stat-value"><span className="num">{stats?.profit_factor?.toFixed(2) || 0}</span></div>
        </div>
      </div>

      <div className="grid grid-2">
        <div className="card">
          <h3 style={{ marginBottom: 16 }}>الصفقات الرابحة</h3>
          <div className="stat-value price-up" style={{ marginBottom: 8 }}>
            <span className="num">{stats?.winning_trades || 0}</span>
          </div>
          <p style={{ color: 'var(--color-text-muted)' }}>
            متوسط الربح: <span className="num price-up">${stats?.average_win?.toFixed(2) || '0.00'}</span>
          </p>
        </div>
        <div className="card">
          <h3 style={{ marginBottom: 16 }}>الصفقات الخاسرة</h3>
          <div className="stat-value price-down" style={{ marginBottom: 8 }}>
            <span className="num">{stats?.losing_trades || 0}</span>
          </div>
          <p style={{ color: 'var(--color-text-muted)' }}>
            متوسط الخسارة: <span className="num price-down">${stats?.average_loss?.toFixed(2) || '0.00'}</span>
          </p>
        </div>
      </div>
    </DashboardLayout>
  );
}
