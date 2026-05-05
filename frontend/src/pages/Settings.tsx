import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import DashboardLayout from '../components/DashboardLayout';
import { mt5Api, authApi } from '../services/api';

export default function Settings() {
  const [accounts, setAccounts] = useState<any[]>([]);
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    authApi.me().then((r) => setUser(r.data));
    mt5Api.listAccounts().then((r) => setAccounts(r.data));
  }, []);

  const disconnect = async (id: string) => {
    if (!confirm('هل تريد إلغاء ربط هذا الحساب؟')) return;
    try {
      await mt5Api.disconnect(id);
      toast.success('تم إلغاء الربط');
      setAccounts(accounts.filter((a) => a.id !== id));
    } catch {
      toast.error('فشل إلغاء الربط');
    }
  };

  return (
    <DashboardLayout>
      <h1 style={{ fontSize: 28, marginBottom: 24 }}>الإعدادات</h1>

      <div className="card" style={{ marginBottom: 20 }}>
        <h2 style={{ fontSize: 18, marginBottom: 16 }}>الملف الشخصي</h2>
        <p><strong>الاسم:</strong> {user?.full_name}</p>
        <p><strong>البريد:</strong> {user?.email}</p>
        <p><strong>الجوال:</strong> {user?.phone || '-'}</p>
      </div>

      <div className="card">
        <h2 style={{ fontSize: 18, marginBottom: 16 }}>حسابات MT5 ({accounts.length})</h2>
        {accounts.map((a) => (
          <div key={a.id} style={{
            background: 'var(--color-bg)', padding: 16, borderRadius: 12,
            marginBottom: 12, display: 'flex', justifyContent: 'space-between',
          }}>
            <div>
              <strong>{a.nickname || `حساب ${a.login}`}</strong>
              <p style={{ color: 'var(--color-text-muted)', fontSize: 13 }}>
                <span className="num">{a.login}</span> · {a.server}
              </p>
            </div>
            <button onClick={() => disconnect(a.id)} className="btn btn-danger btn-sm">
              إلغاء الربط
            </button>
          </div>
        ))}
      </div>
    </DashboardLayout>
  );
}
