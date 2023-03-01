"""
    name: casino_hack
    once: false
    origin: tgpy://module/casino_hack
    priority: 1677494496
"""
from telethon.tl.types import InputMediaDice as Dice

async def casino_hack(ultimate=False):
  map = [1, 2, 3, 0]
  while True:
    m = await ctx.msg.respond(file=Dice(“🎰”))
    value = m.media.value
    a, b, c = map[(value-1) & 3], map[((value-1) >> 2) & 3], map[((value-1) >> 4) & 3]
    if a == b == c and not ultimate or ultimate and a == b == c == 0:
      break
    await m.delete()
