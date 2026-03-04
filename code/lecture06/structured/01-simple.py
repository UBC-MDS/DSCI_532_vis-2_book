import chatlas as ctl
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Person(BaseModel):
    name: str
    age: int


chat = ctl.ChatGithub(model="gpt-4.1-mini")
# chat = ctl.ChatGithub(model="gpt-4.1")
# chat = ctl.ChatAnthropic()
# extract_data() is deprecated, use chat_structured() — returns a Pydantic model
res = chat.chat_structured(
    "My name is Susan and I'm 13 years old",
    data_model=Person,
)

# print(res)
# print(res.name, res.age)