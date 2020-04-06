# importing environment
from dotenv import load_dotenv
load_dotenv()

# importing libs
import discord
import time
import json
import os

with open("bin/points.json", "r") as f:
    data = json.load(f)

roles = {
    15: ["A NOVICE", 696797542981042228], 
    30: ["A BEGINNER", 696797669141643304],
    60: ["A SKILLED", 696797815019667556],
    120: ["AN INTERMEDIATE", 696798686533124252],
    240: ["A PROFICIENT", 696799276059197440],
    480: ["AN ADVANCED", 696799460071571466],
    960: ["AN EXPERT", 696799680562069614]
}

async def update_role(user, points, message):
    g_id = message.channel.guild.id
    guild = ctx.get_guild(g_id)
    member = guild.get_member(int(user)) # yields None 
    for role_q in list(roles.keys())[::-1]: 
        if points >= role_q:         
            role_id = roles[role_q][1]
            role = guild.get_role(role_id)
            if role not in member.roles:
                await member.add_roles(role)
                await message.channel.send(f"<:OCslice:696868792323539084> Congratulations! You are now **{roles[role_q][0]}** orange! <:OCslice:696868792323539084>")
            break
    

async def award_points(user, point_increment, message):
    user = str(user)
    if user not in data:
        data.update({user: point_increment})
    else:
        data[user] += point_increment
        await update_role(user, data[user], message)
    with open("bin/points.json", "w") as f:
        json.dump(data, f, indent=4)

point_incr = 1
user_cache = {}
class OrangeBot(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        user_id = message.author.id
        if user_id not in user_cache:
            user_cache.update({
                user_id: time.time()
            })
            await award_points(user_id, point_incr, message)
        else:
            if time.time() - user_cache[user_id] >= 60:
                user_cache[user_id] = time.time()
                await award_points(user_id, point_incr, message)


ctx = OrangeBot()
ctx.run(os.getenv("BOT_TOKEN"))