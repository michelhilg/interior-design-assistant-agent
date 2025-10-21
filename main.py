import asyncio
from lib.agent import run_agent

from dotenv import load_dotenv

load_dotenv()

async def main():

  result = await run_agent("Estilo minimalista moderno com tons de mandeira", "floorplan.png")

  print("Final output:", result["final_output"])
  print("Image paths:", result["image_paths"])

if __name__ == "__main__":

  asyncio.run(main())