from agents import Agent, Runner, ImageGenerationTool
from lib.files import retrieve_image_from_resources, open_file
import base64


my_agent = Agent(
    name="Interior Design Agent",
    instructions="""
    You are an interior design agent that can generate design images for every room in a home based on the floorplan that is submitted by the user.

    You should approach the problem using this process:  
    1. Identify the rooms in the floorplan image submitted by the user.
    2. Identify the realistic dimensions of each of the rooms in the floorplan.
    3. Plan the layout and design elements for each room based on the user's preferences (take into account the placement of fixed features such as doors and windows which are visible in the floorplan)
    4. Generate 1 image for each room based on the design plan.
    5. Save the interior design details into the database for each room that you have generated. Only save the details of the design after you have generated the image. Save the interior for this entire floorplan in a single database entry. Do not make multiple database entries. You must use the tool `save_design_data_to_database` to do this.

    The user's design preferences will be submitted using the user prompt.

    Image Generation guidelines:
    - Ensure that the images are relevant to the floorplan
    - Ensure that the images are from a camera perspective that showcases the entire room
    - Do not add in windows or doors where they do not exist in the floorplan
    - Do not generate individual images of hallways (these are not required)
    - Only generate a maximum of 2 images in total

    Output:
    You should return the final output of the agent, including the generated images. Do not output text links to the images in the final output.
    """,
    tools=[
    ImageGenerationTool({
      "type": "image_generation",
      "output_format": "png",
      "quality": "low",
      "size": "1024x1024"
    }),
    ],
     model="gpt-4.1"
    )

async def run_agent(design_style: str, floorplan_image: str):

    image = retrieve_image_from_resources(floorplan_image)

    formatted_input = [{
    "role": "user",
    "content": [
      {
        "type": "input_image",
        "image_url": f"data:image/jpeg;base64,{image}"
      },
      {
        "type": "input_text",
        "text": design_style
      }
    ]
    }]

    result = await Runner.run(
        my_agent,
        formatted_input
    )

    print("Agent Result:", result)

    ##return result

    image_paths = []

    image_count = 0

    for item in result.new_items:
      if (
        item.type == "tool_call_item"
        and item.raw_item.type == "image_generation_call"
        and (img_result := item.raw_item.result)
      ):
        with open(f"output/generated_image_{image_count}.png", "wb") as f:
          f.write(base64.b64decode(img_result))
          image_paths.append(f"output/generated_image_{image_count}.png")
          image_count += 1
          #open_file(f"output/generated_image_{image_count}.png")

    return image_paths