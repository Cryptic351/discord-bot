import discord
from discord.ext import commands
import json
import os
from flask import Flask
from threading import Thread

# --- FIX FOR RENDER FREE (fixes your port error) ---
app = Flask('')
@app.route('/')
def home():
    return "LUA STUDIO BOT ONLINE - IM TOO GOOD"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# CONFIG
BOT_TOKEN = os.environ["TOKEN"]
PREFIX = "!"
SCRIPTS_FILE = "scripts.json"

# Default scripts
DEFAULT_SCRIPTS = {
    "duels": {
        "name": "LUA STUDIO Duels Fork",
        "loadstring": 'loadstring(game:HttpGet("https://pixel-perfect-render-80435.lovable.app/raw/t/10618fceb69b3b35ed39ad2fd2ca14e6"))()',
        "desc": "Yellow & Black | Pixel Logo | Fade-In"
    }
}

def load_scripts():
    if os.path.exists(SCRIPTS_FILE):
        with open(SCRIPTS_FILE, "r") as f:
            return json.load(f)
    else:
        with open(SCRIPTS_FILE, "w") as f:
            json.dump(DEFAULT_SCRIPTS, f, indent=4)
        return DEFAULT_SCRIPTS

def save_scripts(data):
    with open(SCRIPTS_FILE, "w") as f:
        json.dump(data, f, indent=4)

SCRIPTS = load_scripts()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"LUA STUDIO BOT ONLINE - {bot.user}")
    print(f"Loaded {len(SCRIPTS)} scripts")

@bot.command(name="find")
async def find_script(ctx, *, query: str = None):
    if not query:
        await ctx.send("**LUA STUDIO FINDER**\nUsage: `!find duels`\nDo `!list` to see all scripts")
        return
    query = query.lower()
    for key, script in SCRIPTS.items():
        if query in key.lower() or query in script["name"].lower():
            embed = discord.Embed(
                title=f"💛 {script['name']}",
                description=f"**{script['desc']}**\n\n```lua\n{script['loadstring']}\n```",
                color=0xFFD400
            )
            embed.set_footer(text="LUA STUDIO ON TOP | IM TOO GOOD")
            await ctx.send(embed=embed)
            return
    await ctx.send(f"No script found for `{query}`. Do `!list`")

@bot.command(name="list")
async def list_scripts(ctx):
    embed = discord.Embed(
        title="LUA STUDIO - ALL SCRIPTS",
        description="Use `!find <name>` - No more scrolling 20 channels",
        color=0xFFD400
    )
    for key, script in SCRIPTS.items():
        embed.add_field(name=script["name"], value=f"`!find {key}` - {script['desc']}", inline=False)
    embed.set_footer(text="Yellow & Black | Pixel Logo | Fade-In")
    await ctx.send(embed=embed)

@bot.command(name="add")
@commands.has_permissions(administrator=True)
async def add_script(ctx, key: str = None, *, rest: str = None):
    if not key or not rest:
        await ctx.send("**ADMIN ONLY - HOW TO USE:**\n```\n!add <key> <Name> | <loadstring> | <description>\n```")
        return
    try:
        parts = [p.strip() for p in rest.split("|")]
        if len(parts) < 2:
            await ctx.send("❌ You need at least Name | loadstring")
            return
        name = parts[0]
        loadstring_code = parts[1]
        desc = parts[2] if len(parts) > 2 else "No description"
        SCRIPTS[key.lower()] = {"name": name, "loadstring": loadstring_code, "desc": desc}
        save_scripts(SCRIPTS)
        embed = discord.Embed(title="✅ SCRIPT ADDED", description=f"**{name}** added as `{key.lower()}`", color=0x00FF00)
        embed.add_field(name="Loadstring", value=f"```lua\n{loadstring_code}\n```", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@add_script.error
async def add_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Nah bro, you need ADMIN to use `!add`. IM TOO GOOD.")

@bot.command(name="delete")
@commands.has_permissions(administrator=True)
async def delete_script(ctx, key: str = None):
    if not key:
        await ctx.send("Usage: `!delete <key>`")
        return
    key = key.lower()
    if key in SCRIPTS:
        del SCRIPTS[key]
        save_scripts(SCRIPTS)
        await ctx.send(f"✅ Deleted `{key}`")
    else:
        await ctx.send(f"❌ No script found for `{key}`")

# --- THIS IS THE FIX ---
keep_alive()
bot.run(BOT_TOKEN)
