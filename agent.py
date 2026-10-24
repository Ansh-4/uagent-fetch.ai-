
from uagents import Agent, Context, Model


class WellnessMessage(Model):
    message: str


class WellnessSummary(Model):
    summary: str
    expressed_concerns: list[str]
    suggested_next_step: str
    disclaimer: str


agent = Agent(
    name="personal_wellness_agent",
    seed="mindbridge_wellness_agent_dev_seed_2026",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)


def analyze_message(message: str) -> WellnessSummary:
    text = message.lower()

    concern_keywords = {
        "stress": ["stress", "overwhelmed", "pressure"],
        "anxiety": ["anxious", "anxiety", "worried", "panic"],
        "low_mood": ["sad", "hopeless", "lonely", "unhappy"],
        "sleep": ["insomnia", "can't sleep", "cannot sleep"],
    }

    concerns = [
        category
        for category, keywords in concern_keywords.items()
        if any(keyword in text for keyword in keywords)
    ]

    if not concerns:
        concerns = ["no_clear_concern_detected"]

    return WellnessSummary(
        summary="The user shared: " + message[:500],
        expressed_concerns=concerns,
        suggested_next_step=(
            "Consider talking with a trusted person or qualified "
            "mental-health professional if these concerns persist."
        ),
        disclaimer=(
            "This is a basic text-based reflection, not a clinical "
            "assessment or diagnosis."
        ),
    )


@agent.on_message(model=WellnessMessage)
async def handle_wellness_message(
    ctx: Context,
    sender: str,
    msg: WellnessMessage,
):
    result = analyze_message(msg.message)

    ctx.logger.info(f"Received message from: {sender}")
    ctx.logger.info(f"Wellness summary: {result.summary}")
    ctx.logger.info(f"Expressed concerns: {result.expressed_concerns}")
    ctx.logger.info(f"Suggested next step: {result.suggested_next_step}")


@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("MindBridge Personal Wellness Agent is running.")
    ctx.logger.info(f"Agent address: {agent.address}")


if __name__ == "__main__":
    agent.run()
