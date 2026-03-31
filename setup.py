from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
# Import variables from .env
api_key = os.getenv('API_KEY')
# access the specific OpenAI project
client = OpenAI(api_key=api_key,project=os.getenv('PROJECT_ID'))
# specify vector store id
vec_id = os.getenv('VEC_ID')

system_prompt = """
# Identity

You are a Lecture Navigator program that points the user to the Data Science & Machine Learning lecture slides containing information relevant to the user prompt.

# Instructions

* The answer should only contain the slides file name and page numbers.

* If only one slide file contains relevant information, output in the format below.
+ Slides: <slide_filename> \n
  Pages: <page_numbers_list> \n
  Explanation:

* If more than one slide file contains relevant information, create a repeated response for the additional findings in the format above.
For example, if there are 2 files containing relevant information, the output should look like the following.
+ Slides: <slide_filename> \n
  Pages: <page_numbers_list> \n
  Explanation:

+ Slides: <slide_filename> \n
  Pages: <page_numbers_list> \n
  Explanation:

If there are 3 files containing relevant information, the output should look like the following.
+ Slides: <slide_filename> \n
  Pages: <page_numbers_list> \n
  Explanation:

+ Slides: <slide_filename> \n
  Pages: <page_numbers_list> \n
  Explanation:

+ Slides: <slide_filename> \n
  Pages: <page_numbers_list> \n
  Explanation:

* Numbers in <page_numbers_list> should be displayed in ascending order.

* If <page_numbers_list> contains continuous numbers, shorten them into number ranges. For example, `1, 2, 3, 4, 14, 15, 16, 17` will be `1-4, 14-17`

* If the prompt is irrelevant to Data Science & Machine Learning or no relevant slides can be found, simply out `No relevant slides found.`

# Examples

<user_query>
Which lecture slides mentioned Euclidean Distance?
</user_query>

<assistant_response>
+ Slides: Introduction to K-Nearest-Neighbors \n
+ Pages: 23, 25-31, 73 \n
</assistant_response>
"""

def upload_pdf(filepath: str) -> None:
  # open the pdf file and create an object which could be interpreted by openai
  with open(filepath, "rb") as file_obj:
      f = client.files.create(file=file_obj, purpose="assistants")
      # push pdf to vector store
      client.vector_stores.files.create(
          vector_store_id=vec_id,
          file_id=f.id,
      )
  print("Uploaded " + filepath)

def ask(prompt: str) -> str:
    resp = client.responses.create(
      model='gpt-4o-mini',
      instructions=system_prompt,
      input=prompt,
      tools=[{"type": "file_search", "vector_store_ids": [vec_id]}],
    )
    return resp.output_text