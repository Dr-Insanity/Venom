import discord_self_embed

embed = discord_self_embed.Embed("discord.py-self_embed", 
  description="A way for selfbots to send embeds again.", 
  colour="ff0000"
)
embed.set_author("Benny")

url = embed.generate_url(hide_url=True, shorten_url=False) # You can also convert the embed to a string.
print(url) # The url will be put in your ctx.send() content.

