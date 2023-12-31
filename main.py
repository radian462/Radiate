import function_file.AIchat as AIchat
import function_file.Translate as Translate
import function_file.WolfarmAlpha as WolfarmAlpha
import function_file.Exchanging as Exchanging
import function_file.shorturl as shorturl
import function_file.scp as scp
import datetime
import qrcode
import re
import random
import discord
import json
import os
from discord import app_commands
from keep_alive import keep_alive

client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print('起動しました')
    scp.make_database()
    await tree.sync()
    
#機能リスト
@tree.command(name='function_list', description='機能の一覧を表示します')
async def function_list(interaction: discord.Interaction):
  embed = discord.Embed(title="機能一覧",description="・AIチャット\n・DeepL翻訳\n・WolframAlpha計算知能\n・為替機能\n・短縮URL作成\n・QRコード作成\n・偽中国語作成\n・文章黒塗り")
  await interaction.response.send_message(embed=embed)

#helpコマンド
@tree.command(name='help', description='ヘルプを表示します')
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="ヘルプ")
    embed.add_field(name="・AIチャット",value="`@radianのbot [話す内容]`で会話できます\nELYZA-japanese-Llama-2-7bを搭載しています\n")
    embed.add_field(name="・DeepL翻訳",value="`/deepl [text] [lang] [lang2(省略可)]`で翻訳できます。\ntext:翻訳する文\nlang、lang2:翻訳する言語(選択肢の数の都合上分けました)\n※lang2の言語を使う場合はlangを「lang2の言語を使う」にしてください。\n対応言語:日本語, 英語(イギリス,アメリカ), 中国語(簡字体), 韓国語, ブルガリア語, チェコ語, デンマーク語, ドイツ語, ギリシャ語, エストニア語, スペイン語, フィンランド語, フランス語, ハンガリー語, インドネシア語, イタリア語, リトアニア語, ラトビア語, ノルウェー語(ブークモール), オランダ語, ポーランド語, ポルトガル語(ブラジル,ブラジル以外), ルーマニア語, ロシア語, スロバキア語, スロベニア語, スウェーデン語, トルコ語, ウクライナ語")
    embed.add_field(name="・WolfarmAlpha計算知能",value="WolfarmAlpha計算知能で計算ができます。方程式も可能です。\n`/wolfarmalpha [formula]`で計算できます。xの2乗はx^2と書けば出来ます。")
    embed.add_field(name="・為替機能",value="/exchange [currency] [currency2]で為替を確認できます。[currency]→[currency2]の為替を表示します。一部仮想通貨に対応しています")
    embed.add_field(name="・短縮URL作成",value="/shorturl [url]で作成できます")
    embed.add_field(name="・QRコード作成",value="/qrcode [text]で作成できます ")
    embed.add_field(name="・偽中国語作成",value="/fakechinese [text]で平仮名を削除します\nカタカナを消すかどうかの設定があります")
    embed.add_field(name="・文章黒塗り",value="/blackpaint [text]でランダムで文字を黒塗りします\n開示書類のような文を作れます")
    embed.add_field(name="・ランダムSCP",value="/scp でランダムなSCPの記事を表示します\nEN、J、EX、ARC、JP、JP-J、JP-EXに対応していますがSCP-8900-EX除く特殊な番号のSCPは出てきません")
    await interaction.response.send_message(embed=embed)

#AIチャット
@client.event
async def on_message(message):
  if message.author.bot:
      return

  if client.user.mentioned_in(message):
    message_text = re.sub('<@1173980854507274323>', '', message.content)
    if message_text: 
      async with message.channel.typing():
        
        if message_text.lower().startswith("#gemini") or message_text.lower().startswith("#bard"):
            message_text = re.sub('#gemini', '', message_text)
            message_text = re.sub('#bard', '', message_text)
            sent_message = await message.channel.send(AIchat.chatgemini(message_text))
            message_id = sent_message.id
            channel = message.channel 
            message_fetched = await channel.fetch_message(message_id)  
            await message_fetched.add_reaction("<:GeminiPro:1189384963045478450>")
        elif message_text.lower().startswith("#gpt"):
          message_text = re.sub('#gpt', '', message_text)
          sent_message = await message.channel.send(AIchat.chatgpt(message_text))
          message_id = sent_message.id
          channel = message.channel 
          message_fetched = await channel.fetch_message(message_id)  
          await message_fetched.add_reaction("<:GPT35turbo:1190420380347797564>")
        else:
            sent_message = await message.channel.send(AIchat.chatllama(message_text))
            message_id = sent_message.id
            channel = message.channel 
            message_fetched = await channel.fetch_message(message_id)  
            await message_fetched.add_reaction("<:ELYZAjapaneseLlama27b:1189216141873254420>")

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
@tree.command(name='wolfarmalpha', description='WolfarmAlpha計算知能で計算します') 
async def wolfarmalpha(interaction: discord.Interaction,formula:str):
  await interaction.response.send_message(WolfarmAlpha.calc(formula))

#為替コマンド
@tree.command(name='exchange', description='為替を表示します') 
@app_commands.describe(number="数",currency="通貨1",currency2="通貨2")
@discord.app_commands.choices(currency=[
  discord.app_commands.Choice(name="円",value="JPY"),
  discord.app_commands.Choice(name="ドル(アメリカ)",value="USD"),
  discord.app_commands.Choice(name="ユーロ",value="EUR"),
  discord.app_commands.Choice(name="ポンド",value="GBP"),
  discord.app_commands.Choice(name="人民元",value="CNY"), 
  discord.app_commands.Choice(name="ウォン",value="KRW"),
  discord.app_commands.Choice(name="ドル(香港)",value="HKD"),
  discord.app_commands.Choice(name="ドル(台湾)",value="TWD"),
  discord.app_commands.Choice(name="ルピー(インド)",value="INR"), 
  discord.app_commands.Choice(name="ルピア(インドネシア)",value="IDR"), 
  discord.app_commands.Choice(name="ドル(シンガポール)",value="SGD"),
  discord.app_commands.Choice(name="バーツ(タイ)",value="THB"),
  discord.app_commands.Choice(name="ドル(オーストラリア)",value="AUD"), 
  discord.app_commands.Choice(name="ドル(ニュージーランド)",value="NZD"), 
  discord.app_commands.Choice(name="フラン(スイス)",value="CHF"),
  discord.app_commands.Choice(name="リラ(トルコ)",value="TRY"),
  discord.app_commands.Choice(name="ペソ(メキシコ)",value="MXN"),
  discord.app_commands.Choice(name="ルーブル(ロシア)",value="RUB"),
  discord.app_commands.Choice(name="ドル(カナダ)",value="CAD"),
  discord.app_commands.Choice(name="レアル(ブラジル)",value="BRL"),
  discord.app_commands.Choice(name="ビットコイン",value="BTC"),
  discord.app_commands.Choice(name="イーサリアム",value="ETH"),
  discord.app_commands.Choice(name="リップル",value="XRP"),
  discord.app_commands.Choice(name="ライトコイン",value="LTC"),])

@discord.app_commands.choices(currency2=[
  discord.app_commands.Choice(name="円",value="JPY"),
  discord.app_commands.Choice(name="ドル(アメリカ)",value="USD"),
  discord.app_commands.Choice(name="ユーロ",value="EUR"),
  discord.app_commands.Choice(name="ポンド",value="GBP"),
  discord.app_commands.Choice(name="人民元",value="CNY"), 
  discord.app_commands.Choice(name="ウォン",value="KRW"),
  discord.app_commands.Choice(name="ドル(香港)",value="HKD"),
  discord.app_commands.Choice(name="ドル(台湾)",value="TWD"),
  discord.app_commands.Choice(name="ルピー(インド)",value="INR"), 
  discord.app_commands.Choice(name="ルピア(インドネシア)",value="IDR"), 
  discord.app_commands.Choice(name="ドル(シンガポール)",value="SGD"),
  discord.app_commands.Choice(name="バーツ(タイ)",value="THB"),
  discord.app_commands.Choice(name="ドル(オーストラリア)",value="AUD"), 
  discord.app_commands.Choice(name="ドル(ニュージーランド)",value="NZD"), 
  discord.app_commands.Choice(name="フラン(スイス)",value="CHF"),
  discord.app_commands.Choice(name="リラ(トルコ)",value="TRY"),
  discord.app_commands.Choice(name="ペソ(メキシコ)",value="MXN"),
  discord.app_commands.Choice(name="ルーブル(ロシア)",value="RUB"),
  discord.app_commands.Choice(name="ドル(カナダ)",value="CAD"),
  discord.app_commands.Choice(name="レアル(ブラジル)",value="BRL"),
  discord.app_commands.Choice(name="ビットコイン",value="BTC"),
  discord.app_commands.Choice(name="イーサリアム",value="ETH"),
  discord.app_commands.Choice(name="リップル",value="XRP"),
  discord.app_commands.Choice(name="ライトコイン",value="LTC"),])

async def exchange(interaction: discord.Interaction,number:str,currency:str,currency2:str):
  await interaction.response.defer()
  value = Exchanging.exchange(number,currency,currency2)
  embed = discord.Embed(title="為替")
  embed.add_field(name=f"{number}{currency}→{value}{currency2}",value=datetime.datetime.now())
  await interaction.followup.send(embed=embed)


#短縮URL作成コマンド
@tree.command(name='shorturl', description='短縮URLを作成します') 
async def shorturlbyshortio(interaction: discord.Interaction,url:str):
  await interaction.response.send_message(shorturl.makeshorturl(url))

#qrコード作成コマンド
@tree.command(name='qrcode', description='QRコードを作成します') 
async def qrcodemake(interaction: discord.Interaction,text:str):
  qrcode.make(text).save("qrcode.png")
  await interaction.response.send_message(file=discord.File("qrcode.png"))
  os.remove("qrcode.png")

#偽中国語コマンド
@tree.command(name='fakechinese', description='偽中国語を作成します') 
@app_commands.describe(text="原文",deletekatakana="カタカナを削除するか")                              
async def fakechinese(interaction: discord.Interaction,text:str,deletekatakana:bool=None):
  if deletekatakana == True or deletekatakana == None:
    text = re.sub('[ァ-ン]', '',text)
  await interaction.response.send_message(re.sub('[ぁ-ん]', '',text))

#黒塗りコマンド
@tree.command(name='blackpaint', description='ランダムで黒塗りします')
@app_commands.describe(text="原文")                      
async def blackpaint(interaction: discord.Interaction,text:str):
  painttimes = len(text) // 15
  firstnumber = 0
  if painttimes < 1:
      painttimes = 1

  while painttimes > 0:
      paintlong = random.randint(2, 7)
      paintplace = random.randint(firstnumber, len(text) - 7)
      text = (
          text[:paintplace]
          + "█" * paintlong
          + text[paintplace + paintlong:]
      )
      firstnumber += paintlong
      painttimes -= 1
    
  await interaction.response.send_message(text)

#2進数変換コマンド
@tree.command(name='binary', description='2進数に変換します')
@app_commands.describe(text="原文")                              
async def binary(interaction: discord.Interaction,text:str):
  byte_data = text.encode("utf-8")
  await interaction.response.send_message(' '.join(format(byte, '08b') for byte in byte_data))

#ランダムscp
@tree.command(name='scp', description='ランダムなSCPのリンクを生成します')
async def exchange(interaction: discord.Interaction):
  await interaction.response.send_message(scp.random_scp())

#文字化けコマンド
@tree.command(name='mojibake', description='文を文字化けさせます')
@app_commands.describe(text="原文")                              
async def mojibake(interaction: discord.Interaction,text:str):
  await interaction.response.send_message(text.encode("UTF-8").decode('shift-jis', errors='ignore'))

#アナグラムコマンド
@tree.command(name='anagram', description='アナグラムを作ります')
@app_commands.describe(text="原文")               
async def anagram(interaction: discord.Interaction,text:str):
  textlist = list(text)
  times = len(textlist)
  anagram = ""  

  for i in range(times):
    randomtext = random.choice(textlist)
    anagram = anagram + randomtext
    textlist.remove(randomtext)
  await interaction.response.send_message(anagram)

#文字コードコマンド
@tree.command(name='utf8', description='文を文字コードにします')
@app_commands.describe(text="原文")                              
async def utf8(interaction: discord.Interaction,text:str):
  await interaction.response.send_message(text.encode("UTF-8"))

keep_alive()
client.run(os.getenv("Discord_token"))
