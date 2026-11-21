import { Link } from 'react-router-dom';
import Button from '../components/common/Button';

export default function NotFound() {
  return (
    <div className="not-found animate-fade-in">
      <div className="not-found__code">404</div>
      <h1 className="not-found__title">Page Not Found</h1>
      <p className="not-found__text">
        The page you are looking for does not exist or has been relocated.
      </p>
      <Link to="/">
        <Button variant="primary">Return to Home</Button>
      </Link>
    </div>
  );
}

