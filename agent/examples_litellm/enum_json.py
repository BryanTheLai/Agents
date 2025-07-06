import enum
from dotenv import load_dotenv
from pydantic import BaseModel
import json as pyjson

from litellm import Field, completion  

load_dotenv()

messages = [{"role": "user", "content": """
Extract the information and return a list of columns:

report_date	product_category	revenue	cogs	marketing_spend
01-01-24	Electronics	50000	25000	5000
01-01-24	Apparel	20000	12000	3000
01-02-24	Electronics	55000	27500	5500
01-02-24	Apparel	18000	11000	4000
01-03-24	Electronics	62000	31000	6000
"""}]

class ColumnTypes(enum.Enum):
    text = "text"
    date = "date"
    number = "number"
    time = "time"
    email = "email"
    checkbox = "checkbox"
    tel = "tel"
    datetime_local = "datetime-local"

class Column(BaseModel):
    reasoning: str = Field(..., description="Resoning for the following data, start with 'Since ...'")
    sql_display_name: str = Field(..., min_length=1, description="Name of the column for sql table")
    col_display_name: str = Field(..., min_length=1, description="Name of the column for user to see")
    description: str = Field(..., description="Short concise description of the column")
    type: ColumnTypes = Field(..., description="Type of the column")
    example: str = Field(..., description="Example of data to use for the column")

class Columns(BaseModel):
    columns: list[Column] = Field(..., description="List of column definitions")

resp = completion(
    model="gemini/gemini-2.5-flash-lite-preview-06-17",
    messages=messages,
    response_format=Columns
)
message = resp.choices[0].message
data = pyjson.loads(message.content)
print(pyjson.dumps(data, indent=2))

# print(f"{data["columns"][0]["reasoning"]}")