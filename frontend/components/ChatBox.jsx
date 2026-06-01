// ChatBox.jsx — chat input + progress + sample prompts
function ChatBox({ messages, onSend, loading }) {
  const [text, setText] = React.useState("");
  const bottomRef = React.useRef(null);
  const [stepIndex, setStepIndex] = React.useState(0);
  const timerRef = React.useRef(null);

  const steps = [
    { icon: "📊", label: "Analyzing sales data..."        },
    { icon: "💬", label: "Processing customer feedback..." },
    { icon: "🔍", label: "Running SWOT analysis..."       },
    { icon: "🎯", label: "Prioritizing features..."       },
    { icon: "🧠", label: "Generating strategy..."         },
    { icon: "📋", label: "Building executive report..."   },
  ];

  const samples = [
    "Analyze overall product performance",
    "Which products need improvement?",
    "Show me the SWOT analysis",
    "What are the top strategic recommendations?",
    "Which region has the highest revenue?",
  ];

  React.useEffect(() => {
    if (loading) {
      setStepIndex(0);
      timerRef.current = setInterval(() => setStepIndex(p => p < steps.length - 1 ? p + 1 : p), 2500);
    } else {
      clearInterval(timerRef.current);
      setStepIndex(0);
    }
    return () => clearInterval(timerRef.current);
  }, [loading]);

  React.useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  function handleSend(msg) {
    const m = msg || text.trim();
    if (!m || loading) return;
    onSend(m); setText("");
  }

  return (
    <React.Fragment>
      <div className="section-title">Chat</div>
      <div className="chat-messages">
        {messages.length === 0 && <div className="chat-bubble agent">Ask me anything about product strategy, sales, or customer insights...</div>}
        {messages.map((m, i) => <div key={i} className={`chat-bubble ${m.role}`}>{m.text}</div>)}
        <div ref={bottomRef} />
      </div>

      {loading && (
        <div className="progress-box">
          <span className="spinner" />
          <span className="progress-current">{steps[stepIndex].icon} {steps[stepIndex].label}</span>
        </div>
      )}

      <div className="chat-input-row">
        <input className="chat-input" value={text} onChange={e => setText(e.target.value)}
          onKeyDown={e => e.key === "Enter" && handleSend()} placeholder="Ask about strategy, sales, products..." disabled={loading} />
        <button className="chat-send-btn" onClick={() => handleSend()} disabled={loading}>{loading ? "⏳" : "Send"}</button>
      </div>

      <div className="section-title" style={{ marginTop: "8px" }}>Sample Prompts</div>
      <div className="sample-prompts">
        {samples.map((s, i) => <button key={i} className="sample-btn" onClick={() => handleSend(s)}>{s}</button>)}
      </div>
    </React.Fragment>
  );
}
