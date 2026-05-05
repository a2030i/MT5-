import { useEffect, useState } from 'react';
import DashboardLayout from '../components/DashboardLayout';
import { mt5Api } from '../services/api';

export default function History() {
  const [trades, setTrades] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => { load(); }, []);

  const load = async () => {
    try {
      const accs = await mt5Api.listAccounts();
      if (!accs.data[0]) return;
      const res = await mt5Api.getHistory(accs.data[0].id, 30);
      setTrades(res.data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <h1 style={{ fontSize: 28, marginBottom: 24 }}>سجل الصفقات (آخر 30 يوم)</h1>
      <div className="card">
        {loading ? (
          <p style={{ textAlign: 'center', padding: 40 }}>جاري التحميل...</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>التاريخ</th>
                <th>الرمز</th>
                <th>النوع</th>
                <th>الحجم</th>
                <th>الفتح</th>
                <th>الإغلاق</th>
                <th>الربح</th>
              </tr>
            </thead>
            <tbody>
              {trades.map((t) => (
                <tr key={t.ticket}>
                  <td style={{ fontSize: 13 }}>
                    <span className="num">{new Date(t.close_time).toLocaleDateString('ar-SA')}</span>
                  </td>
                  <td><strong>{t.symbol}</strong></td>
                  <td>
                    <span className={t.type === 'BUY' ? 'badge badge-success' : 'badge badge-danger'}>
                      {t.type === 'BUY' ? 'شراء' : 'بيع'}
                    </span>
                  </td>
                  <td><span className="num">{t.volume}</span></td>
                  <td><span className="num">{t.open_price}</span></td>
                  <td><span className="num">{t.close_price}</span></td>
                  <td className={t.profit >= 0 ? 'price-up' : 'price-down'}>
                    <strong className="num">${t.profit.toFixed(2)}</strong>
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
