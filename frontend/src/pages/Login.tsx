import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { authApi } from '../services/api';
import { useAuthStore } from '../services/auth';

export default function Login() {
  const navigate = useNavigate();
  const setToken = useAuthStore((s) => s.setToken);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ email: '', password: '' });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await authApi.login(form);
      setToken(res.data.access_token);
      toast.success('تم تسجيل الدخول بنجاح');
      navigate('/dashboard');
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'فشل تسجيل الدخول');
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
          <Link to="/register" className="btn btn-primary">إنشاء حساب</Link>
        </div>
      </nav>

      <div className="container" style={{ maxWidth: 440, padding: '80px 24px' }}>
        <div className="card" style={{ padding: 40 }}>
          <div style={{ textAlign: 'center', marginBottom: 32 }}>
            <h1 style={{ fontSize: 28, marginBottom: 8 }}>مرحباً بعودتك</h1>
            <p style={{ color: 'var(--color-text-muted)' }}>سجّل دخولك للوصول إلى لوحتك</p>
          </div>

          <form onSubmit={handleSubmit}>
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
              <label className="form-label">كلمة المرور</label>
              <input
                type="password"
                className="form-input"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                required
              />
            </div>
            <button type="submit" className="btn btn-primary btn-lg btn-block" disabled={loading}>
              {loading ? 'جاري تسجيل الدخول...' : 'تسجيل الدخول'}
            </button>
          </form>

          <p style={{ textAlign: 'center', marginTop: 24, color: 'var(--color-text-muted)' }}>
            ليس لديك حساب؟{' '}
            <Link to="/register" style={{ color: 'var(--color-primary)' }}>أنشئ واحداً</Link>
          </p>
        </div>
      </div>
    </>
  );
}
