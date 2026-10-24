from typing import List, Optional

from uagents import Model


class DAOAnalysisRequest(Model):
    proposal_id: str
    proposal_title: str
    proposal_url: str
    requested_amount: Optional[float] = None
    treasury_balance: Optional[float] = None


class ResearchRequest(Model):
    proposal_id: str
    proposal_title: str
    proposal_url: str


class ResearchResult(Model):
    proposal_id: str
    summary: str
    findings: List[str]
    source_urls: List[str]
    limitations: List[str]


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
    recommendation: str
    strategy_assessment: str
    financial_assessment: str
    alternatives_assessment: str
    critic_findings: List[str]
    risk_findings: List[str]
    evidence_gaps: List[str]
    review_status: str


class DecisionReport(Model):
    proposal_id: str
    proposal_title: str
    research_summary: str
    research_findings: List[str]
    recommendation: str
    strategy_assessment: str
    financial_assessment: str
    alternatives_assessment: str
    critic_findings: List[str]
    risk_findings: List[str]
    evidence_gaps: List[str]
    source_urls: List[str]
    status: str