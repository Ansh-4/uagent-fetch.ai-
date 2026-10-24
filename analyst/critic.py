
def critique_evidence(
    research_findings: list[str],
    source_urls: list[str],
    alternatives: list[str],
) -> dict:
    findings = [
        item.strip()
        for item in research_findings
        if item.strip()
    ]
    sources = [
        url.strip()
        for url in source_urls
        if url.strip()
    ]
    options = [
        item.strip()
        for item in alternatives
        if item.strip()
    ]

    issues = []
    evidence_gaps = []

    if not findings:
        evidence_gaps.append("No research findings were supplied.")

    if not sources:
        evidence_gaps.append("No source links were supplied.")

    if findings and not sources:
        issues.append(
            "Claims cannot currently be traced to supporting sources."
        )

    if not options:
        evidence_gaps.append(
            "No alternatives were supplied, including the option "
            "of taking no action."
        )

    issues.extend([
        "Verify material claims against their original sources.",
        "Check whether expected benefits are facts or assumptions.",
        "Check implementation dependencies and conflicts of interest.",
    ])

    return {
        "critic_findings": issues,
        "evidence_gaps": evidence_gaps,
        "review_status": (
            "needs_more_evidence"
            if evidence_gaps
            else "ready_for_human_review"
        ),
    }
