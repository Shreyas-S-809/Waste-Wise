import { useLocation } from 'react-router-dom';

const PAGE_META = {
  '/': {
    title: 'Dashboard Overview',
    desc: 'Real-time solid waste classification and segregation metrics',
  },
  '/classify': {
    title: 'Classification Workspace',
    desc: 'Individual waste item analysis and segregation status auditor',
  },
  '/history': {
    title: 'Audit History',
    desc: 'Chronological log of automated waste classifications',
  },
  '/model-info': {
    title: 'Model Diagnostics',
    desc: 'MobileNetV2 transfer learning performance metrics and confusion matrix',
  },
  '/about': {
    title: 'System Architecture',
    desc: 'Technical specifications, dataset mappings, and methodology',
  },
};

export default function Header() {
  const location = useLocation();
  const currentPath = location.pathname.startsWith('/classify') ? '/classify' : location.pathname;
  const meta = PAGE_META[currentPath] || {
    title: 'WasteWise System',
    desc: 'AI-Powered Waste Classification',
  };

  return (
    <header className="app-header">
      <div className="app-header__title-group">
        <h1 className="app-header__title">{meta.title}</h1>
        <span className="app-header__description">{meta.desc}</span>
      </div>

      <div className="app-header__badge">
        <span className="app-header__badge-dot"></span>
        <span>MobileNetV2 Online</span>
      </div>
    </header>
  );
}
