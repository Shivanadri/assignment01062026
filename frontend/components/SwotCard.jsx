// SwotCard.jsx — SWOT analysis
function SwotCard({ swot }) {
  if (!swot || !swot.strengths) return null;
  const sections = [
    { key: "strengths",     cls: "s", title: "Strengths"     },
    { key: "weaknesses",    cls: "w", title: "Weaknesses"    },
    { key: "opportunities", cls: "o", title: "Opportunities" },
    { key: "threats",       cls: "t", title: "Threats"       },
  ];
  return (
    <div className="card">
      <h3><span className="card-icon">🔍</span> SWOT Analysis</h3>
      <div className="swot-grid">
        {sections.map(s => (
          <div key={s.key} className={`swot-box ${s.cls}`}>
            <div className="swot-title">{s.title}</div>
            {swot[s.key]?.map((item, i) => <div key={i} className="swot-item">• {item}</div>)}
          </div>
        ))}
      </div>
    </div>
  );
}
