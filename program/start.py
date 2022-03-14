"""
Video + Music Stream Telegram Bot
Copyright (c) 2022-present levina=lab <https://github.com/levina-lab>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but without any warranty; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/licenses.html>
"""


import asyncio

from datetime import datetime
from sys import version_info
from time import time

from config import (
    ALIVE_IMG,
    ALIVE_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_USERNAME,
    UPDATES_CHANNEL,
)
from driver.decorators import check_blacklist
from program import __version__, LOGS
from driver.core import bot, me_bot, me_user
from driver.filters import command
from driver.database.dbchat import add_served_chat, is_served_chat
from driver.database.dbpunish import is_gbanned_user
from driver.database.dbusers import add_served_user, is_served_user
from driver.database.dblockchat import blacklisted_chats

from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait, ChatAdminRequired
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
@check_blacklist()
async def start_(c: Client, message: Message):
    user_id = message.from_user.id
    if await is_served_user(user_id):
        pass
    else:
        await add_served_user(user_id)
        return
    await message.reply_text(
        f"""**━━━━━━━━━━━━━━━━━━
🖤 ʜᴇʏ {message.from_user.mention()} !

         ɪ ᴀᴍ sᴜᴘᴇʀ ғᴀsᴛ ᴠᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘs...
ᴀʟʟ ᴏꜰ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : /
┏━━━━━━━━━━━━━━┓
┣★
┣★ ᴄʀᴇᴀᴛᴏʀ: [🖤 ᴀʙʜɪᴍᴀɴʏᴜ 🖤](t.me/Itz_VeNom_xD)
┣★
┗━━━━━━━━━━━━━━┛

💞 ɪғ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ǫᴜᴇsᴛɪᴏɴs ᴛʜᴇɴ ᴅᴍ ᴛᴏ ᴍʏ [ᴏᴡɴᴇʀ](t.me/Itz_VeNom_xD) ʙᴀʙʏ...
━━━━━━━━━━━━━━━━━━**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🖤   ᴋɪᴅɴᴀᴘ ᴍᴇ   🖤",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton("🦋 ʜᴇʟᴘ ", callback_data="command_list"),
                    InlineKeyboardButton("ᴏᴡɴᴇʀ 🦋", url=f"https://t.me/Itz_VeNom_xD"),
                ],
                [
                    InlineKeyboardButton(
                        "🖤 ᴏꜰꜰɪᴄɪᴀʟ ɢʀᴏᴜᴘ", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "ᴏꜰꜰɪᴄɪᴀʟ ᴄʜᴀɴɴᴇʟ 🖤", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_message(
    command(["alive", f"alive@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
@check_blacklist()
async def alive(c: Client, message: Message):
    chat_id = message.chat.id
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✨ ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{GROUP_SUPPORT}"),
                InlineKeyboardButton(
                    "📣 ᴜᴘᴅᴀᴛᴇꜱ", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
            ]
        ]
    )

    alive = f"**ʜᴇʟʟᴏ {message.from_user.mention()}, ɪ'ᴍ {me_bot.first_name}**\n\n🧑🏼‍💻 ᴍʏ ᴍᴀꜱᴛᴇʀ: [{ALIVE_NAME}](https://t.me/{OWNER_USERNAME})\n👾 ʙᴏᴛ ᴠᴇʀꜱɪᴏɴ: `v{__version__}`\n🔥 ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀꜱɪᴏɴ: `{pyrover}`\n🐍 ᴘʏᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ: `{__python_version__}`\n✨ ᴘʏᴛɢᴄᴀʟʟꜱ ᴠᴇʀꜱɪᴏɴ: `{pytover.__version__}`\n🆙 ᴜᴘᴛɪᴍᴇ: `{uptime}`\n\n❤ **ᴛʜᴀɴᴋꜱ ꜰᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ʜᴇʀᴇ, ꜰᴏʀ ᴘʟᴀʏɪɴɢ ᴠɪᴅᴇᴏ ɴᴅ ᴍᴜꜱɪᴄ ᴏɴ ᴜʀ ɢʀᴘ's ᴠᴏɪᴄᴇ ᴄʜᴀᴛ**"

    await c.send_photo(
        chat_id,
        photo=f"{ALIVE_IMG}",
        caption=alive,
        reply_markup=keyboard,
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
@check_blacklist()
async def ping_pong(c: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("🌸 `ᴘᴏɴɢ!!`\n" f"⚡️ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@check_blacklist()
async def get_uptime(c: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 bot status:\n"
        f"• **uptime:** `{uptime}`\n"
        f"• **start time:** `{START_TIME_ISO}`"
    )


@Client.on_chat_join_request()
async def approve_join_chat(c: Client, m: ChatJoinRequest):
    if not m.from_user:
        return
    try:
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)
    except FloodWait as e:
        await asyncio.sleep(e.x + 2)
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)


@Client.on_message(filters.new_chat_members)
async def new_chat(c: Client, m: Message):
    chat_id = m.chat.id
    if await is_served_chat(chat_id):
        pass
    else:
        await add_served_chat(chat_id)
    for member in m.new_chat_members:
        try:
            if member.id == me_bot.id:
                if chat_id in await blacklisted_chats():
                    await m.reply_text(
                        "❗️ This chat has blacklisted by sudo user and You're not allowed to use me in this chat."
                    )
                    return await bot.leave_chat(chat_id)
            if member.id == me_bot.id:
                return await m.reply(
                    "❤️ ᴛʜᴀɴᴋꜱ ꜰᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ᴛᴏ ᴛʜᴇ  **ɢʀᴏᴜᴘ** !\n\n"
                    "Aᴘᴘᴏɪɴᴛ ᴍᴇ ᴀꜱ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ **ɢʀᴏᴜᴘ**, ᴏᴛʜᴇʀᴡɪꜱᴇ ɪ ᴡɪʟʟ ɴᴏᴛ ʙᴇ ᴀʙʟᴇ ᴛᴏ ᴡᴏʀᴋ ᴘʀᴏᴘᴇʀʟʏ, ᴀɴᴅ ᴅᴏɴ'ᴛ ꜰᴏʀɢᴇᴛ ᴛᴏ ᴛʏᴘᴇ `/userbotjoin` ꜰᴏʀ ɪɴᴠɪᴛᴇ ᴛʜᴇ ᴀꜱꜱɪꜱᴛᴀɴᴛ.\n\n"
                    "Oɴᴄᴇ ᴅᴏɴᴇ, ᴛʜᴇɴ ᴛʏᴘᴇ `/reload`",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🖤 ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{UPDATES_CHANNEL}"),
                                InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇꜱ 🖤", url=f"https://t.me/{GROUP_SUPPORT}")
                            ],[
                                InlineKeyboardButton("🖤 ᴀꜱꜱɪꜱᴛᴀɴᴛ 🖤", url=f"https://t.me/{me_user.username}")
                            ]
                        ]
                    )
                )
            return
        except BaseException:
            return


chat_watcher_group = 5

@Client.on_message(group=chat_watcher_group)
async def chat_watcher_func(_, message: Message):
    userid = message.from_user.id
    suspect = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_gbanned_user(userid):
        try:
            await message.chat.ban_member(userid)
        except ChatAdminRequired:
            LOGS.info(f"can't remove gbanned user from chat: {message.chat.id}")
            return
        await message.reply_text(
            f"👮🏼 (> {suspect} <)\n\n**Gbanned** user detected, that user has been gbanned by sudo user and was blocked from this Chat !\n\n🚫 **Reason:** potential spammer and abuser."
        )
