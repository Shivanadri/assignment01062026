from agents import load_sales_data, DataAgent, FeedbackAgent, SWOTAgent, StrategyAgent, ReportAgent

DATA_PATH = "Sample Sales Data.csv"


def main():
    print("\nAI-Powered Product Strategy Assistant")
    print("======================================")
    print("Loading sales data and initializing AI agents...\n")

    rows = load_sales_data(DATA_PATH)
    data_agent = DataAgent(rows)
    feedback_agent = FeedbackAgent(rows)
    swot_agent = SWOTAgent(data_agent, feedback_agent)
    strategy_agent = StrategyAgent(data_agent, feedback_agent, swot_agent)
    report_agent = ReportAgent(data_agent, feedback_agent, swot_agent, strategy_agent)

    print(f"Loaded {len(rows)} sales records from {DATA_PATH}")
    print("Agents ready: DataAgent | FeedbackAgent | SWOTAgent | StrategyAgent | ReportAgent\n")

    print("Generating initial strategy summary (powered by GPT-4o Mini)...\n")
    print(strategy_agent.generate_recommendations())

    print("\n----------------------------------------------------------------------")
    print("You can ask any question in natural language, or use these shortcuts:")
    print("  insights    - AI-generated data insights")
    print("  sentiment   - Customer sentiment analysis")
    print("  swot        - SWOT analysis")
    print("  strategy    - Strategic recommendations")
    print("  report      - Full executive report")
    print("  exit        - Quit")
    print("----------------------------------------------------------------------\n")

    while True:
        try:
            query = input("Your question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting the Product Strategy Assistant.")
            break

        if not query:
            continue

        lower = query.lower()

        if lower in ["exit", "quit", "q"]:
            print("Exiting the Product Strategy Assistant.")
            break
        elif lower == "insights":
            print("\n" + data_agent.generate_insights())
        elif lower == "sentiment":
            print("\n" + feedback_agent.analyze_sentiment())
        elif lower == "swot":
            print("\n" + swot_agent.generate_swot())
        elif lower in ["strategy", "recommendations"]:
            print("\n" + strategy_agent.generate_recommendations())
        elif lower == "report":
            print("\n" + report_agent.generate_executive_report())
        else:
            print("\n" + strategy_agent.answer_question(query))

        print()


if __name__ == "__main__":
    main()
