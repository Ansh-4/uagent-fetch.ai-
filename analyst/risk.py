
def assess_risk(
    requested_amount: float,
    treasury_balance: float,
) -> dict:
    """Assess basic treasury exposure using supplied figures."""

    if requested_amount < 0 or treasury_balance < 0:
        raise ValueError("Amounts cannot be negative.")

    if treasury_balance == 0:
        exposure = None
        level = "unknown"
        findings = [
            "Treasury balance is zero or unavailable.",
            "Affordability cannot be established.",
        ]
    else:
        exposure = round(
            requested_amount / treasury_balance * 100, 2
        )

        if requested_amount > treasury_balance:
            level = "critical"
            findings = [
                "Requested amount exceeds the reported treasury."
            ]
        elif exposure > 25:
            level = "high"
            findings = [
                "Proposal consumes more than 25% of reported treasury."
            ]
        elif exposure > 10:
            level = "moderate"
            findings = [
                "Proposal consumes more than 10% of reported treasury."
            ]
        else:
            level = "lower_concentration"
            findings = [
                "Treasury concentration is below the configured "
                "10% review threshold."
            ]

    findings.extend([
        "Token volatility and liquidity are not assessed.",
        "Verify the balance, token denomination, and outstanding "
        "commitments before relying on this result.",
    ])

    return {
        "treasury_exposure_percent": exposure,
        "risk_level": level,
        "risk_findings": findings,
    }
