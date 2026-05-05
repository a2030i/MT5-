import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import DashboardLayout from '../components/DashboardLayout';
import { mt5Api } from '../services/api';

export default function Dashboard() {
  const navigate = useNavigate();
  const [accounts, setAccounts] = useState<any[]>([]);
  const [info, setInfo] = useState<any>(null);
  const [positions, setPositions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const accs = await mt5Api.listAccounts();
      setAccounts(accs.data);

      if (accs.data.length === 0) {
        navigate('/connect-mt5');
        return;
      }

      const accountId = accs.data[0].id;
      const [infoRes, posRes] = await Promise.all([
        mt5Api.getInfo(accountId),
        mt5Api.getPositions(accountId),
      ]);
      setInfo(infoRes.data);
      setPositions(posRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div style={{ textAlign: 'center', padding: 60 }}>
          <p style={{ color: 'var(--color-text-muted)' }}>جاري التحميل...</p>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <h1 style={{ fontSize: 28, marginBottom: 4 }}>مرحباً بك 👋</h1>
      <p style={{ color: 'var(--color-text-muted)', marginBottom: 32 }}>إليك ملخص حسابك</p>

      <div className="grid grid-4" style={{ marginBottom: 32 }}>
        <div className="stat-card">
          <div className="stat-label">الرصيد الحالي</div>
          <div className="stat-value">
            <span className="num">${info?.balance?.toFixed(2) || '0.00'}</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-label">الإيكويتي</div>
          <div className="stat-value">
            <span className="num">${info?.equity?.toFixed(2) || '0.00'}</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-label">الهامش الحر</div>
          <div className="stat-value">
            <span className="num">${info?.free_margin?.toFixed(2) || '0.00'}</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-label">الربح/الخسارة</div>
          <div className={`stat-value ${(info?.profit || 0) >= 0 ? 'price-up' : 'price-down'}`}>
            <span className="num">${info?.profit?.toFixed(2) || '0.00'}</span>
          </div>
        </div>
      </div>

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 20 }}>
          <h2 style={{ fontSize: 18 }}>الصفقات المفتوحة ({positions.length})</h2>
        </div>
        {positions.length === 0 ? (
          <p style={{ color: 'var(--color-text-muted)', textAlign: 'center', padding: 40 }}>
            لا توجد صفقات مفتوحة حالياً
          </p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>الرمز</th>
                <th>النوع</th>
                <th>الحجم</th>
                <th>سعر الفتح</th>
                <th>السعر الحالي</th>
                <th>الربح/الخسارة</th>
              </tr>
            </thead>
            <tbody>
              {positions.map((p) => (
                <tr key={p.ticket}>
                  <td><strong>{p.symbol}</strong></td>
                  <td>
                    <span className={p.type === 'BUY' ? 'badge badge-success' : 'badge badge-danger'}>
                      {p.type === 'BUY' ? 'شراء' : 'بيع'}
                    </span>
                  </td>
                  <td><span className="num">{p.volume}</span></td>
                  <td><span className="num">{p.open_price}</span></td>
                  <td><span className="num">{p.current_price}</span></td>
                  <td className={p.profit >= 0 ? 'price-up' : 'price-down'}>
                    <strong className="num">${p.profit.toFixed(2)}</strong>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </DashboardLayout>
  );
}
