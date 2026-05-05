import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { mt5Api } from '../services/api';

export default function ConnectMT5() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    login: '', password: '', server: '', nickname: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await mt5Api.connect(form);
      toast.success('تم ربط حساب MT5 بنجاح');
      navigate('/dashboard');
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'فشل ربط الحساب');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/" className="logo">
            <div className="logo-icon">م</div>
            <span>مُرشد</span>
          </Link>
        </div>
      </nav>

      <div className="container" style={{ maxWidth: 720, padding: '40px 24px' }}>
        <div style={{ textAlign: 'center', marginBottom: 40 }}>
          <h1 style={{ fontSize: 32 }}>اربط حساب MetaTrader 5</h1>
          <p style={{ color: 'var(--color-text-muted)' }}>خطوة واحدة وتبدأ التداول</p>
        </div>

        <div style={{
          background: 'rgba(255, 184, 0, 0.1)',
          border: '1px solid rgba(255, 184, 0, 0.3)',
          padding: 16,
          borderRadius: 12,
          marginBottom: 24,
          display: 'flex',
          gap: 12,
        }}>
          <span style={{ fontSize: 20 }}>⚠️</span>
          <div style={{ fontSize: 14 }}>
            تحتاج حساب نشط لدى وسيط معتمد يدعم MetaTrader 5.
            استخدم Investor Password إن كنت ترغب بالمراقبة فقط بدون تداول.
          </div>
        </div>

        <div className="card" style={{ padding: 32 }}>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">رقم الحساب (Login)</label>
              <input
                type="text"
                className="form-input"
                dir="ltr"
                placeholder="12345678"
                value={form.login}
                onChange={(e) => setForm({ ...form, login: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">كلمة المرور</label>
              <input
                type="password"
                className="form-input"
                dir="ltr"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">اسم السيرفر</label>
              <select
                className="form-select"
                value={form.server}
                onChange={(e) => setForm({ ...form, server: e.target.value })}
                required
              >
                <option value="">اختر السيرفر...</option>
                <option value="XMGlobal-MT5">XM Global - Real</option>
                <option value="XMGlobal-MT5-Demo">XM Global - Demo</option>
                <option value="Exness-MT5Real">Exness - Real</option>
                <option value="Exness-MT5Trial">Exness - Demo</option>
                <option value="ICMarkets-MT5">IC Markets - Real</option>
                <option value="FXTM-MT5Live">FXTM - Real</option>
                <option value="Pepperstone-MT5">Pepperstone - Real</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">اسم تعريفي (اختياري)</label>
              <input
                type="text"
                className="form-input"
                placeholder="حساب فوركس رئيسي"
                value={form.nickname}
                onChange={(e) => setForm({ ...form, nickname: e.target.value })}
              />
            </div>

            <div style={{
              background: 'var(--color-bg)', borderRadius: 12,
              padding: 16, marginBottom: 24, fontSize: 13,
              color: 'var(--color-text-muted)',
            }}>
              🔐 بياناتك مشفرة بـ AES-256. لن نخزن كلمة المرور بشكل واضح.
            </div>

            <button type="submit" className="btn btn-primary btn-lg btn-block" disabled={loading}>
              {loading ? 'جاري الربط (قد يستغرق دقيقة)...' : 'ربط الحساب'}
            </button>
          </form>
        </div>
      </div>
    </>
  );
}
