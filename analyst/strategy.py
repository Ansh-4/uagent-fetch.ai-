
from risk import assess_risk
from critic import critique_evidence


def analyze_strategy(
    proposal_title: str,
    requested_amount: float,
    treasury_balance: float,
    research_findings: list[str],
    source_urls: list[str],
    alternatives: list[str],
) -> dict:
    if not proposal_title.strip():
        raise ValueError("Proposal title cannot be empty.")

    risk = assess_risk(
        requested_amount=requested_amount,
        treasury_balance=treasury_balance,
    )

    critique = critique_evidence(
        research_findings=research_findings,
        source_urls=source_urls,
        alternatives=alternatives,
    )

    if not research_findings:
        assessment = (
            "Insufficient evidence to evaluate strategic value."
        )
    else:
        assessment = (
            f"Received {len(research_findings)} research finding(s). "
            "Benefits, costs, feasibility, and alternatives need "
            "to be evaluated against the supplied evidence."
        )

    if critique["evidence_gaps"]:
        recommendation = "DEFER_PENDING_EVIDENCE"
    elif risk["risk_level"] in {"critical", "high"}:
        recommendation = "ESCALATE_FOR_REVIEW"
    else:
        recommendation = "HUMAN_REVIEW_REQUIRED"

    return {
        "proposal_title": proposal_title,
        "strategy_assessment": assessment,
        "treasury_risk": risk,
        "critique": critique,
        "recommendation": recommendation,
    }
