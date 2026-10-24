
from typing import List, Optional
from shared.models import AnalysisRequest, AnalysisResult
from uagents import Agent, Context, Model


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


ANALYST_AGENT_ADDRESS = (
    "agent1qfx9t30lwa9ywf9zdr03rmcmj76ztum28r93j2hk8cmp6e8m23fgzykcu2a"
)

client = Agent(
    name="daothink_test_client",
    seed="daothink-test-client-seed-change-this",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
    mailbox=True,
)


@client.on_event("startup")
async def send_request(ctx: Context):
    ctx.logger.info(
        f"Sending analysis request to {ANALYST_AGENT_ADDRESS}..."
    )

    request = AnalysisRequest(
        proposal_id="test-001",
        proposal_title="DAO protocol integration",
        requested_amount=50000.0,
        treasury_balance=200000.0,
        research_findings=[
            "The proposal requests 50,000 USDC.",
            "The goal is protocol integration.",
        ],
        source_urls=["https://example.org/sample-proposal"],
        alternatives=[
            "Approve full amount",
            "Approve a smaller pilot",
            "Take no action",
        ],
    )

    await ctx.send(ANALYST_AGENT_ADDRESS, request)


@client.on_message(model=AnalysisResult)
async def receive_result(
    ctx: Context,
    sender: str,
    msg: AnalysisResult,
):
    ctx.logger.info(f"Received result: {msg.proposal_id}")
    ctx.logger.info(f"Treasury exposure: {msg.treasury_exposure_percent}%")
    ctx.logger.info(f"Risk level: {msg.risk_level}")
    ctx.logger.info(f"Review status: {msg.review_status}")
    ctx.logger.info(f"Recommendation: {msg.recommendation}")
    


if __name__ == "__main__":
    client.run()
