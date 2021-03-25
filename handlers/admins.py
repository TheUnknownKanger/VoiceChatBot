import queue

from pyrogram import Client
from pyrogram.types import Message

import callsmusic

import queues
import cache.admins

from helpers.filters import command
from helpers.wrappers import errors, admins_only


@Client.on_message(command(["pause"]))
@errors
@admins_only
async def pause(_, message: Message):
    if (
            message.chat.id not in callsmusic.pytgcalls.active_calls
    ) or (
            callsmusic.pytgcalls.active_calls[message.chat.id] == 'paused'
    ):
        await message.reply_text("❕ Nothing is playing.")
    else:
        callsmusic.pytgcalls.pause_stream(message.chat.id)
        await message.reply_text("⏸ Paused.")


@Client.on_message(command(["resume"]))
@errors
@admins_only
async def resume(_, message: Message):
    if (
            message.chat.id not in callsmusic.pytgcalls.active_calls
    ) or (
            callsmusic.pytgcalls.active_calls[message.chat.id] == 'playing'
    ):
        await message.reply_text("❕ Nothing is paused.")
    else:
        callsmusic.pytgcalls.resume_stream(message.chat.id)
        await message.reply_text("▶️ Resumed.")


@Client.on_message(command(["end", "stopvc"]))
@errors
@admins_only
async def stop(_, message: Message):
    if message.chat.id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❕ Nothing is streaming.")
    else:
        try:
            queues.clear(message.chat.id)
        except queue.Empty:
            pass

        callsmusic.pytgcalls.leave_group_call(message.chat.id)
        await message.reply_text("⏹ Stopped streaming.")


@Client.on_message(command(["skip"]))
@errors
@admins_only
async def skip(_, message: Message):
    if message.chat.id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❕ Nothing is playing to skip.")
    else:
        queues.task_done(message.chat.id)

        if queues.is_empty(message.chat.id):
            callsmusic.pytgcalls.leave_group_call(message.chat.id)
        else:
            callsmusic.pytgcalls.change_stream(message.chat.id, queues.get(message.chat.id)["file_path"])

        await message.reply_text("⏩ Skipped the current song.")


@Client.on_message(command("adminscache"))
@errors
@admins_only
async def admincache(_, message: Message):
    cache.admins.set(
        message.chat.id,
        [member.user for member in await message.chat.get_members(filter="administrators")]
    )
    await message.reply_text("❇ Admin cache refreshed!")
    
@Client.on_message(command(["cpause"]))
@errors
@admins_only
async def play(_, message: Message):
    try:
        cmd, text = message.text.split(" ", 1)
    except:
        await message.reply_text(
            "Enter in correct format. @Username or chai id
        )
        return
    try:
        if not text.startswith("@"):
            chid = int(text)
            chatdetails = chid
            if not len(text) == 14:
                await message.reply_text(
                    "Enter valid channel ID"
                )
                return
        elif text.startswith("@"):
            chid = text
            if not len(chid) > 2:
                await message.reply_text(
                    "Enter valid channel username"
                )                
                
    except Exception:
        await message.reply_text(
            "Enter a valid ID\n"
            "Correct syntax : <b>-100xxxxxxxxxx</b>\n"
            "Or use @Username of Channel",
        )
        return

    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Add me as admin of yor channel first</b>",
        )
        return

    if chid.startswith("@"):
        try:
            chatdetails = await client.get_chat(chid)
            channel_id = chatdetails.id
        except:
            await message.reply_text(
                "<i>Send a message to your channel and try again</i>"
            )
            return
    else:
        channel_id = chid    
    if (
            channel_id not in callsmusic.pytgcalls.active_calls
    ) or (
            callsmusic.pytgcalls.active_calls[channel_id] == 'paused'
    ):
        await message.reply_text("❕ Nothing is playing.")
    else:
        callsmusic.pytgcalls.pause_stream(channel_id)
        await message.reply_text("⏸ Paused.")

        
@Client.on_message(command(["cresume"]))
@errors
@admins_only
async def play(_, message: Message):
    try:
        cmd, text = message.text.split(" ", 1)
    except:
        await message.reply_text(
            "Enter in correct format. @Username or chai id
        )
        return
    try:
        if not text.startswith("@"):
            chid = int(text)
            chatdetails = chid
            if not len(text) == 14:
                await message.reply_text(
                    "Enter valid channel ID"
                )
                return
        elif text.startswith("@"):
            chid = text
            if not len(chid) > 2:
                await message.reply_text(
                    "Enter valid channel username"
                )                
                
    except Exception:
        await message.reply_text(
            "Enter a valid ID\n"
            "Correct syntax : <b>-100xxxxxxxxxx</b>\n"
            "Or use @Username of Channel",
        )
        return

    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Add me as admin of yor channel first</b>",
        )
        return

    if chid.startswith("@"):
        try:
            chatdetails = await client.get_chat(chid)
            channel_id = chatdetails.id
        except:
            await message.reply_text(
                "<i>Send a message to your channel and try again</i>"
            )
            return
    else:
        channel_id = chid  
    if (
            channel_id not in callsmusic.pytgcalls.active_calls
    ) or (
            callsmusic.pytgcalls.active_calls[channel_id] == 'playing'
    ):
        await message.reply_text("❕ Nothing is paused.")
    else:
        callsmusic.pytgcalls.resume_stream(channel_id)
        await message.reply_text("▶️ Resumed.")
        
        
@Client.on_message(command(["cskip"]))
@errors
@admins_only
async def play(_, message: Message):
    try:
        cmd, text = message.text.split(" ", 1)
    except:
        await message.reply_text(
            "Enter in correct format. @Username or chai id
        )
        return
    try:
        if not text.startswith("@"):
            chid = int(text)
            chatdetails = chid
            if not len(text) == 14:
                await message.reply_text(
                    "Enter valid channel ID"
                )
                return
        elif text.startswith("@"):
            chid = text
            if not len(chid) > 2:
                await message.reply_text(
                    "Enter valid channel username"
                )                
                
    except Exception:
        await message.reply_text(
            "Enter a valid ID\n"
            "Correct syntax : <b>-100xxxxxxxxxx</b>\n"
            "Or use @Username of Channel",
        )
        return

    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Add me as admin of yor channel first</b>",
        )
        return

    if chid.startswith("@"):
        try:
            chatdetails = await client.get_chat(chid)
            channel_id = chatdetails.id
        except:
            await message.reply_text(
                "<i>Send a message to your channel and try again</i>"
            )
            return
    else:
        channel_id = chid  
    if channel_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❕ Nothing is playing to skip.")
    else:
        queues.task_done(channel_id)

        if queues.is_empty(channel_id):
            callsmusic.pytgcalls.leave_group_call(channel_id)
        else:
            callsmusic.pytgcalls.change_stream(channel_id, queues.get(message.chat.id)["file_path"])

        await message.reply_text("⏩ Skipped the current song.")
        
        
        
@Client.on_message(command(["cend"]))
@errors
@admins_only
async def play(_, message: Message):
    try:
        cmd, text = message.text.split(" ", 1)
    except:
        await message.reply_text(
            "Enter in correct format. @Username or chai id
        )
        return
    try:
        if not text.startswith("@"):
            chid = int(text)
            chatdetails = chid
            if not len(text) == 14:
                await message.reply_text(
                    "Enter valid channel ID"
                )
                return
        elif text.startswith("@"):
            chid = text
            if not len(chid) > 2:
                await message.reply_text(
                    "Enter valid channel username"
                )                
                
    except Exception:
        await message.reply_text(
            "Enter a valid ID\n"
            "Correct syntax : <b>-100xxxxxxxxxx</b>\n"
            "Or use @Username of Channel",
        )
        return

    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Add me as admin of yor channel first</b>",
        )
        return

    if chid.startswith("@"):
        try:
            chatdetails = await client.get_chat(chid)
            channel_id = chatdetails.id
        except:
            await message.reply_text(
                "<i>Send a message to your channel and try again</i>"
            )
            return
    else:
        channel_id = chid  
        
    if channel_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❕ Nothing is streaming.")
    else:
        try:
            queues.clear(channel_id)
        except queue.Empty:
            pass

        callsmusic.pytgcalls.leave_group_call(channel_id)
        await message.reply_text("⏹ Stopped streaming.")
