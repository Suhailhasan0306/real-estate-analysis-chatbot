import TrendChart from "./TrendChart";
import DataTable from "./DataTable";

function AnalysisResult({ analysis }) {
  if (!analysis) {
    return (
      <div className="text-muted">
        <h5>Welcome to Real Estate Analysis</h5>
        <p>Type a query to start analyzing property trends.</p>
      </div>
    );
  }

  const metricLabel =
    analysis.metric === "demand"
      ? "Demand (total sold)"
      : "Price (total sales)";

  return (
    <div>
      <h5>
        Trend Analysis <small className="text-muted">({metricLabel})</small>
      </h5>
      <TrendChart data={analysis.chartData} />

      {analysis.chartData.length === 0 && (
      <p style={{ color: "red" }}>
        No trend data available for selected area and metric.
      </p>
      )}


      <h5 className="mt-4">
        Data Table <small className="text-muted">({metricLabel})</small>
      </h5>
      <DataTable rows={analysis.tableData} />
    </div>
  );
}

export default AnalysisResult;
