import { Link } from 'react-router-dom';

export default function Landing() {
  return (
    <>
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/" className="logo">
            <div className="logo-icon">م</div>
            <span>مُرشد</span>
          </Link>
          <div style={{ display: 'flex', gap: 12 }}>
            <Link to="/login" className="btn btn-ghost">تسجيل الدخول</Link>
            <Link to="/register" className="btn btn-primary">ابدأ مجاناً</Link>
          </div>
        </div>
      </nav>

      <section style={{ padding: '80px 0' }}>
        <div className="container" style={{ textAlign: 'center', maxWidth: 800 }}>
          <div style={{
            display: 'inline-flex', gap: 8, padding: '8px 16px',
            background: 'rgba(0, 214, 143, 0.1)',
            border: '1px solid rgba(0, 214, 143, 0.3)',
            borderRadius: 100, fontSize: 13, color: 'var(--color-primary)',
            marginBottom: 24,
          }}>
            <span className="live-dot"></span>
            <span>منصة سعودية مرتبطة بـ MetaTrader 5</span>
          </div>
          <h1 style={{ fontSize: 'clamp(36px, 6vw, 64px)', marginBottom: 24, lineHeight: 1.15 }}>
            تداول بثقة، <br/>
            <span style={{
              background: 'linear-gradient(135deg, var(--color-primary), var(--color-primary-light))',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}>بواجهة عربية واضحة</span>
          </h1>
          <p style={{ fontSize: 19, color: 'var(--color-text-muted)', marginBottom: 32 }}>
            منصة "مُرشد" تأخذ تعقيد MetaTrader 5 وتحوله إلى تجربة بسيطة وأنيقة بالعربية.
          </p>
          <div style={{ display: 'flex', gap: 16, justifyContent: 'center', flexWrap: 'wrap' }}>
            <Link to="/register" className="btn btn-primary btn-lg">
              ابدأ تجربتك المجانية ←
            </Link>
            <Link to="/login" className="btn btn-secondary btn-lg">
              تسجيل الدخول
            </Link>
          </div>
        </div>
      </section>

      <section style={{ padding: '80px 0', background: 'var(--color-bg-elevated)' }}>
        <div className="container">
          <div style={{ textAlign: 'center', marginBottom: 56 }}>
            <h2 style={{ fontSize: 36, marginBottom: 16 }}>كل ما تحتاجه، بطريقة أبسط</h2>
            <p style={{ color: 'var(--color-text-muted)', fontSize: 17 }}>
              ميزات احترافية مصممة لتجعل التداول واضحاً ومريحاً
            </p>
          </div>
          <div className="grid grid-3">
            {[
              { icon: '🔗', title: 'ربط آمن مع MT5', desc: 'بياناتك مشفرة بـ AES-256' },
              { icon: '📊', title: 'لوحة تحكم ذكية', desc: 'كل بياناتك بالعربي في مكان واحد' },
              { icon: '⚡', title: 'تنفيذ سريع', desc: 'فتح وإغلاق الصفقات بزر واحد' },
              { icon: '🤖', title: 'تداول آلي', desc: 'انسخ صفقات المحترفين' },
              { icon: '📈', title: 'تحليل عميق', desc: 'رؤى ذكية لتحسين أدائك' },
              { icon: '🔔', title: 'إشعارات ذكية', desc: 'تنبيهات فورية بالعربي' },
            ].map((f, i) => (
              <div key={i} className="card">
                <div style={{ fontSize: 40, marginBottom: 16 }}>{f.icon}</div>
                <h3 style={{ fontSize: 20, marginBottom: 12 }}>{f.title}</h3>
                <p style={{ color: 'var(--color-text-muted)' }}>{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
