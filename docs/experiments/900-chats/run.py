import json
from typing import cast
from rich import print as pprint
from rich.progress import track
import tiktoken
from time import time, sleep
from powermemo import PowerMemoClient, ChatBlob


PROJECT_URL = "http://localhost:8019"
PROJECT_TOKEN = "secret"


ENCODER = tiktoken.encoding_for_model("gpt-4o")
with open("./sharegpt_test_7uOhOjo.json") as f:
    data = json.load(f)


messages = [
    {"role": "user" if d["from"] == "human" else "assistant", "content": d["value"]}
    for d in data["conversations"]
]

blobs = [
    ChatBlob(
        messages=messages[i : i + 2],
    )
    for i in range(0, len(messages), 2)
]

print("Total blobs is ", len(blobs))
print(
    "Raw messages tokens is",
    len(ENCODER.encode("\n".join([m["content"] for m in messages]))),
)

client = PowerMemoClient(
    project_url=PROJECT_URL,
    api_key=PROJECT_TOKEN,
)

assert client.ping()


uid = client.add_user()
print("User ID is", uid)
u = client.get_user(uid)

start = time()
for blob in track(blobs):
    u.insert(blob)
u.flush()
print("Cost time(s)", time() - start)

pprint(u.profile()[:10])
prompts = [m.describe for m in u.profile()]
print("* " + "\n* ".join(sorted(prompts)))


# Change to the uid
# uid = "8327710d-f3a9-47e7-a28b-9e6f10bd01d5"
# print("User ID is", uid)
# u = client.get_user(uid)
# profiles = u.profile()

# prompts = [(m.topic, m.sub_topic) for m in profiles]
# pprint(sorted(prompts))

# for p in profiles:
#     if "married" in p.describe:
#         print(p.describe)
#         pprint(p)
#         for bid in p.related_blob_ids:
#             b = cast(ChatBlob, u.get(bid))
#             print("\n".join([f"{m.role}: {m.content}" for m in b.messages]))
#         break
