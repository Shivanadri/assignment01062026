// FeatureCard.jsx — feature prioritization
function FeatureCard({ features }) {
  if (!features || !features.priorities) return null;
  const actionClass = (action) =>
    action?.includes("Invest") ? "invest" : action?.includes("Improve") ? "improve" : "maintain";
  return (
    <div className="card">
      <h3><span className="card-icon">🎯</span> Feature Prioritization</h3>
      <div style={{fontSize:"11px",color:"#64748b",marginBottom:"10px"}}>{features.summary}</div>
      {features.priorities?.slice(0,7).map((p, i) => (
        <div key={i} className="priority-item">
          <span className="priority-rank">#{i+1}</span>
          <span className="priority-name">{p.product}</span>
          <span className="priority-score">{p.priority_score}</span>
          <span style={{fontSize:"10px",color:"#94a3b8",marginRight:"4px"}}>⭐{p.avg_rating}</span>
          <span className={`action-badge ${actionClass(p.action)}`}>{p.action.split(" — ")[0]}</span>
        </div>
      ))}
    </div>
  );
}
