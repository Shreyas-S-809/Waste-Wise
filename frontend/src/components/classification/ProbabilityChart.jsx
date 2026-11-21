import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';

const COLORS = ['#1B4332', '#2D6A4F', '#40916C', '#52B788', '#74C69D', '#95D5B2', '#B7E4C7'];

export default function ProbabilityChart({ probabilities }) {
  if (!probabilities || Object.keys(probabilities).length === 0) return null;

  const data = Object.entries(probabilities)
    .map(([name, value]) => ({
      name,
      probability: typeof value === 'number' ? +(value * 100).toFixed(1) : +parseFloat(value).toFixed(1),
    }))
    .sort((a, b) => b.probability - a.probability);

  return (
    <div style={{ marginTop: 'var(--space-6)' }}>
      <h4 style={{ marginBottom: 'var(--space-4)', fontSize: 'var(--font-size-base)', fontWeight: 600 }}>
        Probability Distribution
      </h4>
      <ResponsiveContainer width="100%" height={Math.max(200, data.length * 50)}>
        <BarChart data={data} layout="vertical" margin={{ top: 5, right: 30, left: 80, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E8F0E5" />
          <XAxis type="number" domain={[0, 100]} tickFormatter={(v) => `${v}%`} />
          <YAxis type="category" dataKey="name" width={70} tick={{ fontSize: 12 }} />
          <Tooltip formatter={(v) => [`${v}%`, 'Probability']} />
          <Bar dataKey="probability" radius={[0, 6, 6, 0]} barSize={24}>
            {data.map((entry, idx) => (
              <Cell key={entry.name} fill={COLORS[idx % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
