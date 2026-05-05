import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import DashboardLayout from '../components/DashboardLayout';
import { mt5Api } from '../services/api';

export default function Positions() {
  const [positions, setPositions] = useState<any[]>([]);
  const [accountId, setAccountId] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => { load(); }, []);

  const load = async () => {
    try {
      const accs = await mt5Api.listAccounts();
      if (!accs.data[0]) return;
      setAccountId(accs.data[0].id);
      const res = await mt5Api.getPositions(accs.data[0].id);
      setPositions(res.data);
    } finally {
      setLoading(false);
    }
  };

  const closePosition = async (ticket: number) => {
    if (!confirm('هل تريد إغلاق هذه الصفقة؟')) return;
    try {
      await mt5Api.closePosition(accountId, ticket);
      toast.success('تم إغلاق الصفقة');
      load();
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'فشل الإغلاق');
    }
  };

  return (
    <DashboardLayout>
      <h1 style={{ fontSize: 28, marginBottom: 24 }}>الصفقات المفتوحة</h1>
      <div className="card">
        {loading ? (
          <p style={{ textAlign: 'center', padding: 40, color: 'var(--color-text-muted)' }}>
            جاري التحميل...
          </p>
        ) : positions.length === 0 ? (
          <p style={{ textAlign: 'center', padding: 40, color: 'var(--color-text-muted)' }}>
            لا توجد صفقات مفتوحة
          </p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>الرقم</th>
                <th>الرمز</th>
                <th>النوع</th>
                <th>الحجم</th>
                <th>الفتح</th>
                <th>الحالي</th>
                <th>الربح</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {positions.map((p) => (
                <tr key={p.ticket}>
                  <td><span className="num">#{p.ticket}</span></td>
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
                  <td>
                    <button onClick={() => closePosition(p.ticket)} className="btn btn-danger btn-sm">
                      إغلاق
                    </button>
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
