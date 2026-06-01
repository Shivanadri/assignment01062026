// FeedbackCard.jsx — customer feedback analysis
function FeedbackCard({ feedback }) {
  if (!feedback || !feedback.avg_rating) return null;
  return (
    <div className="card">
      <h3><span className="card-icon">💬</span> Customer Feedback</h3>
      <div className="feedback-stats">
        <div className="feedback-stat"><div className="label">Avg Rating</div><div className="val green">{feedback.avg_rating}/5</div></div>
        <div className="feedback-stat"><div className="label">Positive</div><div className="val green">{feedback.positive_reviews}</div></div>
        <div className="feedback-stat"><div className="label">Negative</div><div className="val red">{feedback.negative_reviews}</div></div>
        <div className="feedback-stat"><div className="label">Return Rate</div><div className="val red">{feedback.return_rate_pct}%</div></div>
      </div>
      <div className="section-title">Top Rated Products</div>
      {feedback.top_rated_products?.slice(0,3).map((p, i) => (
        <div key={i} className="table-row">
          <span className="table-label">{p.Product_Name}</span>
          <span className="table-value">⭐ {p.Customer_Rating?.toFixed(2)}</span>
        </div>
      ))}
      <div className="section-title" style={{marginTop:"10px"}}>Key Positives</div>
      {feedback.key_positives?.map((k, i) => <div key={i} className="strategy-item"><span className="strategy-dot" style={{background:"#22c55e"}} />{k}</div>)}
      <div className="section-title" style={{marginTop:"8px"}}>Key Issues</div>
      {feedback.key_issues?.map((k, i) => <div key={i} className="strategy-item"><span className="strategy-dot" style={{background:"#ef4444"}} />{k}</div>)}
    </div>
  );
}
