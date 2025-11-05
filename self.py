import os, random, psutil, json, pytz, aiocron, asyncio, aiofiles, aiohttp, numpy, sys
from telethon.sync import TelegramClient, events, types
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.account import UpdateStatusRequest, GetAuthorizationsRequest, UpdateProfileRequest
from telethon.tl.functions.messages import SendScreenshotNotificationRequest, SendReactionRequest
from telethon.tl.functions.phone import CreateGroupCallRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from gtts import gTTS
from googletrans import Translator
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from google_play_scraper import search
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import google.generativeai as genai
from config import API_ID, API_HASH, GEMINI_API_KEY, LOG_CHANNEL_ID

async def get(f):
    async with aiofiles.open(f, 'r') as r:
        return json.loads(await r.read())

async def put(f, d):
    async with aiofiles.open(f, 'w') as w:
        await w.write(json.dumps(d))

def font(t):
    return t.lower().translate(t.maketrans('qwertyuiopasdfghjklzxcvbnm', 'ǫᴡᴇʀᴛʏᴜɪᴏᴘᴀsᴅғɢʜᴊᴋʟᴢxᴄᴠʙɴᴍ'))

async def requests(u, **kw):
    async with aiohttp.ClientSession() as s:
        async with s.get(u, **kw) as r:
            try: return json.loads(await r.text())
            except: return await r.read()

loop = asyncio.get_event_loop()

if not os.path.exists('data.json'):
    d = {'timename': 'off', 'timebio': 'off', 'timeprofile': 'off', 'timecrush': 'off', 'bot': 'on', 'hashtag': 'off', 'bold': 'off', 'italic': 'off', 'delete': 'off', 'code': 'off', 'underline': 'off', 'reverse': 'off', 'part': 'off', 'mention': 'off', 'spoiler': 'off', 'comment': 'on', 'text': 'first !', 'typing': 'off', 'game': 'off', 'voice': 'off', 'video': 'off', 'sticker': 'off', 'crush': [], 'enemy': [], 'afk': {'status': 'off', 'reason': '', 'time': 0}, 'notes': {}}
    loop.run_until_complete(put('data.json', d))

helperbot = 'helperselfbot'
bot = TelegramClient('self', API_ID, API_HASH, loop=loop)

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
else:
    gemini_model = None

async def makeClock(h, m, s, r, w):
    img = plt.imread(r)
    fig = plt.figure(figsize=(4, 4), dpi=300, facecolor=[0.2, 0.2, 0.2])
    ax_img = fig.add_axes([0, 0, 1, 1]); ax_img.axis('off'); ax_img.imshow(img)
    axc = fig.add_axes([0.062, 0.062, 0.88, 0.88], projection='polar')
    axc.cla(); axc.axis('off'); axc.set_theta_zero_location('N'); axc.set_theta_direction(-1)
    sec = numpy.multiply(numpy.ones(5), s * 2 * numpy.pi / 60)
    minu = numpy.multiply(numpy.ones(5), m * 2 * numpy.pi / 60) + (sec / 60)
    hrs = numpy.multiply(numpy.ones(5), h * 2 * numpy.pi / 12) + (minu / 12)
    axc.plot(hrs, numpy.linspace(0.00, 0.70, 5), c='c', linewidth=2.0)
    axc.plot(minu, numpy.linspace(0.00, 0.85, 5), c='b', linewidth=1.5)
    axc.plot(sec, numpy.linspace(0.00, 1.00, 5), c='r', linewidth=1.0)
    axc.plot(minu, numpy.linspace(0.73, 0.83, 5), c='w', linewidth=1.0)
    axc.plot(hrs, numpy.linspace(0.60, 0.68, 5), c='w', linewidth=1.5)
    axc.plot(sec, numpy.linspace(0.80, 0.98, 5), c='w', linewidth=0.5)
    axc.set_rmax(1); plt.savefig(w)
    return w

@aiocron.crontab('*/1 * * * *')
async def clock():
    await bot(UpdateStatusRequest(offline=False))
    js = await get('data.json')
    if all(js.get(k) == 'off' for k in ['timename', 'timebio', 'timeprofile', 'timecrush']): return
    now = datetime.now(pytz.timezone('Asia/Tehran')).strftime('%H:%M:%S')
    h, m, s = list(map(int, now.split(':')))
    t = f'【 {h}:{m} 】'
    fonts = t.translate(t.maketrans('0123456789', random.choice(['⓪➀➁➂➃➄➅➆➇➈', '𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗'])))
    if js['timecrush'] == 'on' and h == m:
        for f_id in js['crush']: await bot.send_message(f_id, f'ɪ ʟᴏᴠᴇ ʏᴏᴜ 🙂❤️ {fonts}')
    if js['timename'] == 'on': await bot(UpdateProfileRequest(last_name=fonts))
    if js['timebio'] == 'on': await bot(UpdateProfileRequest(about=f'❦ 𝒀𝒐𝒖 𝒄𝒂𝒏 𝒔𝒆𝒆 𝒎𝒚 𝒈𝒐𝒐𝒅 𝒇𝒂𝒄𝒆 𝒐𝒓 𝒎𝒚 𝒆𝒗𝒊𝒍 𝒇𝒂𝒄𝒆 ❦ {fonts}'))
    if js['timeprofile'] == 'on':
        build = await makeClock(h, m, s, 'clock.jpg', 'oclock.jpg')
        photo = await bot.upload_file(build)
        photos = await bot.get_profile_photos('me')
        if photos and datetime.now(pytz.timezone('UTC')) - photos[0].date < timedelta(minutes=10):
            await bot(DeletePhotosRequest(id=[types.InputPhoto(id=photos[0].id, access_hash=photos[0].access_hash, file_reference=photos[0].file_reference)]))
        await bot(UploadProfilePhotoRequest(file=photo, fallback=True))

async def get_user_id(event):
    if event.is_reply:
        return (await event.get_reply_message()).sender.id
    try:
        if len(event.raw_text.split()) > 1:
            user = event.raw_text.split()[1]
            e = await bot.get_input_entity(int(user) if user.isdigit() else user)
            return e.user_id
    except: pass
    if event.is_private: return event.chat_id
    return None

def get_timedelta_str(t):
    s = (datetime.now() - datetime.fromtimestamp(t)).total_seconds()
    if s < 60: return f"{int(s)} seconds ago"
    if s < 3600: return f"{int(s // 60)} minutes ago"
    if s < 86400: return f"{int(s // 3600)} hours ago"
    return f"{int(s // 86400)} days ago"

@bot.on(events.NewMessage(pattern=r'\.afk(?: (.*))?', outgoing=True))
async def afk_handler(event):
    reason = event.pattern_match.group(1) or "I'm currently away."
    js = await get('data.json')
    js['afk'] = {"status": "on", "reason": reason, "time": datetime.now().timestamp()}
    await put('data.json', js)
    await event.edit(f"**AFK Mode Enabled** ✅\nReason: {reason}")

@bot.on(events.NewMessage(incoming=True, func=lambda e: e.is_private or e.mentioned))
async def afk_reply(event):
    js = await get('data.json')
    if js.get('afk', {}).get('status') == 'on':
        sender = await event.get_sender()
        if sender and (sender.bot or sender.is_self): return
        reason = js['afk']['reason']
        since = get_timedelta_str(js['afk']['time'])
        await event.reply(f"**I'm currently AFK.** (Since {since})\n\nReason: {reason}\n\n_This is an automated message._")

@bot.on(events.NewMessage(outgoing=True, func=lambda e: not e.raw_text.startswith(('.afk', '.save', '.notes', '.delnote'))))
async def disable_afk(event):
    js = await get('data.json')
    if js.get('afk', {}).get('status') == 'on':
        js['afk']['status'] = 'off'
        await put('data.json', js)
        await event.respond("**AFK Mode Disabled** ❌")

@bot.on(events.NewMessage(pattern=r'\.save (\w+)(?: (.*))?', outgoing=True))
async def save_note(event):
    k, t = event.pattern_match.groups()
    if not t and event.is_reply: t = (await event.get_reply_message()).raw_text
    if not t: return await event.edit(f"**Error:** Provide text or reply to a message.`.save <keyword> <text>`")
    js = await get('data.json')
    js.setdefault('notes', {})[k] = t
    await put('data.json', js)
    await event.edit(f"**Note Saved!** 📝\nKeyword: `{k}`")

@bot.on(events.NewMessage(pattern=r'\.(notes|listnotes)', outgoing=True))
async def list_notes(event):
    notes = (await get('data.json')).get('notes', {})
    if not notes: return await event.edit("**No notes saved.** ℹ️\nUse `.save <keyword> <text>` to add one.")
    await event.edit("**Saved Notes:**\n\n" + "\n".join(f"• `{k}`" for k in notes))

@bot.on(events.NewMessage(pattern=r'\.delnote (\w+)', outgoing=True))
async def del_note(event):
    k = event.pattern_match.group(1); js = await get('data.json')
    if 'notes' in js and k in js['notes']:
        del js['notes'][k]; await put('data.json', js)
        await event.edit(f"**Note Deleted!** 🗑️\nKeyword: `{k}`")
    else: await event.edit(f"**Error:** Note `{k}` not found.")

@bot.on(events.NewMessage(pattern=r'#(\w+)', outgoing=True))
async def use_note(event):
    k = event.pattern_match.group(1)
    if event.raw_text.strip() != f"#{k}": return
    n = (await get('data.json')).get('notes', {}).get(k)
    if n: await event.edit(n)

@bot.on(events.NewMessage(pattern=r'\.ask (.*)', outgoing=True))
async def ask_gemini(event):
    if not gemini_model: return await event.edit("**Error:** Gemini AI is not configured. Set `GEMINI_API_KEY`.")
    p = event.pattern_match.group(1)
    await event.edit(f"**Asking Gemini...** 🧠\n`{p}`")
    try:
        r = await gemini_model.generate_content_async(p)
        await event.edit(r.text)
    except Exception as e:
        await event.edit(f"**Gemini AI Error:**\n`{str(e)}`")

@bot.on(events.NewMessage(outgoing=True))
async def mode(event):
    js = await get('data.json'); t = event.raw_text
    if t:
        try:
            m = {'hashtag': f'#{t.replace(" ", "_")}', 'bold': f'<b>{t}</b>', 'italic': f'<i>{t}</i>', 'delete': f'<del>{t}</del>', 'code': f'<code>{t}</code>', 'underline': f'<u>{t}</u>'}
            if js['reverse'] == 'on': await event.edit(t[::-1], parse_mode='HTML')
            elif js['part'] == 'on' and len(t) > 1:
                for new in (t[:i+1] for i in range(len(t)) if t[i] != ' '): await event.edit(new, parse_mode='HTML')
            elif js['mention'] == 'on' and event.is_reply:
                await event.edit(f'<a href =\'tg://openmessage?user_id={(await event.get_reply_message()).sender.id}\'>{t}</a>', parse_mode='HTML')
            elif js['spoiler'] == 'on': await event.edit(f'<tg-spoiler>{t}</tg-spoiler>', parse_mode='HTML')
            elif any(js[k] == 'on' for k in m):
                k = next(k for k in m if js[k] == 'on')
                await event.edit(m[k], parse_mode='HTML' if k not in ['hashtag'] else None)
        except Exception as e: print(e)

@bot.on(events.NewMessage())
async def updateMessage(event):
    js = await get('data.json'); f_id = event.sender_id
    if f_id in js['enemy'] and event.is_private: await event.delete()
    elif f_id in js['crush'] and event.is_group:
        try: await bot(SendReactionRequest(event.chat_id, event.message.id, [types.ReactionEmoji('❤️')]))
        except: await event.reply(random.choice(['🤍', '🖤', '💜', '💙', '💚', '💛', '🧡', '❤️', '🤎', '💖']))
        await event.forward_to('me')
    elif js['comment'] == 'on' and event.fwd_from and event.fwd_from.saved_from_peer and event.from_id:
        await event.reply(js['text'])

@bot.on(events.ChatAction)
async def chatAction(event):
    if event.user_joined: await event.reply('ɪ\'ᴍ ᴡᴇʟᴄᴏᴍᴇᴅ !' if event.action_message.out else 'ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ !')
    elif event.new_score: await event.reply('😜 رکورد جدیدی رو زدم !' if event.action_message.out else '😉 رکورد جدید زدی ولی رکوردت به من نمیرسه !')

@bot.on(events.UserUpdate)
async def userUpdate(event):
    if event.is_private:
        if event.uploading: await bot.send_message(event.user_id, '🤔 چی داری میفرستی ؟')
        elif event.playing: await bot.send_message(event.user_id, '🤔 چی بازی می‌کنی ؟')

@bot.on(events.MessageEdited(outgoing=False, func=lambda e: e.is_private))
async def messageEdited(event):
    if event.message and not event.reactions:
        t = datetime.now(pytz.timezone('Asia/Tehran')).strftime('✐ %H:%M:%S ✎')
        await bot.send_message(event.chat_id, f'<a href =\'tg://openmessage?user_id={event.sender_id}\'>😅 پیامت رو در ساعت {t} ادیت زدی</a>', parse_mode='HTML', reply_to=event.message.id)

@bot.on(events.NewMessage())
async def sendAction(event):
    js = await get('data.json')
    for t in ['typing', 'game', 'voice', 'video', 'sticker']:
        if js[t] == 'on':
            async with bot.action(event.chat_id, t): await asyncio.sleep(2)

@bot.on(events.NewMessage(pattern=r'(robot|ربات)', outgoing=True))
async def roBot(event): await event.edit('ᴛʜᴇ ʀᴏʙᴏᴛ ɪs ᴏɴ !')

@bot.on(events.NewMessage(pattern=r'(help|راهنما)', outgoing=True))
async def help(event):
    p = psutil.Process(os.getpid()); me = await bot.get_me(); js = await get('data.json')
    h = f"нelp мeɴυ {me.first_name}:\n\n"
    for k, v in js.items(): h += f"⟩••• {k.upper().replace('_', ' ')} : {v}\n"
    h += "\n⟩••• .timename (oɴ|oғғ)\n⟩••• .timebio (oɴ|oғғ)\n⟩••• .timeprofile (oɴ|oғғ)\n⟩••• .timecrush (oɴ|oғғ)\n⟩••• .comment (oɴ|oғғ)\n⟩••• .commentText (тeхт)\n\n"
    h += "⟩••• hashtag (oɴ|oғғ)\n⟩••• bold (oɴ|oғғ)\n⟩••• italic (oɴ|oғғ)\n⟩••• delete (oɴ|oғғ)\n⟩••• code (oɴ|oғғ)\n⟩••• underline (oɴ|oғғ)\n⟩••• reverse (oɴ|oғғ)\n⟩••• part (oɴ|oғғ)\n⟩••• mention (oɴ|oғғ)\n⟩••• spoiler (oɴ|oғғ)\n\n"
    h += "⟩••• typing (oɴ|oғғ)\n⟩••• game (oɴ|oғғ)\n⟩••• voice (oɴ|oғғ)\n⟩••• video (oɴ|oғғ)\n⟩••• sticker (oɴ|oғғ)\n\n"
    h += "⟩••• .addenemy (ιd)\n⟩••• .delenemy (ιd)\n⟩••• listenemy\n⟩••• .addcrush (ιd)\n⟩••• .delcrush (ιd)\n⟩••• listcrush\n\n"
    h += "⟩••• .afk (reαѕoɴ)\n⟩••• .save (ĸeyword) (тeхт)\n⟩••• .notes\n⟩••• .delnote (ĸeyword)\n⟩••• #ĸeyword\n⟩••• .ask (proмpт)\n\n"
    h += "⟩••• fun (тeхт)\n⟩••• heart\n⟩••• tagall\n⟩••• tagadmins\n⟩••• checker (тeхт)\n⟩••• download\n\n"
    h += "⟩••• info (ιd)(reply)\n⟩••• status\n⟩••• .clean (ιɴт)\n\n"
    h += f"• ᴍᴇᴍᴏʀʏ ᴜsᴇᴅ : {p.memory_info()[0] / 1073741824:.2f} GB\n• ᴍᴇᴍᴏʀʏ : {psutil.virtual_memory()[2]} %\n• ᴄᴘᴜ : {psutil.cpu_percent(3)} %"
    await event.reply(h)
    results = await bot.inline_query('like', 'ＤＯ ＹＯＵ ＬＩＫＥ ＭＹ ＲＯＢＯＴ ? ')
    await results[0].click(event.chat_id)

@bot.on(events.NewMessage(pattern=r'(panel|پنل)', outgoing=True))
async def panel(event):
    await event.edit('⟩••• ᴏᴘᴇɴɪɴɢ ᴛʜᴇ ᴘᴀɴᴇʟ !')
    results = await bot.inline_query(helperbot, 'panel')
    await results[0].click(event.chat_id)

@bot.on(events.NewMessage(pattern=r'(xo|دوز)', outgoing=True))
async def xo(event):
    await event.edit('⟩••• ᴏᴘᴇɴɪɴɢ ᴛʜᴇ xᴏ !')
    results = await bot.inline_query(helperbot, 'xo')
    await results[0].click(event.chat_id)

@bot.on(events.NewMessage(pattern=r'(dice|تاس) (1|2|3|4|5|6)', outgoing=True))
async def dice(event):
    i = int(event.pattern_match.group(2)); await event.delete()
    send = await bot.send_file(event.chat_id, types.InputMediaDice('🎲'))
    while send.media.value != i:
        await bot.delete_messages(event.chat_id, send.id)
        send = await bot.send_file(event.chat_id, types.InputMediaDice('🎲'))

@bot.on(events.NewMessage(pattern=r'(fun|فان) (.*)', outgoing=True))
async def fun(event):
    i = event.pattern_match.group(2).lower()
    e = {'love': ['🤍', '🖤', '💜', '💙', '💚', '💛', '🧡', '❤️', '🤎', '💖'], 'oclock': ['🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚', '🕛', '🕜', '🕝', '🕞', '🕟', '🕠', '🕡', '🕢', '🕣', '🕤', '🕥', '🕦', '🕧'], 'star': ['💥', '⚡️', '✨', '🌟', '⭐️', '💫'], 'snow': ['❄️', '☃️', '⛄️']}
    emoticons = e.get(i, [])
    if not emoticons: return await event.edit(f'Unknown fun mode: {i}')
    random.shuffle(emoticons)
    for emoji in emoticons:
        await asyncio.sleep(1); await event.edit(emoji)

@bot.on(events.NewMessage(pattern=r'(heart|قلب)', outgoing=True))
async def heart(event):
    for x in range(1, 4):
        for i in range(1, 11): await event.edit('➣ ' + str(x) + ' ❦' * i + ' | ' + str(10 * i) + '%')

@bot.on(events.NewMessage(pattern=r'(clean|حذف) (\d+)', outgoing=True))
async def clean(event):
    i = int(event.pattern_match.group(2))
    m_ids = [m.id async for m in bot.iter_messages(event.chat_id, limit=i)]
    await bot.delete_messages(event.chat_id, m_ids)
    await bot.send_message(event.chat_id, f'{i} мeѕѕαɢeѕ were deleтed . . . !')

@bot.on(events.NewMessage(pattern=r'(addcrush|افزودن کراش)', outgoing=True))
async def addCrush(event):
    g_id = await get_user_id(event)
    if not g_id: return await event.edit('⟩••• ᴄᴀɴɴᴏᴛ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ !')
    js = await get('data.json')
    if g_id in js['crush']: await event.edit(f'• [ᴜsᴇʀ](tg://user?id={g_id}) ᴡᴀs ɪɴ crυѕн ʟɪsᴛ !')
    else:
        js['crush'].append(g_id); await put('data.json', js)
        await event.edit(f'• [ᴜsᴇʀ](tg://user?id={g_id}) ɴᴏᴡ ɪɴ crυѕн ʟɪsᴛ !')

@bot.on(events.NewMessage(pattern=r'(delcrush|حذف کراش)', outgoing=True))
async def delCrush(event):
    g_id = await get_user_id(event)
    if not g_id: return await event.edit('⟩••• ᴄᴀɴɴᴏᴛ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ !')
    js = await get('data.json')
    if g_id in js['crush']:
        js['crush'].remove(g_id); await put('data.json', js)
        await event.edit(f'• [ᴜsᴇʀ](tg://user?id={g_id}) ᴅᴇʟᴇᴛᴇᴅ ғʀᴏᴍ crυѕн ʟɪsᴛ !')
    else: await event.edit(f'• [ᴜsᴇʀ](tg://user?id={g_id}) ɪs ɴᴏᴛ ɪɴ ᴛʜᴇ crυѕн ʟɪsᴛ !')

@bot.on(events.NewMessage(pattern=r'(listcrush|لیست کراش)', outgoing=True))
async def listCrush(event):
    txt = 'crυѕн ʟɪsᴛ :\n'
    for i in (await get('data.json'))['crush']: txt += f'\n• [{i}](tg://user?id={i})'
    await event.edit(txt)

@bot.on(events.NewMessage(pattern=r'(addenemy|افزودن انمی)', outgoing=True))
async def addEnemy(event):
    g_id = await get_user_id(event)
    if not g_id: return await event.edit('⟩••• ᴄᴀɴɴᴏᴛ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ !')
    js = await get('data.json')
    if g_id in js['enemy']: await event.edit(f'• [ᴜsᴇʀ](tg://user?id={g_id}) ᴡᴀs ɪɴ ᴇɴᴇᴍʏ ʟɪsᴛ !')
    else:
        js['enemy'].append(g_id); await put('data.json', js)
        await event.edit(f'• [ᴜsᴇʀ](tg://user?id={g_id}) ɴᴏᴡ ɪɴ ᴇɴᴇᴍʏ ʟɪsᴛ !')

@bot.on(events.NewMessage(pattern=r'(delenemy|حذف انمی)', outgoing=True))
async def delEnemy(event):
    g_id = await get_user_id(event)
    if not g_id: return await event.edit('⟩••• ᴄᴀɴɴᴏᴛ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ !')
    js = await get('data.json')
    if g_id in js['enemy']:
        js['enemy'].remove(g_id); await put('data.json', js)
        await event.edit(f'• [ᴜsᴇʀ](tg://user?id={g_id}) ᴅᴇʟᴇᴛᴇᴅ ғʀᴏᴍ ᴇɴᴇᴍʏ ʟɪsᴛ !')
    else: await event.edit(f'• [ᴜsᴇʀ](tg://user?id={g_id}) ɪs ɴᴏᴛ ɪɴ ᴛʜᴇ ᴇɴᴇᴍʏ ʟɪsᴛ !')

@bot.on(events.NewMessage(pattern=r'(listenemy|لیست انمی)', outgoing=True))
async def listEnemy(event):
    txt = 'ᴇɴᴇᴍʏ ʟɪsᴛ :\n'
    for i in (await get('data.json'))['enemy']: txt += f'\n• [{i}](tg://user?id={i})'
    await event.edit(txt)

@bot.on(events.NewMessage(pattern=r'\.time(name|bio|profile|crush) (on|off)', outgoing=True))
async def timeMode(event):
    k, v = event.pattern_match.groups(); js = await get('data.json')
    js[f'time{k}'] = v; await put('data.json', js)
    await event.edit(f'⟩••• ᴛʜᴇ ᴛɪᴍᴇ {k.upper()} ɴᴏᴡ ɪs {v}')

@bot.on(events.NewMessage(pattern=r'\.comment (on|off)', outgoing=True))
async def comment(event):
    v = event.pattern_match.group(1); js = await get('data.json')
    js['comment'] = v; await put('data.json', js)
    await event.edit(f'⟩••• ᴛʜᴇ coммeɴт ɴᴏᴡ ɪs {v}')

@bot.on(events.NewMessage(pattern=r'\.commentText (.*)', outgoing=True))
async def commentText(event):
    v = event.pattern_match.group(1); js = await get('data.json')
    js['text'] = v; await put('data.json', js)
    await event.edit(f'⟩••• ᴛʜᴇ coммeɴт тeхт ɴᴏᴡ ɪs {v}')

@bot.on(events.NewMessage(pattern=r'(tagall|تگ)', outgoing=True, func=lambda e: e.is_group))
async def tagAll(event):
    mentions = '✅ آخرین افراد آنلاین گروه'
    async for x in bot.iter_participants(event.chat_id, 100):
        mentions += f'\n [{x.first_name}](tg://user?id={x.id})'
    await event.reply(mentions); await event.delete()

@bot.on(events.NewMessage(pattern=r'(tagadmins|تگ ادمین ها)', outgoing=True, func=lambda e: e.is_group))
async def tagAdmins(event):
    mentions = '⚡️ تگ کردن ادمین ها'
    async for x in bot.iter_participants(event.chat_id, filter=types.ChannelParticipantsAdmins):
        mentions += f'\n [{x.first_name}](tg://user?id={x.id})'
    await event.reply(mentions); await event.delete()

@bot.on(events.NewMessage(pattern=r'(report|گزارش)', func=lambda e: e.is_group and e.is_reply))
async def report(event):
    mentions = 'ʏᴏᴜʀ ʀᴇᴘᴏʀᴛ ʜᴀs ʙᴇᴇɴ sᴜᴄᴄᴇssғᴜʟʟʏ sᴜʙᴍɪᴛᴛᴇᴅ !'
    async for x in bot.iter_participants(event.chat_id, filter=types.ChannelParticipantsAdmins):
        mentions += u'[\u2066]' + f'(tg://user?id={x.id})'
    await event.reply(mentions)

@bot.on(events.NewMessage(pattern=r'(checker|چکر) (\d+)', outgoing=True))
async def checker(event):
    i = event.pattern_match.group(2)
    req = await requests(f'https://MTproto.in/API/checker.php?phone={i}')
    await event.edit(f"𝄞 ᴘʜᴏɴᴇ ➣ {i}\n𝄞 sᴛᴀᴛᴜs ➣ {req['ok']}\n𝄞 ʀᴇsᴜʟᴛs ➣ {req['results']}")

@bot.on(events.NewMessage(pattern=r'(gamee|گیم|gamebot|game) (.*) (\d+)', outgoing=True))
async def gamee(event):
    url, score = event.pattern_match.group(2), event.pattern_match.group(3)
    api_url = 'gamebot' if 'tbot.xyz' in url else 'gamee'
    req = await requests(f'https://MTproto.in/API/{api_url}.php?score={score}&url={url}')
    await event.edit(f"𝄞 sᴄᴏʀᴇ ➣ {score}\n𝄞 sᴛᴀᴛᴜs ➣ {req['ok']}")

@bot.on(events.NewMessage(pattern=r'(qrcode|کیو آر کد) (.*)', outgoing=True))
async def qrcode(event):
    t = event.pattern_match.group(2).replace(' ', '+')
    await bot.send_file(event.chat_id, file=f'https://MTProto.in/API/qrcode.php?text={t}', caption='ʏᴏᴜʀ ǫʀ ᴄᴏᴅᴇ ɪs ʀᴇᴀᴅʏ !')

@bot.on(events.NewMessage(pattern=r'(captcha|کپچا) (.*)', outgoing=True))
async def captcha(event):
    t = event.pattern_match.group(2).replace(' ', '+')
    await bot.send_file(event.chat_id, file=f'https://MTproto.in/API/captcha.php?text={t}', caption='ʏᴏᴜʀ ᴄᴀᴘᴛᴄʜᴀ ᴄᴏᴅᴇ ɪs ʀᴇᴀᴅʏ !')

@bot.on(events.NewMessage(pattern=r'(whois|هویز) (.*)', outgoing=True))
async def whois(event):
    i = event.pattern_match.group(2)
    req = await requests(f'https://MTproto.in/API/whois.php?domain={i}')
    if req['ok']:
        r = req['results']
        txt = '\n'.join([f"𝄞 {k.replace('_', ' ').upper()} ➣ {v}" for k, v in r.items()])
        await event.edit(txt)
    else: await event.edit('⟩••• ᴛʜᴇ ᴅᴏᴍᴀɪɴ ɪs ɪɴᴠᴀʟɪᴅ !')

@bot.on(events.NewMessage(pattern=r'(whisper|نجوا) (.*)', outgoing=True))
async def whisper(event):
    i = event.pattern_match.group(2); await event.delete()
    if event.is_reply: g_id = (await event.get_reply_message()).sender.id
    elif event.is_private: g_id = event.chat_id
    else: return
    results = await bot.inline_query('whisperbot', f'{i} {g_id}')
    await results[0].click(event.chat_id)

@bot.on(events.NewMessage(pattern=r'(info|اطلاعات)', outgoing=True))
async def info(event):
    g_id = await get_user_id(event)
    if not g_id: return await event.edit('⟩••• ᴄᴀɴɴᴏᴛ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ !')
    full = await bot(GetFullUserRequest(g_id)); user = full.users[0]
    t = datetime.now(pytz.timezone('Asia/Tehran')).strftime('ᴛɪᴍᴇ : %H:%M:%S')
    txt = f'υѕer ιd : {g_id}\nғιrѕт ɴαмe : {user.first_name}\nlαѕт ɴαмe : {user.last_name}\nυѕerɴαмe : {user.username}\npнoɴe : {user.phone}\nвιo : {full.full_user.about}\n{t}'
    photos = await bot.get_profile_photos(g_id)
    if photos: await event.delete(); await bot.send_message(event.chat_id, txt, file=photos[0])
    else: await event.edit(txt)

@bot.on(events.NewMessage(pattern=r'(status|وضعیت)', outgoing=True))
async def status(event):
    c = {'p_c': 0, 'bots': 0, 'groups': 0, 'b_c': 0, 'a_g': 0, 'c_g': 0, 'a_b': 0, 'c_c': 0, 'u_m': 0, 'unread': 0}
    async for d in bot.iter_dialogs():
        e = d.entity
        if isinstance(e, types.Channel):
            if e.broadcast:
                c['b_c'] += 1; c['a_b'] += (e.creator or e.admin_rights); c['c_c'] += e.creator
            elif e.megagroup:
                c['groups'] += 1; c['a_g'] += (e.creator or e.admin_rights); c['c_g'] += e.creator
        elif isinstance(e, types.User):
            c['p_c'] += 1; c['bots'] += e.bot
        elif isinstance(e, types.Chat):
            c['groups'] += 1; c['a_g'] += (e.creator or e.admin_rights); c['c_g'] += e.creator
        c['u_m'] += d.unread_mentions_count; c['unread'] += d.unread_count
    txt = 'ѕтαтυѕ !'
    txt += f"\nᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛs : {c['p_c']}\nʙᴏᴛs : {c['bots']}\nɢʀᴏᴜᴘs : {c['groups']}\nʙʀᴏᴀᴅᴄᴀsᴛ ᴄʜᴀɴɴᴇʟs : {c['b_c']}\nᴀᴅᴍɪɴ ɪɴ ɢʀᴏᴜᴘs : {c['a_g']}\nᴄʀᴇᴀᴛᴏʀ ɪɴ ɢʀᴏᴜᴘs : {c['c_g']}\nᴀᴅᴍɪɴ ɪɴ ʙʀᴏᴀᴅᴄᴀsᴛ ᴄʜᴀɴɴᴇʟs : {c['a_b']}\nᴄʀᴇᴀᴛᴏʀ ɪɴ ᴄʜᴀɴɴᴇʟs : {c['c_c']}\nᴜɴʀᴇᴀᴅ ᴍᴇɴᴛɪᴏɴs : {c['u_m']}\nᴜɴʀᴇᴀᴅ : {c['unread']}\nʟᴀʀɢᴇsᴛ ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀ ᴄᴏᴜɴᴛ : 0\nʟᴀʀɢᴇsᴛ ɢʀᴏᴜᴘ ᴡɪᴛʜ ᴀᴅᴍɪɴ : 0"
    await event.edit(txt)

@bot.on(events.NewMessage(pattern=r'(sessions|نشست های فعال)', outgoing=True))
async def sessions(event):
    r = await bot(GetAuthorizationsRequest()); txt = 'sᴇssɪᴏɴs :\n\n'
    for i in r.authorizations:
        txt += f'ʜᴀsʜ : {i.hash}\nᴅᴇᴠɪᴄᴇ ᴍᴏᴅᴇʟ : {i.device_model}\nᴘʟᴀᴛғᴏʀᴍ : {i.platform}\nsʏsᴛᴇᴍ ᴠᴇʀsɪон : {i.system_version}\nᴀᴘɪ ɪᴅ : {i.api_id}\nᴀᴘᴘ ɴᴀᴍᴇ : {i.app_name}\nᴀᴘᴘ ᴠᴇʀsɪᴏɴ : {i.app_version}\nᴅᴀᴛᴇ ᴄʀᴇᴀᴛᴇᴅ : {i.date_created}\nᴅᴀᴛᴇ ᴀᴄᴛɪᴠᴇ : {i.date_active}\nɪᴘ : {i.ip}\nᴄᴏᴜɴᴛʀʏ : {i.country}\n' + '┄┅┈┉┅┉┈┅┄' * 3 + '\n'
    await event.edit(txt)

@bot.on(events.NewMessage(pattern=r'(translate|مترجم)', outgoing=True, func=lambda e: e.is_reply))
async def translate(event):
    m = event.raw_text.split(' '); lan = str(m[1]) if len(m) == 2 else 'fa'
    msg = (await event.get_reply_message()).raw_text
    try:
        t = Translator().translate(msg, lan)
        await event.edit(f'ᴛʀᴀɴsʟᴀᴛᴇᴅ ғʀᴏᴍ {t.src} ᴛᴏ {t.dest}\n\nᴛʀᴀɴsʟᴀᴛᴇᴅ ᴛᴇxᴛ : {t.text}')
        v = gTTS(text=msg, lang=t.src, slow=True); v.save('file.mp3')
        await bot.send_file(event.chat_id, 'file.mp3', voice_note=True, reply_to=event.message.id); os.remove('file.mp3')
    except Exception as e: await bot.send_message('me', f'ＥＲＲＯＲ :\n\n{e}')

@bot.on(events.NewMessage(pattern=r'(download|دانلود)', outgoing=True, func=lambda e: e.is_reply))
async def download(event):
    try:
        await event.delete(); d = await bot.download_media(await event.get_reply_message())
        await bot.send_file(LOG_CHANNEL_ID, file=d, caption=os.path.basename(d)); os.remove(d)
    except Exception as e: await bot.send_message('me', f'ＥＲＲＯＲ :\n\n{e}')

@bot.on(events.NewMessage(pattern=r'(findtext|پیدا کردن متن) (.*)', outgoing=True))
async def findText(event):
    i = event.pattern_match.group(2)
    try:
        await event.edit(f'⟩••• sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛʜᴇ ᴡᴏʀᴅ {i}')
        async for m in bot.iter_messages(event.chat_id, search=i): await bot.forward_messages('me', m.id, event.chat_id)
    except Exception as e: await bot.send_message('me', f'ＥＲＲＯＲ :\n\n{e}')

@bot.on(events.NewMessage(pattern=r'(sendmessage|ارسال پیام) (.*)', outgoing=True, func=lambda e: e.is_reply))
async def sendMessage(event):
    t = timedelta(minutes=int(event.pattern_match.group(2))); msg = (await event.get_reply_message()).raw_text
    try:
        await event.edit(f'⟩••• ᴍᴇssᴀɢᴇ sᴇɴᴅɪɴɢ ɪs sᴇᴛ ᴀғᴛᴇʀ {t}')
        await bot.send_message(event.chat_id, msg, schedule=t)
    except Exception as e: await bot.send_message('me', f'ＥＲＲＯＲ :\n\n{e}')

@bot.on(events.NewMessage(pattern=r'(myphone|شماره من)', outgoing=True))
async def myPhone(event):
    await event.delete(); me = await bot.get_me()
    await bot.send_file(event.chat_id, types.InputMediaContact(phone_number=me.phone, first_name=me.first_name, last_name=me.last_name, vcard=''))

@bot.on(events.NewMessage(pattern=r'(pin|پین)', outgoing=True, func=lambda e: e.is_reply))
async def pin(event):
    await event.delete(); await bot.pin_message(event.chat_id, await event.get_reply_message(), notify=True)

@bot.on(events.NewMessage(pattern=r'(unpin|آن پین)', outgoing=True))
async def unPin(event): await event.delete(); await bot.unpin_message(event.chat_id)

@bot.on(events.NewMessage(pattern=r'(ban|بن)', outgoing=True, func=lambda e: e.is_group))
async def ban(event):
    g_id = await get_user_id(event)
    if not g_id: return await event.edit('⟩••• ᴄᴀɴɴᴏᴛ ғɪɴᴅ ᴛʜɪs ᴜsᴇʀ !')
    await event.delete(); await bot.kick_participant(event.chat_id, g_id)

@bot.on(events.NewMessage(pattern=r'(voicecall|ویس کال) (.*)', outgoing=True, func=lambda e: e.is_group))
async def voiceCall(event):
    t = timedelta(minutes=int(event.pattern_match.group(2)))
    title = (await event.get_reply_message()).raw_text if event.is_reply else 'Voice Call'
    try:
        await event.edit(f'⟩••• ᴠᴏɪᴄᴇ ᴄᴀʟʟ ɪs sᴇᴛ ғᴏʀ {t}')
        await bot(CreateGroupCallRequest(event.chat_id, title=title, schedule_date=t))
    except Exception as e: await bot.send_message('me', f'ＥＲＲＯＲ :\n\n{e}')

@bot.on(events.NewMessage(pattern=r'(voicecallplay|ویس کال پلی)', outgoing=True, func=lambda e: e.is_reply))
async def voiceCallPlay(event):
    try:
        d = await bot.download_media(await event.get_reply_message())
        await event.edit(f'⟩••• ᴠᴏɪᴄᴇ ᴄᴀʟʟ ɪs ᴘʟᴀʏɪɴɢ')
        app = PyTgCalls(bot); await app.start(); await app.play(event.chat_id, MediaStream(d))
    except Exception as e: await bot.send_message('me', f'ＥＲＲＯＲ :\n\n{e}')

@bot.on(events.NewMessage(pattern=r'(spam|اسپم) (.*) (\d+)', outgoing=True))
async def spam(event):
    try:
        t, c = event.pattern_match.groups()[1:]
        await event.edit(f'⟩••• sᴘᴀᴍᴍɪɴɢ ᴛʜᴇ {t} ᴛᴇxᴛ {c} ᴛɪᴍᴇs')
        r = event.reply_to.reply_to_msg_id if event.is_reply else None
        for _ in range(int(c)): await bot.send_message(event.chat_id, t, reply_to=r)
    except Exception as e: await bot.send_message('me', f'ＥＲＲＯＲ :\n\n{e}')

@bot.on(events.NewMessage(pattern=r'(flood|فلود) (.*) (\d+)', outgoing=True))
async def flood(event):
    try:
        t, c = event.pattern_match.groups()[1:]
        await event.edit(f'⟩••• ғʟᴏᴏᴅɪɴɢ ᴛʜᴇ {t} ᴛᴇxᴛ {c} ᴛɪᴍᴇs')
        r = event.reply_to.reply_to_msg_id if event.is_reply else None
        await bot.send_message(event.chat_id, (t + '\n') * int(c), reply_to=r)
    except Exception as e: await bot.send_message('me', f'ＥＲＲＯＲ :\n\n{e}')

@bot.on(events.NewMessage(pattern=r'(googleplay|گوگل پلی) (.*)', outgoing=True))
async def googlePlay(event):
    i = event.pattern_match.group(2)
    try:
        await event.edit(f'⟩••• sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛʜᴇ ɢᴀᴍᴇ {i}')
        r = search(i, lang='en', n_hits=3)
        if r:
            for res in r:
                c = f"ᴛɪᴛʟᴇ ➣ {res['title']}\n\nsᴄᴏʀᴇ ➣ {res['score']}\n\nɢᴇɴʀᴇ ➣ {res['genre']}\n\nᴠɪᴅᴇᴏ ➣ {res['video']}\n\nᴅᴇᴠᴇʟᴏᴘᴇʀ ➣ {res['developer']}\n\nɪɴsᴛᴀʟʟs ➣ {res['installs']}\n\nᴘʀɪᴄᴇ ➣ {res['price']}\n\nᴄᴜʀʀᴇɴᴄʏ ➣ {res['currency']}\n\nᴅᴇsᴄʀɪᴘᴛɪᴏɴ ➣ {res['description']}"
                c = c[:1021] + '...' if len(c) > 1024 else c
                await bot.send_file(event.chat_id, res['screenshots'][0], caption=c)
        else: await event.edit(f'⟩••• ᴀɴ ᴀᴘᴘʟɪᴄᴀᴛɪᴏɴ ɴᴀᴍᴇᴅ {i} ᴡᴀs ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ɢᴏᴏɢʟᴇ ᴘʟᴀʏ')
    except Exception as e: await bot.send_message('me', f'ＥＲＲＯＲ :\n\n{e}')

@bot.on(events.NewMessage(pattern=r'(screenshot|اسکرین شات)', outgoing=True))
async def screenShot(event):
    m_id = (await event.get_reply_message()).id if event.is_reply else event.message.id
    await event.edit(f'⟩••• ᴛᴀᴋɪɴɢ ᴀ sᴄʀᴇᴇɴsʜᴏᴛ ᴏғ ᴛʜᴇ ᴄʜᴀᴛ')
    await bot(SendScreenshotNotificationRequest(event.chat_id, types.InputReplyToMessage(reply_to_msg_id=m_id)))

@bot.on(events.NewMessage(pattern=r'(restart|ریستارت)', outgoing=True))
async def restart(event):
    await event.edit(f'**Restarting...** 🚀')
    await bot.disconnect()
    os.execv(sys.executable, ['python3'] + sys.argv)

@bot.on(events.NewMessage(pattern=r'(hashtag|bold|italic|delete|code|underline|reverse|part|mention|spoiler) (on|off)', outgoing=True))
async def editMode(event):
    k, v = event.pattern_match.groups(); js = await get('data.json')
    js[k] = v; await put('data.json', js)
    await event.edit(f'⟩••• ᴛʜᴇ {font(k)} ᴍᴏᴅᴇ ɴᴏᴡ ɪs {v}')

@bot.on(events.NewMessage(pattern=r'(typing|game|voice|video|sticker) (on|off)', outgoing=True))
async def editAction(event):
    k, v = event.pattern_match.groups(); js = await get('data.json')
    js[k] = v; await put('data.json', js)
    await event.edit(f'⟩••• ᴛʜᴇ {font(k)} αcтιoɴ ɴᴏᴡ ɪs {v}')

bot.start(); clock.start(); bot.run_until_disconnected()
