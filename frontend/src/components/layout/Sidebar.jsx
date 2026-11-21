import { useState, useEffect, useRef } from 'react';
import { NavLink, useLocation } from 'react-router-dom';

export default function Sidebar() {
  const location = useLocation();
  const navRef = useRef(null);
  const linkRefs = useRef({});
  const [activePill, setActivePill] = useState({ top: 0, height: 36, opacity: 0 });
  const [hoverPill, setHoverPill] = useState({ top: 0, height: 36, opacity: 0 });

  const navItems = [
    {
      to: '/',
      label: 'Dashboard',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <rect x="3" y="3" width="7" height="7"></rect>
          <rect x="14" y="3" width="7" height="7"></rect>
          <rect x="14" y="14" width="7" height="7"></rect>
          <rect x="3" y="14" width="7" height="7"></rect>
        </svg>
      ),
    },
    {
      to: '/classify',
      label: 'Waste Classifier',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
          <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
          <line x1="12" y1="22.08" x2="12" y2="12"></line>
        </svg>
      ),
    },
    {
      to: '/history',
      label: 'Audit History',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <polyline points="12 6 12 12 16 14"></polyline>
        </svg>
      ),
    },
    {
      to: '/model-info',
      label: 'Model Diagnostics',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <line x1="18" y1="20" x2="18" y2="10"></line>
          <line x1="12" y1="20" x2="12" y2="4"></line>
          <line x1="6" y1="20" x2="6" y2="14"></line>
        </svg>
      ),
    },
    {
      to: '/about',
      label: 'System Architecture',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="16" x2="12" y2="12"></line>
          <line x1="12" y1="8" x2="12.01" y2="8"></line>
        </svg>
      ),
    },
  ];

  const getActiveKey = () => {
    const path = location.pathname;
    if (path.startsWith('/classify')) return '/classify';
    const match = navItems.find((item) => (item.to === '/' ? path === '/' : path.startsWith(item.to)));
    return match ? match.to : '/';
  };

  const activeKey = getActiveKey();

  // Morph active pill position whenever activeKey or resize occurs
  useEffect(() => {
    const updatePosition = () => {
      const activeEl = linkRefs.current[activeKey];
      if (activeEl) {
        setActivePill({
          top: activeEl.offsetTop,
          height: activeEl.offsetHeight,
          opacity: 1,
        });
      }
    };

    updatePosition();
    // In case fonts or layout settles
    const timer = setTimeout(updatePosition, 50);
    window.addEventListener('resize', updatePosition);
    return () => {
      clearTimeout(timer);
      window.removeEventListener('resize', updatePosition);
    };
  }, [activeKey]);

  const handleMouseEnter = (key) => {
    if (key === activeKey) {
      setHoverPill((prev) => ({ ...prev, opacity: 0 }));
      return;
    }
    const el = linkRefs.current[key];
    if (el) {
      setHoverPill({
        top: el.offsetTop,
        height: el.offsetHeight,
        opacity: 1,
      });
    }
  };

  const handleMouseLeave = () => {
    setHoverPill((prev) => ({ ...prev, opacity: 0 }));
  };

  return (
    <aside className="sidebar">
      <div className="sidebar__header">
        <div className="sidebar__logo-badge">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="7 10 12 15 17 10"></polyline>
            <path d="M12 15V3"></path>
            <path d="M20 21H4"></path>
          </svg>
        </div>
        <span className="sidebar__brand-text">WasteWise</span>
      </div>

      <nav
        ref={navRef}
        className="sidebar__nav"
        onMouseLeave={handleMouseLeave}
      >
        <div className="sidebar__nav-section-title">Navigation</div>

        {/* Morphing Hover Pill */}
        <div
          className="sidebar__hover-pill"
          style={{
            transform: `translateY(${hoverPill.top}px)`,
            height: `${hoverPill.height}px`,
            opacity: hoverPill.opacity,
          }}
        />

        {/* Morphing Active Tab Pill */}
        <div
          className="sidebar__active-pill"
          style={{
            transform: `translateY(${activePill.top}px)`,
            height: `${activePill.height}px`,
            opacity: activePill.opacity,
          }}
        />

        {navItems.map((item) => {
          const isActive = item.to === activeKey;
          return (
            <NavLink
              key={item.to}
              ref={(el) => {
                if (el) linkRefs.current[item.to] = el;
              }}
              to={item.to}
              end={item.to === '/'}
              className={`sidebar__link ${isActive ? 'sidebar__link--active' : ''}`}
              onMouseEnter={() => handleMouseEnter(item.to)}
            >
              <span className="sidebar__link-icon">{item.icon}</span>
              <span className="sidebar__link-text">{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className="sidebar__footer">
        <div className="sidebar__status-box">
          <div className="sidebar__status-indicator">
            <span className="sidebar__status-dot"></span>
            <span>MobileNetV2</span>
          </div>
          <span className="sidebar__version-tag">v1.0.0</span>
        </div>
      </div>
    </aside>
  );
}
