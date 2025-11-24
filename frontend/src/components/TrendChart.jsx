import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

function TrendChart({ data }) {
  if (!data || data.length === 0) {
    return <div className="text-muted">Chart data not available.</div>;
  }

  return (
    <div style={{ height: 300 }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="year" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="value" name="Value" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default TrendChart;
