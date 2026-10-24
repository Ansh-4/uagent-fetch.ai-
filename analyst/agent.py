
import os
from typing import List, Optional

from dotenv import load_dotenv
from uagents import Agent, Context, Model

from strategy import analyze_strategy
from critic import critique_evidence
from risk import assess_risk

# Load .env from the project directory
load_dotenv()

SEED = os.getenv("ANALYSIS_AGENT_SEED")

if not SEED:
    raise RuntimeError(
        "ANALYSIS_AGENT_SEED is missing. "
        "Check that .env is in the analyst folder."
    )


# ---------- Shared message models ----------

class AnalysisRequest(Model):
    proposal_id: str
    proposal_title: str
    requested_amount: float
    treasury_balance: float
    research_findings: List[str]
    source_urls: List[str]
    alternatives: List[str]


class AnalysisResult(Model):
    proposal_id: str
    strategy_assessment: str
    financial_assessment: str
    alternatives_assessment: str
    treasury_exposure_percent: Optional[float]
    risk_level: str
    critic_findings: List[str]
    risk_findings: List[str]
    evidence_gaps: List[str]
    review_status: str
    recommendation: str


# ---------- Create the Analyst Agent ----------

analysis_agent = Agent(
    name="daothink_analysis_agent",
    seed=SEED,
    port=8002,
    endpoint=["http://127.0.0.1:8002/submit"],
)


@analysis_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("DAOThink Analyst Agent is online.")
    ctx.logger.info(f"Agent address: {analysis_agent.address}")


@analysis_agent.on_message(model=AnalysisRequest)
async def handle_analysis(
    ctx: Context,
    sender: str,
    msg: AnalysisRequest,
):
    ctx.logger.info(
        f"Received analysis request: {msg.proposal_id}"
    )

    try:
        strategy = analyze_strategy(
            proposal_title=msg.proposal_title,
            requested_amount=msg.requested_amount,
            treasury_balance=msg.treasury_balance,
            research_findings=msg.research_findings,
            source_urls=msg.source_urls,
            alternatives=msg.alternatives,
        )

        risk = assess_risk(
            requested_amount=msg.requested_amount,
            treasury_balance=msg.treasury_balance,
        )

        critique = critique_evidence(
            research_findings=msg.research_findings,
            source_urls=msg.source_urls,
            alternatives=msg.alternatives,
        )

        await ctx.send(
            sender,
            AnalysisResult(
                proposal_id=msg.proposal_id,
                strategy_assessment=strategy["strategy_assessment"],
                financial_assessment=risk["risk_findings"][0],
                alternatives_assessment=(
                    strategy["treasury_risk"]["risk_findings"][0]
                    if strategy.get("treasury_risk")
                    else "Review alternatives against the supplied evidence."
                ),
                treasury_exposure_percent=(
                    risk["treasury_exposure_percent"]
                ),
                risk_level=risk["risk_level"],
                critic_findings=critique["critic_findings"],
                risk_findings=risk["risk_findings"],
                evidence_gaps=critique["evidence_gaps"],
                review_status=critique["review_status"],
                recommendation=strategy["recommendation"],
            ),
        )

        ctx.logger.info(
            f"Analysis result sent for {msg.proposal_id}"
        )

    except (ValueError, TypeError, KeyError) as exc:
        ctx.logger.warning(f"Could not analyze proposal: {exc}")

        await ctx.send(
            sender,
            AnalysisResult(
                proposal_id=msg.proposal_id,
                strategy_assessment="Analysis could not be completed.",
                financial_assessment="Input validation failed.",
                alternatives_assessment="Not assessed.",
                treasury_exposure_percent=None,
                risk_level="unknown",
                critic_findings=["The request could not be analyzed."],
                risk_findings=[str(exc)],
                evidence_gaps=["Correct the input and retry."],
                review_status="invalid_request",
                recommendation="HUMAN_REVIEW_REQUIRED",
            ),
        )


if __name__ == "__main__":
    analysis_agent.run()
