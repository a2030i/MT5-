import { useState } from 'react';
import toast from 'react-hot-toast';
import DashboardLayout from '../components/DashboardLayout';
import { mt5Api } from '../services/api';

export default function Trade() {
  const [form, setForm] = useState({
    symbol: 'EURUSD',
    type: 'BUY',
    volume: 0.1,
    stop_loss: '',
    take_profit: '',
  });
  const [loading, setLoading] = useState(false);

  const execute = async (type: 'BUY' | 'SELL') => {
    setLoading(true);
    try {
      const accs = await mt5Api.listAccounts();
      if (!accs.data[0]) {
        toast.error('لا يوجد حساب MT5 مرتبط');
        return;
      }
      await mt5Api.trade(accs.data[0].id, {
        symbol: form.symbol,
        type,
        volume: form.volume,
        stop_loss: form.stop_loss ? Number(form.stop_loss) : null,
        take_profit: form.take_profit ? Number(form.take_profit) : null,
      });
      toast.success(`تم تنفيذ صفقة ${type === 'BUY' ? 'شراء' : 'بيع'}`);
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'فشل تنفيذ الصفقة');
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <h1 style={{ fontSize: 28, marginBottom: 24 }}>تداول جديد</h1>
      <div className="card" style={{ maxWidth: 500 }}>
        <div className="form-group">
          <label className="form-label">الرمز</label>
          <select
            className="form-select"
            value={form.symbol}
            onChange={(e) => setForm({ ...form, symbol: e.target.value })}
          >
            <option value="EURUSD">EUR/USD</option>
            <option value="GBPUSD">GBP/USD</option>
            <option value="XAUUSD">XAU/USD (الذهب)</option>
            <option value="USDJPY">USD/JPY</option>
            <option value="BTCUSD">BTC/USD</option>
          </select>
        </div>
        <div className="form-group">
          <label className="form-label">حجم الصفقة (Lot)</label>
          <input
            type="number"
            step="0.01"
            min="0.01"
            className="form-input"
            dir="ltr"
            value={form.volume}
            onChange={(e) => setForm({ ...form, volume: parseFloat(e.target.value) })}
          />
        </div>
        <div className="form-group">
          <label className="form-label">وقف الخسارة (اختياري)</label>
          <input
            type="number"
            step="0.00001"
            className="form-input"
            dir="ltr"
            value={form.stop_loss}
            onChange={(e) => setForm({ ...form, stop_loss: e.target.value })}
          />
        </div>
        <div className="form-group">
          <label className="form-label">جني الأرباح (اختياري)</label>
          <input
            type="number"
            step="0.00001"
            className="form-input"
            dir="ltr"
            value={form.take_profit}
            onChange={(e) => setForm({ ...form, take_profit: e.target.value })}
          />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
          <button
            onClick={() => execute('SELL')}
            className="btn btn-danger btn-lg"
            disabled={loading}
          >
            بيع
          </button>
          <button
            onClick={() => execute('BUY')}
            className="btn btn-primary btn-lg"
            disabled={loading}
          >
            شراء
          </button>
        </div>
      </div>
    </DashboardLayout>
  );
}
