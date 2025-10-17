from agents import Agent, Runner

my_agent = Agent(name="ExampleAgent", instructions="Answer math questions to a user input")

async def run_agent():
    result = await Runner.run(
        my_agent,
        "What is 2 + 2"
    )

    print("Agent Result:", result)

    return result