import aiohttp, aiofiles, json, random, psutil, os
from flask import Flask, request
from config import BOT_TOKEN, ADMIN_USERS

app = Flask(__name__)

async def get(f):
    async with aiofiles.open(f, 'r') as r:
        return json.loads(await r.read())

async def put(f, d):
    async with aiofiles.open(f, 'w') as w:
        await w.write(json.dumps(d))

async def font(t):
    return t.lower().translate(t.maketrans("qwertyuiopasdfghjklzxcvbnm", "ǫᴡᴇʀᴛʏᴜɪᴏᴘᴀsᴅғɢʜᴊᴋʟᴢxᴄᴠʙɴᴍ"))

async def kill(path, filename):
    for p in psutil.process_iter():
        try:
            c = p.cmdline()
            pid = p.pid
            if os.path.basename(c[1]) == filename:
                return os.system(f"kill -9 {pid} && {path} && python3 {filename}")
        except: continue
    return os.system(f"{path} && python3 {filename}")

class U:
    def __init__(self, d):
        for k, v in d.items():
            setattr(self, k, [U(x) if isinstance(x, dict) else x for x in v] if isinstance(v, (list, tuple)) and v and isinstance(v[0], dict) else U(v) if isinstance(v, dict) else v)
    def __getattr__(self, n): return self
    def __str__(self): return 'None'

class B:
    def __init__(self, t): self.token = t
    async def _req(self, m, d=[]):
        async with aiohttp.ClientSession() as s:
            async with s.post(f'https://api.telegram.org/bot{self.token}/{m}', data=d) as r:
                return U(await r.json())
    def __getattr__(self, a):
        async def f(**kw): return await self._req(a, kw)
        return f

@app.route('/helper', methods=['POST', 'GET'])
async def helper():
    T = B(BOT_TOKEN); update = request.get_json(force=True)
    
    if 'message' in update:
        m = update['message']
        if m['text'].startswith('/start') and m['from']['id'] in ADMIN_USERS and m['chat']['type'] == 'private':
            await T.SendMessage(chat_id=m['from']['id'], text=f"Welcome, {m['from']['first_name']}", parse_mode='HTML')
            
    if 'inline_query' in update:
        i = update['inline_query']; q, i_id, f_id = i['query'], i['id'], i['from']['id']
        
        if f_id in ADMIN_USERS:
            if q.startswith('panel'):
                await T.AnswerInlineQuery(inline_query_id=i_id, cache_time=0, is_personal=True, results=json.dumps([{
                    'type': 'article', 'id': random.randint(111, 999), 'title': '❦ Management Panel ❦',
                    'thumb_url': 'https://raw.githubusercontent.com/username/repository/main/assets/panel.png', 
                    'input_message_content': {'message_text': '✰ THE PANEL HAS BEEN OPENED ✰', 'parse_mode': 'HTML'},
                    'reply_markup': {'inline_keyboard': [
                        [{'text': '✰ LOCK MODES ✰', 'callback_data': 'lockmode-null'}, {'text': '✰ LOCK ACTIONS ✰', 'callback_data': 'lockaction-null'}],
                        [{'text': '✰ INFO ✰', 'callback_data': 'info'}],
                        [{'text': '✰ CRUSH LIST ✰', 'callback_data': 'list-crush'}, {'text': '✰ ENEMY LIST ✰', 'callback_data': 'list-enemy'}],
                        [{'text': '✰ HELP ✰', 'callback_data': 'help'}, {'text': '✰ STATUS ✰', 'callback_data': 'stats'}],
                        [{'text': '✰ EXIT ✰', 'callback_data': 'exit'}, {'text': '✰ RESTART ✰', 'callback_data': 'restart'}]]}}]))

            elif q.startswith('xo'):
                await T.AnswerInlineQuery(inline_query_id=i_id, cache_time=0, is_personal=True, results=json.dumps([{
                    'type': 'article', 'id': random.randint(111, 999), 'title': '❦ Tic-Tac-Toe Game ❦',
                    'thumb_url': 'https://raw.githubusercontent.com/username/repository/main/assets/xo.png', 
                    'input_message_content': {'message_text': '✰ CLICK START TO BEGIN ✰', 'parse_mode': 'HTML'},
                    'reply_markup': {'inline_keyboard': [
                        [{'text': '✰ START ✰', 'callback_data': 'doz-0-0-0-0~0~0~0|0~0~0~0|0~0~0~0|0~0~0~0'}]]}}]))

    elif 'callback_query' in update:
        c = update['callback_query']; c_id, c_data, m_id, f_id = c['id'], c['data'], c['inline_message_id'], c['from']['id']
        
        if f_id in ADMIN_USERS:
            if c_data.startswith('fake'):
                await T.AnswerCallbackQuery(c_id, text='DISPLAY INFORMATION ONLY', show_alert=True)

            elif c_data.startswith('back'):
                await T.AnswerCallbackQuery(c_id, text='WAIT...')
                k = [[{'text': '✰ LOCK MODES ✰', 'callback_data': 'lockmode-null'}, {'text': '✰ LOCK ACTIONS ✰', 'callback_data': 'lockaction-null'}],
                     [{'text': '✰ INFO ✰', 'callback_data': 'info'}],
                     [{'text': '✰ CRUSH LIST ✰', 'callback_data': 'list-crush'}, {'text': '✰ ENEMY LIST ✰', 'callback_data': 'list-enemy'}],
                     [{'text': '✰ HELP ✰', 'callback_data': 'help'}, {'text': '✰ STATUS ✰', 'callback_data': 'stats'}],
                     [{'text': '✰ EXIT ✰', 'callback_data': 'exit'}, {'text': '✰ RESTART ✰', 'callback_data': 'restart'}]]
                await T.EditMessageText(text='➣ YOU ARE BACK TO THE MAIN MENU', inline_message_id=m_id, parse_mode='HTML', reply_markup=json.dumps({'inline_keyboard': k}))

            elif c_data.startswith('info'):
                await T.AnswerCallbackQuery(c_id, text='WAIT...')
                txt = (
                    "NICKNAME : YOUR_NICKNAME\n"
                    "USERNAME : @YOUR_USERNAME\n"
                    "PHONE : YOUR_PHONE_NUMBER\n"
                    "BIOGRAPHY : YOUR_BIO_TEXT\n"
                    "VERSION : 0.2"
                )
                await T.EditMessageText(text=txt, inline_message_id=m_id, parse_mode='HTML', 
                                         reply_markup=json.dumps({'inline_keyboard': [[{'text': '➣ BACK ➢', 'callback_data': 'back'}]]}))
            
            elif c_data.startswith('help'):
                await T.AnswerCallbackQuery(c_id, text='WAIT...')
                await T.EditMessageText(text='HELP TEXT IS NOT SET . . . !', inline_message_id=m_id, parse_mode='HTML',
                                         reply_markup=json.dumps({'inline_keyboard': [[{'text': '➣ BACK ➢', 'callback_data': 'back'}]]}))

            elif c_data.startswith('stats'):
                m_use = psutil.Process(os.getpid()).memory_info()[0] / 1073741824
                m_perc = psutil.virtual_memory()[2]
                cpu_perc = psutil.cpu_percent(3)
                await T.AnswerCallbackQuery(c_id, text=f'• MEMORY USED : {m_use:.2f} GB\n• MEMORY : {m_perc} %\n• CPU : {cpu_perc} %', show_alert=True)

            elif c_data.startswith('exit'):
                await T.AnswerCallbackQuery(c_id, text='WAIT...')
                await T.EditMessageText(text='✄ YOU HAVE SUCCESSFULLY EXITED THE PANEL', inline_message_id=m_id, parse_mode='HTML')

            elif c_data.startswith('restart'):
                await T.AnswerCallbackQuery(c_id, text='WAIT...')
                
                RESTART_CMD = "cd /path/to/self-bot/ && git pull" 
                RESTART_FILE = "self.py" 
                await kill(RESTART_CMD, RESTART_FILE)
                
                await T.EditMessageText(text='✄ THE RESTART WAS SUCCESSFUL', inline_message_id=m_id, parse_mode='HTML')

            elif c_data.startswith('lockmode-'):
                mode = c_data.split('-')[1]
                if mode != 'null':
                    js = await get("data.json"); js[mode] = 'off' if js[mode] == 'on' else 'on'; await put("data.json", js)
                await T.AnswerCallbackQuery(c_id, text='WAIT...')
                js = await get("data.json")
                modes = ['hashtag', 'bold', 'italic', 'delete', 'code', 'underline', 'reverse', 'part', 'mention', 'spoiler']
                k = [[{'text': '✅' if js[t] == 'on' else '❌', 'callback_data': 'lockmode-' + t}, {'text': f'✰ {await font(t)} ✰', 'callback_data': 'fake'}] for t in modes]
                k.append([{'text': '➣ BACK ➢', 'callback_data': 'back'}])
                await T.EditMessageText(text='✎﹏﹏﹏ OFF / ON MODES PANEL', inline_message_id=m_id, parse_mode='HTML', reply_markup=json.dumps({'inline_keyboard': k}))

            elif c_data.startswith('lockaction-'):
                mode = c_data.split('-')[1]
                if mode != 'null':
                    js = await get("data.json"); js[mode] = 'off' if js[mode] == 'on' else 'on'; await put("data.json", js)
                await T.AnswerCallbackQuery(c_id, text='WAIT...')
                js = await get("data.json")
                actions = ['typing', 'game', 'voice', 'video', 'sticker']
                k = [[{'text': '✅' if js[t] == 'on' else '❌', 'callback_data': 'lockaction-' + t}, {'text': f'✰ {await font(t)} ✰', 'callback_data': 'fake'}] for t in actions]
                k.append([{'text': '➣ BACK ➢', 'callback_data': 'back'}])
                await T.EditMessageText(text='✎﹏﹏﹏ OFF / ON ACTIONS PANEL', inline_message_id=m_id, parse_mode='HTML', reply_markup=json.dumps({'inline_keyboard': k}))

            elif c_data.startswith('list-'):
                list_type = c_data.split('-')[1]; await T.AnswerCallbackQuery(c_id, text='WAIT...')
                l = f"{await font(list_type)} LIST :\n"; js = await get("data.json")
                if js.get(list_type):
                    for i in js[list_type]: l += f"\n• <a href ='tg://user?id={i}'>{i}</a>"
                else: l += "\nTHE LIST IS EMPTY !"
                await T.EditMessageText(text=l, inline_message_id=m_id, parse_mode='HTML',
                                         reply_markup=json.dumps({'inline_keyboard': [[{'text': '➣ BACK ➢', 'callback_data': 'back'}]]}))

        if c_data.startswith('doz-'):
            exp = c_data.split('-'); r, col, turn_id, board_str = int(exp[1]), int(exp[2]), int(exp[3]), exp[4]
            board = [x.split('~') for x in board_str.split('|')]
            
            if f_id == turn_id:
                await T.AnswerCallbackQuery(c_id, text='IT IS NOT YOUR TURN . . . !', show_alert=True)
                return update
                
            if board[r][col] == '0':
                x_count = board_str.count('X')
                o_count = board_str.count('O')
                mark = 'X' if x_count == o_count else 'O'
                board[r][col] = mark
            else:
                await T.AnswerCallbackQuery(c_id, text='YOU CANNOT SELECT THIS BUTTON . . . !', show_alert=True)
                return update
                
            await T.AnswerCallbackQuery(c_id, text='WAIT...')
            
            new_board_str = '|'.join(['~'.join(x) for x in board])
            
            next_turn_id = f_id
            
            k = [[{'text': board[row][column] if board[row][column] != '0' else ' ', 'callback_data': f'doz-{row}-{column}-{next_turn_id}-{new_board_str}'} for column in range(4)] for row in range(4)]
            await T.EditMessageText(text='▌│█║▌║▌║ TIC-TAC-TOE / XO ║▌║▌║█│▌', inline_message_id=m_id, parse_mode='HTML', reply_markup=json.dumps({'inline_keyboard': k}))
            
    return update

if __name__ == '__main__':
    app.run(port=80)
