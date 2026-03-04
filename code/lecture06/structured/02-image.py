import chatlas as ctl
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Image(BaseModel):
    primary_shape: str
    primary_colour: str


chat = ctl.ChatGithub(model="gpt-4.1-mini")
# chat = ctl.ChatGithub(model="gpt-4.1")
# chat = ctl.ChatAnthropic()
# extract_data() is deprecated, use chat_structured() — returns a Pydantic model
res = chat.chat_structured(
    # https://picsum.photos/200/300
    ctl.content_image_url(
        "https://fastly.picsum.photos/id/19/200/300.jpg?hmac=znGSIxHtiP0JiLTKW6bT7HlcfagMutcHfeZyNkglQFM"
    ),
    data_model=Image,
)

# print(res)
