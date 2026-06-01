// StrategyCard.jsx — strategic recommendations + roadmap
function StrategyCard({ strategy, report }) {
  if (!strategy || !strategy.immediate_actions) return null;
  return (
    <div className="card">
      <h3><span className="card-icon">🧠</span> Strategic Recommendations</h3>

      {report?.executive_summary && (
        <div style={{background:"#eff6ff",borderLeft:"3px solid #6366f1",padding:"8px 12px",borderRadius:"0 6px 6px 0",fontSize:"12px",color:"#1e40af",marginBottom:"10px",lineHeight:"1.6"}}>
          {report.executive_summary}
        </div>
      )}

      <div className="strategy-section">
        <div className="strategy-label">Immediate Actions</div>
        {strategy.immediate_actions?.map((a, i) => <div key={i} className="strategy-item"><span className="strategy-dot" style={{background:"#ef4444"}} />{a}</div>)}
      </div>

      <div className="strategy-section">
        <div className="strategy-label">Short-Term Goals</div>
        {strategy.short_term_goals?.map((a, i) => <div key={i} className="strategy-item"><span className="strategy-dot" style={{background:"#eab308"}} />{a}</div>)}
      </div>

      <div className="strategy-section">
        <div className="strategy-label">Product Roadmap</div>
        {strategy.roadmap?.map((a, i) => <div key={i} className="strategy-item"><span className="strategy-dot" style={{background:"#6366f1"}} />{a}</div>)}
      </div>

      <div className="strategy-section">
        <div className="strategy-label">KPIs to Track</div>
        {strategy.kpis?.map((k, i) => <div key={i} className="strategy-item"><span className="strategy-dot" style={{background:"#22c55e"}} />{k}</div>)}
      </div>
    </div>
  );
}
