import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from config import OWNER_ID


@app.on_message(filters.command("banall") & filters.group & filters.user(OWNER_ID))
async def banall_command(client: Client, message):
    chat_id = message.chat.id

    # ✅ Bot info
    me = await client.get_me()
    bot = await client.get_chat_member(chat_id, me.id)

    # ❌ Permission check
    if not (bot.privileges and bot.privileges.can_restrict_members):
        return await message.reply_text(
            "» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ʙᴀɴ ᴍᴇᴍʙᴇʀs!"
        )

    # ✅ Start message
    user_mention = message.from_user.mention
    msg = await message.reply_text(
        f"» sᴛᴀʀᴛᴇᴅ ʙᴀɴᴀʟʟ ʙʏ :- {user_mention}"
    )

    count = 0
    owner_id = message.from_user.id

    # 🔁 Loop all members
    async for m in client.get_chat_members(chat_id):
        if not m.user:
            continue

        user_id = m.user.id

        # ❌ Skip owner & bot
        if user_id in [owner_id, me.id]:
            continue

        try:
            await client.ban_chat_member(chat_id, user_id)
            count += 1

        except FloodWait as e:
            await asyncio.sleep(e.value)

        except Exception:
            pass

    # ✅ Done
    await msg.delete()
    await message.reply_text(
        f"» ʙᴀɴᴀʟʟ ᴄᴏᴍᴘʟᴇᴛᴇᴅ\n» ʙᴀɴɴᴇᴅ : {count} users"
    )
