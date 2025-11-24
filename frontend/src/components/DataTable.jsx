function DataTable({ rows }) {
  if (!rows || rows.length === 0) {
    return <div className="text-muted">No rows to display.</div>;
  }

  const columns = Object.keys(rows[0]);

  return (
    <div className="table-responsive">
      <table className="table table-sm table-bordered">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col}>{col.toUpperCase()}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr key={idx}>
              {columns.map((col) => (
                <td key={col}>{row[col]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default DataTable;
