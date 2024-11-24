from pyrogram import Client
from pyrogram.types import ChatJoinRequest
from bot import Bot  # Ensure Bot is imported from your bot's main file

ACCEPTED_TEXT = "Hi {user}, welcome to {chat}! You can now access the files here."

@Bot.on_chat_join_request()
async def req_accept(c: Client, m: ChatJoinRequest):
    user_id = m.from_user.id
    chat_id = m.chat.id

    # Approve the join request
    await c.approve_chat_join_request(chat_id, user_id)

    # Send a welcome message
    try:
        await c.send_message(
            user_id,
            ACCEPTED_TEXT.format(user=m.from_user.mention, chat=m.chat.title)
        )
    except Exception as e:
        print(f"Error sending message to {user_id}: {e}")
