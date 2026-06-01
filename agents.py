import csv
import os
from collections import Counter, defaultdict

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import httpx
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

NUMERIC_COLUMNS = {
    "Units_Sold": int,
    "Revenue_USD": float,
    "Cost_USD": float,
    "Profit_USD": float,
    "Marketing_Spend_USD": float,
    "Customer_Rating": float,
    "Returns": int,
    "New_Customers": int,
}

POSITIVE_KEYWORDS = ["great", "excellent", "highly recommend", "very satisfied", "best", "reliable", "easy to use"]
NEGATIVE_KEYWORDS = ["issues", "not satisfied", "bad", "would not buy", "poor", "average experience", "could be better"]


def load_sales_data(path):
    with open(path, encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = []
        for row in reader:
            parsed = {}
            for key, value in row.items():
                if value is None:
                    parsed[key] = None
                    continue
                value = value.strip()
                if key in NUMERIC_COLUMNS:
                    try:
                        parsed[key] = NUMERIC_COLUMNS[key](value)
                    except ValueError:
                        parsed[key] = 0
                else:
                    parsed[key] = value
            rows.append(parsed)
    return rows


def _build_llm():
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is not set in .env file.")
    return ChatOpenAI(
        model="openai/gpt-oss-120b:free",
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.4,
        default_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "Product Strategy Assistant",
        },
        http_client=httpx.Client(verify=False, timeout=30.0),
        request_timeout=30,
        max_retries=1,
    )


# ---------------------------------------------------------------------------
# Agent 1: Data Agent — sales data analysis + AI insights
# ---------------------------------------------------------------------------

class DataAgent:
    def __init__(self, rows):
        self.rows = rows
        self.llm = _build_llm()

    def _group_by(self, key, value_key="Revenue_USD"):
        totals = defaultdict(float)
        for row in self.rows:
            totals[row[key]] += float(row.get(value_key, 0) or 0)
        return totals

    def top_products_by_profit(self, top=3):
        totals = defaultdict(float)
        for row in self.rows:
            totals[row["Product_Name"]] += float(row.get("Profit_USD", 0) or 0)
        return sorted(totals.items(), key=lambda x: x[1], reverse=True)[:top]

    def region_summary(self):
        return self._group_by("Region", "Revenue_USD")

    def category_summary(self):
        return self._group_by("Category", "Revenue_USD")

    def product_risk_opportunities(self):
        profits = defaultdict(float)
        ratings = defaultdict(list)
        for row in self.rows:
            product = row["Product_Name"]
            profits[product] += float(row.get("Profit_USD", 0) or 0)
            ratings[product].append(float(row.get("Customer_Rating", 0) or 0))

        product_scores = []
        for product, profit in profits.items():
            avg_rating = sum(ratings[product]) / len(ratings[product]) if ratings[product] else 0
            product_scores.append((product, profit, avg_rating))

        risks = [p for p in product_scores if p[2] < 4.2]
        opportunities = [p for p in product_scores if p[2] >= 4.4]
        return {
            "risks": sorted(risks, key=lambda x: x[2])[:3],
            "opportunities": sorted(opportunities, key=lambda x: x[1], reverse=True)[:3],
        }

    def data_summary_text(self):
        top = self.top_products_by_profit(5)
        regions = self.region_summary()
        categories = self.category_summary()
        ro = self.product_risk_opportunities()
        lines = [
            "Top products by profit: " + ", ".join(f"{p}: ${v:,.0f}" for p, v in top),
            "Revenue by region: " + ", ".join(f"{r}: ${v:,.0f}" for r, v in regions.items()),
            "Revenue by category: " + ", ".join(f"{c}: ${v:,.0f}" for c, v in categories.items()),
            "Risk products: " + ", ".join(f"{p[0]} (rating {p[2]:.1f})" for p in ro["risks"]),
            "Opportunity products: " + ", ".join(f"{p[0]} (rating {p[2]:.1f})" for p in ro["opportunities"]),
        ]
        return "\n".join(lines)

    def generate_insights(self) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are a data analyst specializing in product sales. "
                "Analyze the sales data summary and provide 3-5 concise, actionable business insights."
            )),
            ("human", "Sales data summary:\n{data}\n\nProvide key data insights:"),
        ])
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"data": self.data_summary_text()})


# ---------------------------------------------------------------------------
# Agent 2: Feedback Agent — customer sentiment analysis
# ---------------------------------------------------------------------------

class FeedbackAgent:
    def __init__(self, rows):
        self.rows = rows
        self.llm = _build_llm()

    def sentiment_counts(self):
        positive = 0
        negative = 0
        for row in self.rows:
            review = row.get("Review", "").lower()
            if any(term in review for term in POSITIVE_KEYWORDS):
                positive += 1
            if any(term in review for term in NEGATIVE_KEYWORDS):
                negative += 1
        return positive, negative

    def average_rating(self):
        ratings = [row.get("Customer_Rating", 0) for row in self.rows if row.get("Customer_Rating") is not None]
        return sum(ratings) / len(ratings) if ratings else 0

    def common_feedback(self, top=5):
        phrases = Counter()
        for row in self.rows:
            review = row.get("Review", "").lower()
            for phrase in POSITIVE_KEYWORDS + NEGATIVE_KEYWORDS:
                if phrase in review:
                    phrases[phrase] += 1
        return phrases.most_common(top)

    def _reviews_sample(self, n=40):
        return [row.get("Review", "") for row in self.rows[:n] if row.get("Review")]

    def analyze_sentiment(self) -> str:
        positive, negative = self.sentiment_counts()
        avg = self.average_rating()
        reviews = self._reviews_sample(40)
        prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are a customer experience analyst. "
                "Analyze the customer reviews and rating data to identify key themes, "
                "pain points, and positive drivers. Be concise and actionable."
            )),
            ("human", (
                "Customer data:\n"
                "- Average rating: {avg}/5\n"
                "- Positive reviews: {positive}\n"
                "- Negative reviews: {negative}\n\n"
                "Sample reviews:\n{reviews}\n\n"
                "Provide a sentiment analysis with key themes and recommended actions:"
            )),
        ])
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({
            "avg": f"{avg:.1f}",
            "positive": positive,
            "negative": negative,
            "reviews": "\n".join(f"- {r}" for r in reviews),
        })


# ---------------------------------------------------------------------------
# Agent 3: SWOT Agent — strengths, weaknesses, opportunities, threats
# ---------------------------------------------------------------------------

class SWOTAgent:
    def __init__(self, data_agent: DataAgent, feedback_agent: FeedbackAgent):
        self.data_agent = data_agent
        self.feedback_agent = feedback_agent
        self.llm = _build_llm()

    def generate_swot(self) -> str:
        data_summary = self.data_agent.data_summary_text()
        positive, negative = self.feedback_agent.sentiment_counts()
        avg_rating = self.feedback_agent.average_rating()
        prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are a strategic business analyst. "
                "Generate a structured SWOT analysis based on the provided sales and customer feedback data. "
                "Use 2-3 bullet points per section."
            )),
            ("human", (
                "Sales data:\n{data}\n\n"
                "Customer feedback: avg rating {avg}/5, "
                "{pos} positive reviews, {neg} negative reviews.\n\n"
                "Generate the SWOT analysis:"
            )),
        ])
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({
            "data": data_summary,
            "avg": f"{avg_rating:.1f}",
            "pos": positive,
            "neg": negative,
        })


# ---------------------------------------------------------------------------
# Agent 4: Strategy Agent — orchestrates agents + handles natural language
# ---------------------------------------------------------------------------

class StrategyAgent:
    def __init__(self, data_agent: DataAgent, feedback_agent: FeedbackAgent, swot_agent: SWOTAgent):
        self.data_agent = data_agent
        self.feedback_agent = feedback_agent
        self.swot_agent = swot_agent
        self.llm = _build_llm()

    def generate_recommendations(self) -> str:
        data_summary = self.data_agent.data_summary_text()
        positive, negative = self.feedback_agent.sentiment_counts()
        avg_rating = self.feedback_agent.average_rating()
        swot = self.swot_agent.generate_swot()
        prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are a senior product strategist. "
                "Based on sales performance, customer feedback, and SWOT analysis, "
                "generate 5-7 prioritized strategic recommendations for the product team. "
                "Each recommendation should be actionable and tied to the data."
            )),
            ("human", (
                "Sales data:\n{data}\n\n"
                "Customer feedback: avg rating {avg}/5, {pos} positive, {neg} negative reviews.\n\n"
                "SWOT analysis:\n{swot}\n\n"
                "Provide strategic recommendations:"
            )),
        ])
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({
            "data": data_summary,
            "avg": f"{avg_rating:.1f}",
            "pos": positive,
            "neg": negative,
            "swot": swot,
        })

    def answer_question(self, question: str) -> str:
        data_summary = self.data_agent.data_summary_text()
        positive, negative = self.feedback_agent.sentiment_counts()
        avg_rating = self.feedback_agent.average_rating()
        prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are a product strategy AI assistant. "
                "Answer the user's question using the provided sales and customer feedback data. "
                "Be concise, data-driven, and specific."
            )),
            ("human", (
                "Sales data:\n{data}\n\n"
                "Customer feedback: avg rating {avg}/5, {pos} positive, {neg} negative reviews.\n\n"
                "Question: {question}"
            )),
        ])
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({
            "data": data_summary,
            "avg": f"{avg_rating:.1f}",
            "pos": positive,
            "neg": negative,
            "question": question,
        })


# ---------------------------------------------------------------------------
# Agent 5: Report Agent — executive report generation
# ---------------------------------------------------------------------------

class ReportAgent:
    def __init__(
        self,
        data_agent: DataAgent,
        feedback_agent: FeedbackAgent,
        swot_agent: SWOTAgent,
        strategy_agent: StrategyAgent,
    ):
        self.data_agent = data_agent
        self.feedback_agent = feedback_agent
        self.swot_agent = swot_agent
        self.strategy_agent = strategy_agent
        self.llm = _build_llm()

    def generate_executive_report(self) -> str:
        data_summary = self.data_agent.data_summary_text()
        insights = self.data_agent.generate_insights()
        sentiment = self.feedback_agent.analyze_sentiment()
        swot = self.swot_agent.generate_swot()
        recommendations = self.strategy_agent.generate_recommendations()
        prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are an executive report writer. "
                "Compile the provided analyses into a well-structured executive summary report "
                "suitable for senior leadership. Use clear sections and professional language."
            )),
            ("human", (
                "Sales data:\n{data}\n\n"
                "Data insights:\n{insights}\n\n"
                "Customer sentiment:\n{sentiment}\n\n"
                "SWOT analysis:\n{swot}\n\n"
                "Strategic recommendations:\n{recs}\n\n"
                "Write the executive report:"
            )),
        ])
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({
            "data": data_summary,
            "insights": insights,
            "sentiment": sentiment,
            "swot": swot,
            "recs": recommendations,
        })
