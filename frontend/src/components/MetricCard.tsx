export function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="panel">
      <div className="label">{label}</div>
      <div className="metric mt-2">{value}</div>
    </div>
  );
}
