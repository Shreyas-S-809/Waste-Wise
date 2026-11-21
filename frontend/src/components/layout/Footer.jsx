export default function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer__inner">
        <div className="footer__brand">WasteWise</div>
        <p className="footer__copy">
          © {year} WasteWise — AI-Powered Waste Classification System
        </p>
        <div className="footer__badges">
          <span className="footer__badge">React</span>
          <span className="footer__badge">Flask</span>
          <span className="footer__badge">TensorFlow</span>
          <span className="footer__badge">MobileNetV2</span>
        </div>
      </div>
    </footer>
  );
}
