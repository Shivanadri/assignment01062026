// SalesCard.jsx — sales performance overview
function SalesCard({ sales }) {
  if (!sales || !sales.total_revenue) return null;
  return (
    <div className="card">
      <h3><span className="card-icon">📊</span> Sales Performance</h3>
      <div className="kpi-grid">
        <div className="kpi-box"><div className="kpi-label">Total Revenue</div><div className="kpi-value green">${sales.total_revenue?.toLocaleString()}</div></div>
        <div className="kpi-box"><div className="kpi-label">Total Profit</div><div className="kpi-value blue">${sales.total_profit?.toLocaleString()}</div></div>
        <div className="kpi-box"><div className="kpi-label">Profit Margin</div><div className="kpi-value">{sales.profit_margin_pct}%</div></div>
        <div className="kpi-box"><div className="kpi-label">New Customers</div><div className="kpi-value">{sales.new_customers?.toLocaleString()}</div></div>
      </div>
      <div className="section-title">Top Products by Revenue</div>
      {sales.by_product?.slice(0,4).map((p, i) => (
        <div key={i} className="table-row">
          <span className="table-label">{p.Product_Name}</span>
          <span className="table-value">${p.Revenue?.toLocaleString()}</span>
        </div>
      ))}
      <div className="section-title" style={{marginTop:"10px"}}>Revenue by Category</div>
      {sales.by_category?.map((c, i) => (
        <div key={i} className="table-row">
          <span className="table-label">{c.Category}</span>
          <span className="table-value">${c.Revenue?.toLocaleString()}</span>
        </div>
      ))}
    </div>
  );
}
