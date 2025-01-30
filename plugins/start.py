# (Â©)NextGenBotz
import asyncio
import base64
import logging
import os
import random
import re
import string
import time

from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import (
    ADMINS,
    FORCE_MSG,
    START_MSG,
    CUSTOM_CAPTION,
    # IS_VERIFY,  # Commented for verification
    # VERIFY_EXPIRE,  # Commented for verification
    # SHORTLINK_API,  # Commented for shortlink
    # SHORTLINK_URL,  # Commented for shortlink
    DISABLE_CHANNEL_BUTTON,
    PROTECT_CONTENT,
    TUT_VID,
    OWNER_ID,
)
from helper_func import (
    subscribed,
    encode,
    decode,
    get_messages,
    # get_shortlink,  # Commented for shortlink
    # get_verify_status,  # Commented for verification
    # update_verify_status,  # Commented for verification
    # get_exp_time  # Commented for verification
)
from database.database import add_user, del_user, full_userbase, present_user
# from shortzy import Shortzy  # Commented for shortlink


@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    owner_ids = ADMINS  # Agar ADMINS list hai, to use karein

    text = message.text  # message.text ko variable me store karein

    if id in owner_ids:  # Agar owner hai
        await message.reply("You are the owner! Additional actions can be added here.")
        return

    if not await present_user(id):
        try:
            await add_user(id)
        except Exception as e:
            print(f"Error adding user: {e}")

    # Decode Base64 argument if available
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
            decoded_string = await decode(base64_string)  # Agar decode async hai
            argument = decoded_string.split("-")
        except (IndexError, Exception) as e:
            print(f"Error decoding Base64: {e}")
            return

        ids = []
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
            except Exception as e:
                print(f"Error decoding IDs: {e}")
                return

        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except Exception as e:
                print(f"Error decoding ID: {e}")
                return

        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except Exception as e:
            await message.reply_text("Something went wrong!")
            print(f"Error getting messages: {e}")
            return
        finally:
            await temp_msg.delete()

        codeflix_msgs = []
        for msg in messages:
            caption = (CUSTOM_CAPTION.format(previouscaption=msg.caption.html if msg.caption else "",
                                             filename=msg.document.file_name) if CUSTOM_CAPTION and msg.document
                       else (msg.caption.html if msg.caption else ""))

            reply_markup = msg.reply_markup if not DISABLE_CHANNEL_BUTTON else None

            try:
                copied_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT
                )
                codeflix_msgs.append(copied_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                copied_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT
                )
                codeflix_msgs.append(copied_msg)
            except Exception as e:
                print(f"Failed to send message: {e}")

    else:
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("About Me", callback_data="about"),
             InlineKeyboardButton("Close", callback_data="close")]
        ])
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=f'@{message.from_user.username}' if message.from_user.username else None,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )


        # Commented out verify link section for token check
        # else:
        #     verify_status = await get_verify_status(id)
        #     if IS_VERIFY and not verify_status['is_verified']:
        #         short_url = f"api.shareus.io"
        #         full_tut_url = f"https://t.me/How_to_download_tutorial_idk/2"
        #         token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        #         await update_verify_status(id, verify_token=token, link="")
        #         link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API,f'https://telegram.dog/{client.username}?start=verify_{token}')
        #         btn = [
        #             [InlineKeyboardButton("📥 Click here 📥 ", url=link)],
        #             [InlineKeyboardButton('🔰 How to use the bot 🔰', url=full_tut_url)]
        #         ]
        #         await message.reply(f"👉 Your Ads token is expired, refresh your token and try again.🔃 \n\n🎟️  Token Timeout: {get_exp_time(VERIFY_EXPIRE)} ⏲️\n\n<blockquote><b>What is the token?</b>\n\nThis is an ads token.🎟️ If you pass 1 ad, you can use the bot for 24 Hour⏲️  after passing the ad.</blockquote>", reply_markup=InlineKeyboardMarkup(btn), protect_content=False, quote=True)

# ... (rest of the code remains unchanged)



    
        
#=====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

#=====================================================================================##

    
    
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(
                "Join Channel",
                url = client.invitelink),
            InlineKeyboardButton(
                "Join Channel",
                url = client.invitelink2),
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = 'Try Again',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
