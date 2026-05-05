import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { authApi } from '../services/api';
import { useAuthStore } from '../services/auth';

export default function Register() {
  const navigate = useNavigate();
  const setToken = useAuthStore((s) => s.setToken);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    email: '', full_name: '', phone: '', password: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await authApi.register(form);
      setToken(res.data.access_token);
      toast.success('تم إنشاء حسابك بنجاح');
      navigate('/connect-mt5');
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'فشل إنشاء الحساب');
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
          <Link to="/login" className="btn btn-ghost">تسجيل الدخول</Link>
        </div>
      </nav>

      <div className="container" style={{ maxWidth: 480, padding: '60px 24px' }}>
        <div className="card" style={{ padding: 40 }}>
          <div style={{ textAlign: 'center', marginBottom: 32 }}>
            <h1 style={{ fontSize: 28, marginBottom: 8 }}>أهلاً بك في مُرشد</h1>
            <p style={{ color: 'var(--color-text-muted)' }}>أنشئ حسابك في أقل من دقيقة</p>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">الاسم الكامل</label>
              <input
                type="text"
                className="form-input"
                value={form.full_name}
                onChange={(e) => setForm({ ...form, full_name: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">البريد الإلكتروني</label>
              <input
                type="email"
                className="form-input"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">رقم الجوال (اختياري)</label>
              <input
                type="tel"
                className="form-input"
                dir="ltr"
                placeholder="+966 5X XXX XXXX"
                value={form.phone}
                onChange={(e) => setForm({ ...form, phone: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">كلمة المرور</label>
              <input
                type="password"
                className="form-input"
                minLength={8}
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                required
              />
            </div>
            <button type="submit" className="btn btn-primary btn-lg btn-block" disabled={loading}>
              {loading ? 'جاري الإنشاء...' : 'إنشاء الحساب'}
            </button>
          </form>

          <p style={{ textAlign: 'center', marginTop: 24, color: 'var(--color-text-muted)' }}>
            لديك حساب؟{' '}
            <Link to="/login" style={{ color: 'var(--color-primary)' }}>سجّل دخولك</Link>
          </p>
        </div>
      </div>
    </>
  );
}
