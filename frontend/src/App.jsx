import { Routes, Route, Navigate } from 'react-router-dom';
import AppLayout from './components/layout/AppLayout';
import Home from './pages/Home';
import Classifier from './pages/Classifier';
import History from './pages/History';
import ModelInfo from './pages/ModelInfo';
import About from './pages/About';
import NotFound from './pages/NotFound';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<AppLayout />}>
        <Route index element={<Home />} />
        <Route path="classify" element={<Classifier />} />
        <Route path="classify/item" element={<Navigate to="/classify?mode=item" replace />} />
        <Route path="classify/segregation" element={<Navigate to="/classify?mode=segregation" replace />} />
        <Route path="history" element={<History />} />
        <Route path="model-info" element={<ModelInfo />} />
        <Route path="about" element={<About />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
