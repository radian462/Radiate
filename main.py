import AIchat
import Translate
import WolfarmAlpha
from keep_alive import keep_alive
import discord
import os
from discord import app_commands

client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print('起動しました')
    await tree.sync()

#helpコマンド
@tree.command(name='help', description='ヘルプを表示します')
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="ヘルプ")
    embed.add_field(name="AIチャット",value="`@radianのbot [話す内容]`で会話できます\nELYZA-japanese-Llama-2-7bを搭載しています\n")
    embed.add_field(name="DeepL翻訳",value="`/deepl [text] [lang] [lang2(省略可)]`で翻訳できます。\ntext:翻訳する文\nlang、lang2:翻訳する言語(選択肢の数の都合上分けました)\n※lang2の言語を使う場合はlangを「lang2の言語を使う」にしてください。\n対応言語:日本語, 英語(イギリス,アメリカ), 中国語(簡字体), 韓国語, ブルガリア語, チェコ語, デンマーク語, ドイツ語, ギリシャ語, エストニア語, スペイン語, フィンランド語, フランス語, ハンガリー語, インドネシア語, イタリア語, リトアニア語, ラトビア語, ノルウェー語(ブークモール), オランダ語, ポーランド語, ポルトガル語(ブラジル,ブラジル以外), ルーマニア語, ロシア語, スロバキア語, スロベニア語, スウェーデン語, トルコ語, ウクライナ語")
    embed.add_field(name="WolfarmAlpha",value="WolfarmAlphaで計算ができます。\n`/wolfarmalpha [formula]`で計算できます。xの2乗はx^2と書けば出来ます。")
    await interaction.response.send_message(embed=embed)

#Llama2チャット
@client.event
async def on_message(message):
    if message.author.bot:
        return

    if client.user.mentioned_in(message):
      await message.channel.send(AIchat.chatfireworks(message.clean_content.replace('@radianのbot test', '')))

#DeepL翻訳コマンド
@tree.command(name='deepl', description='DeepLで翻訳します') 
@app_commands.describe(text="原文",lang="翻訳先の言語",lang2="翻訳先の言語")
@discord.app_commands.choices(lang=[
    discord.app_commands.Choice(name="lang2の言語を使う",value="lang2"),
    discord.app_commands.Choice(name="日本語",value="JA"),
    discord.app_commands.Choice(name="英語(イギリス)",value="EN-GB"),
    discord.app_commands.Choice(name="英語(アメリカ)",value="EN-US"),
    discord.app_commands.Choice(name="中国語(簡字体)",value="ZH"),
    discord.app_commands.Choice(name="韓国語",value="KO"), 
    discord.app_commands.Choice(name="ブルガリア語",value="BG"),
    discord.app_commands.Choice(name="チェコ語",value="CS"),
    discord.app_commands.Choice(name="デンマーク語",value="DA"),
    discord.app_commands.Choice(name="ドイツ語",value="DE"), 
    discord.app_commands.Choice(name="ギリシャ語",value="EL"), 
    discord.app_commands.Choice(name="エストニア語",value="ET"),
    discord.app_commands.Choice(name="スペイン語",value="ES"),
    discord.app_commands.Choice(name="フィンランド語",value="FI"), 
    discord.app_commands.Choice(name="フランス語",value="FR"), 
    discord.app_commands.Choice(name="ハンガリー語",value="HU"),
    discord.app_commands.Choice(name="インドネシア語",value="ID"),
    discord.app_commands.Choice(name="イタリア語",value="IT"),
    discord.app_commands.Choice(name="リトアニア語",value="LT"),
    discord.app_commands.Choice(name="ラトビア語",value="LV"),
    discord.app_commands.Choice(name="ノルウェー語(ブークモール)",value="NB"),
    discord.app_commands.Choice(name="オランダ語",value="NL"),
    discord.app_commands.Choice(name="ポーランド語",value="PL"),
    discord.app_commands.Choice(name="ポルトガル語(ブラジル)",value="PT-BR"),
    discord.app_commands.Choice(name="ポルトガル語(ブラジル除く全てのポルトガル語)",value="PT-PT"),])

@discord.app_commands.choices(lang2=[
    discord.app_commands.Choice(name="ルーマニア語",value="RO"),
    discord.app_commands.Choice(name="ロシア語",value="RU"),
    discord.app_commands.Choice(name="スロバキア語",value="SK"),
    discord.app_commands.Choice(name="スロベニア語",value="SL"),
    discord.app_commands.Choice(name="スウェーデン語",value="SV"),
    discord.app_commands.Choice(name="トルコ語",value="TR"),
    discord.app_commands.Choice(name="ウクライナ語",value="UK"),])


async def deepl(interaction: discord.Interaction,text:str,lang:str,lang2:str=None): 
  embed = discord.Embed(title="DeepL翻訳")
  embed.add_field(name="原文",value=f"{text}\n")
  
  if lang != "lang2":
    embed.add_field(name="翻訳結果",value=Translate.deepltranslate(text,lang))
  else:
    embed.add_field(name="翻訳結果",value=Translate.deepltranslate(text,lang2))
  await interaction.response.send_message(embed=embed)

#Wolfalphaコマンド
@tree.command(name='wolfarmalpha', description='WolfarmAlphaで計算します') 
async def wolfarmalpha(interaction: discord.Interaction,formula:str):
  await interaction.response.send_message(WolfarmAlpha.calc(formula))
  
  

TOKEN = os.getenv("Discord_token")
keep_alive()
client.run(TOKEN)
