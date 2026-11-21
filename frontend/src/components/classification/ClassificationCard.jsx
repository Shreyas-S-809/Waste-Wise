import { Link } from 'react-router-dom';

export default function ClassificationCard({ icon, title, description, to }) {
  return (
    <Link to={to} className="mode-card">
      <div className="mode-card__icon">{icon}</div>
      <div className="mode-card__title">{title}</div>
      <p className="mode-card__description">{description}</p>
    </Link>
  );
}
