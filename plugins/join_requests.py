from pyrogram import Client
from pyrogram.types import ChatJoinRequest

# MongoDB Integration
from config import Data

ACCEPTED_TEXT = "Hi {user}, welcome to {chat}! You can now access the files here."

@Client.on_chat_join_request()
async def req_accept(c: Client, m: ChatJoinRequest):
    user_id = m.from_user.id
    chat_id = m.chat.id

    # Check if user is already in the database
    user_exists = await Data.find_one({'id': user_id})
    if not user_exists: 
        await Data.insert_one({'id': user_id})

    # Approve the join request
    await c.approve_chat_join_request(chat_id, user_id)

    # Send welcome message to the user
    try:
        await c.send_message(
            user_id,
            ACCEPTED_TEXT.format(user=m.from_user.mention, chat=m.chat.title)
        )
    except Exception as e:
        print(f"Error sending message to {user_id}: {e}")
