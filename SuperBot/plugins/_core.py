# SuperBot
# made for SuperBot

import asyncio
import os
from datetime import datetime
from pathlib import Path

from SuperBot import ALIVE_NAME
from SuperBot import bot 
from SuperBot.utils import admin_cmd, load_module, remove_plugin, sudo_cmd
from SuperBot.utils import edit_or_reply as eor

DELETE_TIMEOUT = 3
thumb_image_path = "./Resources/SuperBot4.jpg"
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "SuperBot"


@bot.on(admin_cmd(pattern=r"send (?P<shortname>\w+)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"send (?P<shortname>\w+)", allow_sudo=True))
async def send(event):
    if event.fwd_from:
        return
    hmm = bot.uid
    message_id = event.message.id
    thumb = thumb_image_path
    input_str = event.pattern_match.group(1)
    the_plugin_file = "./SuperBot/plugins/{}.py".format(input_str)
    if os.path.exists(the_plugin_file):
        start = datetime.now()
        pro = await event.client.send_file(
            event.chat_id,
            the_plugin_file,
            force_document=True,
            allow_cache=False,
            thumb=thumb,
            reply_to=message_id,
        )
        end = datetime.now()
        time_taken_in_ms = (end - start).seconds
        await eor(
            pro,
            f"**ยปยปยป ๐๐ก๐ช๐๐๐ฃ ๐๐๐ข๐ :** `{input_str}`\n**ยปยปยป ๐๐ฅ๐ก๐ค๐๐๐๐ ๐๐ฃ :** `{time_taken_in_ms} ๐บ๐๐๐๐๐๐`.\n**ยปยปยป ๐๐ฅ๐ก๐ค๐๐๐๐ ๐ฝ๐ฎ :** `{DEFAULTUSER}`\n",
        )
        await asyncio.sleep(DELETE_TIMEOUT)
        await event.edit("๐๐๐ง๐ญ โโโ") # only italic if loaded markdown else it doesn't look grp
    else:
        await eor(event, "**Sฯษพษพแง :** ๐ญ๐๐๐ ๐๐๐ ๐ญ๐๐๐๐")


@bot.on(admin_cmd(pattern="install -true"))
@bot.on(sudo_cmd(pattern="install -true", allow_sudo=True))
async def install(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = (
                await event.client.download_media(  # pylint:disable=E0602
                    await event.get_reply_message(),
                    "SuperBot/plugins/",  # pylint:disable=E0602
                )
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await eor(
                    event,
                    "๐บ๐๐๐๐๐๐๐๐๐๐๐ ๐ฐ๐๐๐๐๐๐๐ {}".format(
                        os.path.basename(downloaded_file_name)
                    ),
                )
            else:
                os.remove(downloaded_file_name)
                await eor(
                    event,
                    "**ฦษพษพฯษพ โโ**\n\n๐ท๐๐๐๐๐ ๐๐๐๐๐๐ ๐๐ ๐๐๐๐๐๐๐๐โ\n๐ด๐๐๐๐ ๐๐๐๐ ๐๐๐๐ ๐๐๐๐๐๐๐๐ ๐๐๐๐๐๐๐๐๐๐.",
                )
        except Exception as e:  # pylint:disable=C0103,W0703
            await eor(event, str(e))
            os.remove(downloaded_file_name)
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()


@bot.on(admin_cmd(pattern=r"unload (?P<shortname>\w+)$"))
@bot.on(sudo_cmd(pattern=r"unload (?P<shortname>\w+)$", allow_sudo=True))
async def unload(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match["shortname"]
    try:
        remove_plugin(shortname)
        qwe = await eor(event, f"{shortname} ๐ผ๐๐๐๐๐๐๐ ๐บ๐๐๐๐๐๐๐๐๐๐๐  ๐๐ ๐บ๐๐๐๐๐ฉ๐๐.")
    except Exception as e:
        await qwe.edit(
            "{shortname} ๐ผ๐๐๐๐๐๐๐ ๐บ๐๐๐๐๐๐๐๐๐๐๐ ๐๐ ๐บ๐๐๐๐๐ฉ๐๐.\n{}".format(shortname, str(e))
        )๐บ๐๐๐๐๐๐๐๐๐๐๐  


@bot.on(admin_cmd(pattern=r"load (?P<shortname>\w+)$"))
@bot.on(sudo_cmd(pattern=r"load (?P<shortname>\w+)$", allow_sudo=True))
async def load(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match["shortname"]
    try:
        try:
            remove_plugin(shortname)
        except BaseException:
            pass
        load_module(shortname)
        qwe = await eor(event, f"{shortname} ๐ณ๐๐๐๐๐ ๐บ๐๐๐๐๐๐๐๐๐๐๐ ๐๐ ๐บ๐๐๐๐๐ฉ๐๐.")
    except Exception as e:
        await qwe.edit(
            f"{shortname} ๐๐๐โ๐ ๐๐ ๐๐๐๐๐๐ ๐๐ ๐บ๐๐๐๐๐ฉ๐๐\n๐ช๐๐ ๐๐ ๐๐ ๐ฌ๐๐๐๐\n\n{str(e)}"
        )

# SuperBot
# made for SuperBot
