import asyncio
import json

from ainft import Ainft
from ainft.types import Message

ainft = Ainft(
    private_key="YOUR_API_KEY",
    api_url="https://ainft-api-dev.ainetwork.ai",
    blockchain_url="https://testnet-api.ainetwork.ai",
    chain_id=0,
)


async def main():
    object_id = "YOUR_OBJECT_ID"
    app_id = f"ainft721_{object_id.lower()}"
    token_id = "YOUR_TOKEN_ID"
    thread_id = "YOUR_THREAD_ID"

    print("storing a thread")
    res1 = await ainft.chat.threads.store(
        thread_id=thread_id,
        object_id=object_id,
        token_id=token_id,
    )
    print("thread: ", res1.thread)
    print()

    print("storing a list of messages")
    messages = [
        Message(
            id="1",
            thread_id=thread_id,
            role="user",
            content="show pudgy penguins token 6873.",
            created_at=1710645225,
        ),
        Message(
            id="2",
            thread_id=thread_id,
            role="assistant",
            content="Hey there! I'm Aina, your friendly guide for NFT traits. Based on your query, the top traits I found are Cross Eyed, Normal, and Blue. I've got some additional NFTs related to these traits that you might find interesting! Let me know if you'd like to see them.",
            created_at=1710645320,
        ),
    ]
    res2 = await ainft.chat.messages.store(
        messages=messages,
        object_id=object_id,
        token_id=token_id,
    )
    print("messages: ")
    for message in res2.messages:
        print("message: ", message)
    print()

    # NOTE(jiyoung): read data from the ain blockchain database.
    # print("reading blockchain db")
    # value = await ainft._ain.db.ref(
    #     f"apps/{app_id}/tokens/{token_id}/ai/ainize_openai/history"
    # ).getValue()
    # print(json.dumps(value, indent=4))


asyncio.run(main())
