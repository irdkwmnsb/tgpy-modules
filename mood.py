"""
    name: mood
    once: false
    origin: tgpy://module/mood
    priority: 1677334033.088082
    save_locals: true
"""
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from datetime import datetime
from operator import itemgetter
import random
from telethon.tl.functions.messages import SendReactionRequest
from telethon import events, types

tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer = tokenizer)

emot = []
emot.append(types.ReactionEmoji( emoticon='❤️'))
emot.append(types.ReactionEmoji( emoticon='😘'))
emot.append(types.ReactionEmoji( emoticon='😍'))
emot.append(types.ReactionEmoji( emoticon='🥰'))
emot.append(types.ReactionEmoji( emoticon='🤩'))
emot.append(types.ReactionEmoji( emoticon='❤️‍🔥'))
emot.append(types.ReactionEmoji( emoticon='💘'))
emot.append(types.ReactionEmoji( emoticon='🤗'))

emot2 = []
emot2.append(types.ReactionEmoji( emoticon='😱'))
emot2.append(types.ReactionEmoji( emoticon='😢'))
emot2.append(types.ReactionEmoji( emoticon='🤔'))
emot2.append(types.ReactionEmoji( emoticon='🤯'))


@client.on(events.NewMessage(chats=[1470771934, 1631278906, 1214263861]))
async def handler(msg):
  try:
    txt = []
    txt.append(msg.text)
    r = (model.predict(txt, k = 2))[0]
    if 'positive' in r:
      if r['positive'] >= 0.9:
        rea = random.choice(emot)
        res = await client(SendReactionRequest(msg.peer_id, msg.id, big = True, reaction=[rea]))
    if 'negative' in r:
      if r['negative'] >= 0.9:
        rea2 = random.choice(emot2)
        res2 = await client(SendReactionRequest(msg.peer_id, msg.id, big = True, reaction=[rea2]))
  except:
    return
  

async def topmood():
  ct = datetime.now().astimezone()
  texts = []
  ids = []
  async for mess in client.iter_messages(ctx.msg.chat_id):
    if (ct - mess.date).days > 0:
      break
    try:
      if not isinstance(mess.text, str):
        continue
      if len(mess.text) < 10:
        continue
    except:
      continue
    texts.append(mess.text)
    ids.append(mess.id)

  results = model.predict(texts, k = 2)
  dict_pos = {}
  dict_neg = {}
  for id, res in zip(ids, results):
    if 'positive' in res:
      dict_pos[id] = res['positive']
    if 'negative' in res:
      dict_neg[id] = res['negative']
  txt = 'TOP positive messages of the day:'
  cnt = 0
  for id, val in reversed(sorted(dict_pos.items(), key = itemgetter(1))):
    txt = txt + f'\nlink: t.me/c/{ctx.msg.chat.id}/{id}\nval: {val}'
    cnt = cnt + 1
    if cnt >= 5:
      break
  await ctx.msg.reply(txt)
  txt = 'TOP negative messages of the day:'
  cnt = 0
  for id, val in reversed(sorted(dict_neg.items(), key = itemgetter(1))):
    txt = txt + f'\nlink: t.me/c/{ctx.msg.chat.id}/{id}\nval: {val}'
    cnt = cnt + 1
    if cnt >= 5:
      break
  await ctx.msg.reply(txt)
  return 'Done'
