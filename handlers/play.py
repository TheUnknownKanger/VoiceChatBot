from os import path

from pyrogram import Client
from pyrogram.types import Message, Voice

import callsmusic

import converter
import youtube
import queues
import cache.admins
from config import DURATION_LIMIT
from helpers.errors import DurationLimitError
from helpers.filters import command, other_filters
from helpers.wrappers import errors,admins_only


@Client.on_message(command("play") & other_filters)
@errors
async def play(_, message: Message):
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None

    res = await message.reply_text("🔄 Processing...")

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"Videos longer than {DURATION_LIMIT} minute(s) aren't allowed, the provided video is {audio.duration / 60} minute(s)"
            )

        file_name = audio.file_unique_id + "." + (
            audio.file_name.split(".")[-1] if not isinstance(audio, Voice) else "ogg"
        )
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    else:
        messages = [message]
        text = ""
        offset = None
        length = None

        if message.reply_to_message:
            messages.append(message.reply_to_message)

        for _message in messages:
            if offset:
                break

            if _message.entities:
                for entity in _message.entities:
                    if entity.type == "url":
                        text = _message.text or _message.caption
                        offset, length = entity.offset, entity.length
                        break

        if offset in (None,):
            await res.edit_text("❕ You did not give me anything to play.")
            return

        url = text[offset:offset + length]
        lel = url
        results = YoutubeSearch(lel,max_results=3).to_dict()
        i = 0
        texxt = ""
        while i < 1:
            texxt += f"Title - {results[i]['title']}\n"
            texxt += f"Duration - {results[i]['duration']}\n"
            texxt += f"Views - {results[i]['views']}\n"
            texxt += f"Channel - {results[i]['channel']}\n"
            texxt += f"https://youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        print(texxt) 

        file_path = await converter.convert(youtube.download(url))

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = queues.add(message.chat.id, file_path,texxt)
        await res.edit_text(f"#️⃣ Queued at position {position}.")
    else:
        img = Image.open("./downloads/1.jpg")
        draw = ImageDraw.Draw(img)
        image_widthz, image_heightz = img.size
        pointsize = 500
        fillcolor = "white"
        shadowcolor = "black"

        text = texxt

        font = ImageFont.truetype("./downloads/VampireWars.ttf",130)
        w,h = draw.textsize(text, font=font)
        h += int(h*0.21)

        image_width, image_height = img.size

        draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
        x = (image_widthz-w)/2
        y= (image_heightz-h)/2
        draw.text((x, y), text, font=font, fill="white", stroke_width=6, stroke_fill="black")
        pate = fname2
        await client.send_photo(message.chat.id, pate,f"▶️Daisy Music Now Playing...\n{texxt}")
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path, 48000, callsmusic.pytgcalls.get_cache_peer())
        os.remove(fname2)

    
