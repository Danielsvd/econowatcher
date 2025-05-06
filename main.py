import discord
from discord.ext import tasks, commands
import feedparser
import asyncio
import datetime
import json
import os
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")  # ← scrie manual, fără copy-paste
CHANNEL_ID = 1367395360959500288    # ← înlocuiește cu ID-ul canalului #stiri-bursiere

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# Feeduri RSS
rss_feeds = [
    "https://www.zf.ro/rss",
    "https://www.profit.ro/rss/economie",
    "https://www.economica.net/rss",
    "https://www.marketwatch.com/rss/topstories",
    "https://www.bursa.ro/_rss/?t=pcaps",
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC,^IXIC,CL=F,GC=F&region=US&lang=en-US"
]
cuvinte_alerta = ["recesiune", "criză", "faliment", "stagflație", "china", "război comercial", "inflație", "default", "blocaj bugetar", "SUA", "FED", "majorare de dobandă", "scăderea dobânzii de referință", "ședința FED", "date despre piața muncii din SUA", "raportul NFP", "date despre inflație din SUA", "date despre PIB din SUA", "date despre PIB din UE", "date despre inflație din UE", "date despre PIB din China", "date despre inflație din China", "corecție fiscală", "corecție bugetară", "corecție economică", "corecție abruptă a bursei", "scădere accentuată a pieței de capital", "rata șomajului in SUA", "rata șomajului in UE", "rata șomajului in China", "rata șomajului in România", "prețul petrolului", "prețul aurului", "prețul Bitcoinului"
]


@bot.event
async def on_ready():
    print(f"{bot.user} este online.")

    try:
        guild = discord.Object(id=1367394255366131742)  # ID-ul serverului tău
        bot.tree.copy_global_to(guild=guild)  # Copiază comenzile globale în server
        await bot.tree.sync(guild=guild)  # Sincronizează doar pe serverul tău
        print("✅ Comenzile slash au fost sincronizate LOCAL pe server.")
    except Exception as e:
        print(f"❌ Eroare la sincronizare comenzi: {e}")

    await asyncio.sleep(1)
    fetch_news.start()



@bot.tree.command(name="analiza", description="Trimite ultimele 3 știri bursiere relevante.")
async def analiza_command(interaction: discord.Interaction):
    await interaction.response.defer()

    mesaje = []
    trimise = 0

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title
            summary = entry.summary if "summary" in entry else ""
            link = entry.link

            mesaj = f"**{title}**\n\n{summary[:300]}...\n\n" \
                    f"**{interpretare(title + summary)}**\n\n[Vezi articolul complet]({link})"

            mesaje.append(mesaj)
            trimise += 1

            if trimise == 3:
                break
        if trimise == 3:
            break

    if mesaje:
        for m in mesaje:
            await interaction.followup.send(m)
    else:
        await interaction.followup.send("Nu am găsit știri bursiere recente.")

@bot.tree.command(name="bvb", description="Trimite ultimele 3 știri legate de România sau BVB.")
async def bvb_command(interaction: discord.Interaction):
    await interaction.response.defer()

    mesaje = []
    trimise = 0
    cuvinte_cheie = ["bvb românia", "românia", "romania", "bursei de valori bucurești", "anaf", "finanțe", "ministerul finanțelor"]

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title.lower()
            summary = entry.summary.lower() if "summary" in entry else ""
            content = title + summary

            if not any(cuv in content for cuv in cuvinte_cheie):
                continue

            mesaj = f"**{entry.title}**\n\n{entry.summary[:300]}...\n\n" \
                    f"**{interpretare(entry.title + entry.summary)}**\n\n[Vezi articolul complet]({entry.link})"
            mesaje.append(mesaj)
            trimise += 1

            if trimise == 3:
                break
        if trimise == 3:
            break

    if mesaje:
        for m in mesaje:
            await interaction.followup.send(m)
    else:
        await interaction.followup.send("Nu am găsit știri recente despre BVB sau România.")

@bot.tree.command(name="aur", description="Trimite ultimele știri despre aur și piețele sigure.")
async def aur_command(interaction: discord.Interaction):
    await interaction.response.defer()

    mesaje = []
    trimise = 0
    cuvinte_cheie = ["aur", "gold", "metal prețios", "metale prețioase", "refugiu", "safe haven"]

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title.lower()
            summary = entry.summary.lower() if "summary" in entry else ""
            content = title + summary

            if not any(cuv in content for cuv in cuvinte_cheie):
                continue

            mesaj = f"**{entry.title}**\n\n{entry.summary[:300]}...\n\n" \
                    f"**{interpretare(entry.title + entry.summary)}**\n\n[Vezi articolul complet]({entry.link})"
            mesaje.append(mesaj)
            trimise += 1

            if trimise == 3:
                break
            if trimise == 3:
                break

    if mesaje:
        for m in mesaje:
                await interaction.followup.send(m)
    else:
        await interaction.followup.send("Nu am găsit știri recente despre aur.")

@bot.tree.command(name="ping", description="Test de funcționare a comenzilor slash.")
async def ping_command(interaction: discord.Interaction):
    await interaction.response.send_message("✅ Botul funcționează și a răspuns la comanda /ping.")

@bot.tree.command(name="petrol", description="Trimite ultimele știri despre petrol și energie.")
async def petrol_command(interaction: discord.Interaction):
    await interaction.response.defer()

    mesaje = []
    trimise = 0
    cuvinte_cheie = ["petrol", "baril", "brent", "energie", "gaz", "opec"]

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title.lower()
            summary = entry.summary.lower() if "summary" in entry else ""
            content = title + summary

            if not any(cuv in content for cuv in cuvinte_cheie):
                continue

            mesaj = f"**{entry.title}**\n\n{entry.summary[:300]}...\n\n" \
                    f"**{interpretare(entry.title + entry.summary)}**\n\n[Vezi articolul complet]({entry.link})"
            mesaje.append(mesaj)
            trimise += 1

            if trimise == 3:
                break
        if trimise == 3:
            break

    if mesaje:
        for m in mesaje:
            await interaction.followup.send(m)
    else:
        await interaction.followup.send("Nu am găsit știri recente despre petrol sau energie.")

@bot.tree.command(name="somaj", description="Trimite ultimele știri despre șomaj și piața muncii.")
async def somaj_command(interaction: discord.Interaction):
    await interaction.response.defer()

    mesaje = []
    trimise = 0
    cuvinte_cheie = ["șomaj", "locuri de muncă", "rata șomajului", "ocuparea forței de muncă", "someri"]

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title.lower()
            summary = entry.summary.lower() if "summary" in entry else ""
            content = title + summary

            if not any(cuv in content for cuv in cuvinte_cheie):
                continue

            mesaj = f"**{entry.title}**\n\n{entry.summary[:300]}...\n\n" \
                    f"**{interpretare(entry.title + entry.summary)}**\n\n[Vezi articolul complet]({entry.link})"
            mesaje.append(mesaj)
            trimise += 1

            if trimise == 3:
                break
        if trimise == 3:
            break

    if mesaje:
        for m in mesaje:
            await interaction.followup.send(m)
    else:
        await interaction.followup.send("Nu am găsit știri recente despre șomaj sau piața muncii.")

@bot.tree.command(name="recesiune", description="Trimite ultimele știri despre recesiune, criză și încetinire economică.")
async def recesiune_command(interaction: discord.Interaction):
    await interaction.response.defer()

    mesaje = []
    trimise = 0
    cuvinte_cheie = ["recesiune", "contracție", "criză economică", "încetinire", "scădere economică", "contractie"]

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title.lower()
            summary = entry.summary.lower() if "summary" in entry else ""
            content = title + summary

            if not any(cuv in content for cuv in cuvinte_cheie):
                continue

            mesaj = f"**{entry.title}**\n\n{entry.summary[:300]}...\n\n" \
                    f"**{interpretare(entry.title + entry.summary)}**\n\n[Vezi articolul complet]({entry.link})"
            mesaje.append(mesaj)
            trimise += 1

            if trimise == 3:
                break
        if trimise == 3:
            break

    if mesaje:
        for m in mesaje:
            await interaction.followup.send(m)
    else:
        await interaction.followup.send("Nu am găsit știri recente despre recesiune.")

@bot.tree.command(name="taxe", description="Trimite ultimele știri despre taxe, TVA și politici fiscale.")
async def taxe_command(interaction: discord.Interaction):
    await interaction.response.defer()

    mesaje = []
    trimise = 0
    cuvinte_cheie = ["taxe", "tva", "impozit", "fiscal", "cota de impozitare", "cod fiscal", "reformă fiscală"]

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title.lower()
            summary = entry.summary.lower() if "summary" in entry else ""
            content = title + summary

            if not any(cuv in content for cuv in cuvinte_cheie):
                continue

            mesaj = f"**{entry.title}**\n\n{entry.summary[:300]}...\n\n" \
                    f"**{interpretare(entry.title + entry.summary)}**\n\n[Vezi articolul complet]({entry.link})"
            mesaje.append(mesaj)
            trimise += 1

            if trimise == 3:
                break
        if trimise == 3:
            break

    if mesaje:
        for m in mesaje:
            await interaction.followup.send(m)
    else:
        await interaction.followup.send("Nu am găsit știri recente despre taxe sau politici fiscale.")

@bot.tree.command(name="nasdaq", description="Trimite ultimele știri despre Nasdaq și companiile tech din SUA.")
async def nasdaq_command(interaction: discord.Interaction):
    await interaction.response.defer()

    mesaje = []
    trimise = 0
    cuvinte_cheie = ["nasdaq", "s&p 500", "dow jones", "apple", "microsoft", "tesla", "meta", "tech", "sua", "fed"]

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title.lower()
            summary = entry.summary.lower() if "summary" in entry else ""
            content = title + summary

            if not any(cuv in content for cuv in cuvinte_cheie):
                continue

            mesaj = f"**{entry.title}**\n\n{entry.summary[:300]}...\n\n" \
                    f"**{interpretare(entry.title + entry.summary)}**\n\n[Vezi articolul complet]({entry.link})"
            mesaje.append(mesaj)
            trimise += 1

            if trimise == 3:
                break
        if trimise == 3:
            break

    if mesaje:
        for m in mesaje:
            await interaction.followup.send(m)
    else:
        await interaction.followup.send("Nu am găsit știri recente despre Nasdaq sau piața tech.")

@bot.tree.command(name="europa", description="Știri despre BCE, euro, cheltuieli militare și comerț în Europa.")
async def europa_command(interaction: discord.Interaction):
    await interaction.response.defer()

    mesaje = []
    trimise = 0
    cuvinte_cheie = [
        "bce", "zona euro", "euro", "inflație în europa", "dobândă bce", "banca centrală europeană",
        "cheltuieli militare", "ucraina", "nato", "defense", "militar",
        "balanță comercială", "exporturi", "importuri", "comerț extern", "comert exterior"
    ]

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title.lower()
            summary = entry.summary.lower() if "summary" in entry else ""
            content = title + summary

            if not any(cuv in content for cuv in cuvinte_cheie):
                continue

            mesaj = f"**{entry.title}**\n\n{entry.summary[:300]}...\n\n" \
                    f"**{interpretare(entry.title + entry.summary)}**\n\n[Vezi articolul complet]({entry.link})"
            mesaje.append(mesaj)
            trimise += 1

            if trimise == 3:
                break
        if trimise == 3:
            break

    if mesaje:
        for m in mesaje:
            await interaction.followup.send(m)
    else:
        await interaction.followup.send("Nu am găsit știri relevante din Europa.")

@bot.tree.command(name="profituri", description="Trimite ultimele știri despre rezultate financiare și profituri.")
async def profituri_command(interaction: discord.Interaction):
    await interaction.response.defer()

    mesaje = []
    trimise = 0
    cuvinte_cheie = [
        "rezultate financiare", "profit net", "cifră de afaceri", "venituri trimestriale", "venituri semestriale", "venituri anuale",
        "raport financiar", "q1", "q2", "q3", "q4", "t1", "t2", "t3", "t4", "S1", "S2",
        "earnings", "report", "financials"
    ]

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title.lower()
            summary = entry.summary.lower() if "summary" in entry else ""
            content = title + summary

            if not any(cuv in content for cuv in cuvinte_cheie):
                continue

            mesaj = f"**{entry.title}**\n\n{entry.summary[:300]}...\n\n" \
                    f"**{interpretare(entry.title + entry.summary)}**\n\n[Vezi articolul complet]({entry.link})"
            mesaje.append(mesaj)
            trimise += 1

            if trimise == 3:
                break
        if trimise == 3:
            break

    if mesaje:
        for m in mesaje:
            await interaction.followup.send(m)
    else:
        await interaction.followup.send("Nu am găsit știri recente despre profituri sau rezultate financiare.")

@bot.tree.command(name="tarife", description="Trimite știri despre tarife comerciale și politici vamale.")
async def tarife_command(interaction: discord.Interaction):
    await interaction.response.defer()

    mesaje = []
    trimise = 0
    cuvinte_cheie = [
        "tarife", "taxe vamale", "război comercial", "trump", "china", "importuri", "exporturi",
        "politici comerciale", "protecționism", "sancțiuni comerciale", "usa-china"
    ]

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title.lower()
            summary = entry.summary.lower() if "summary" in entry else ""
            content = title + summary

            if not any(cuv in content for cuv in cuvinte_cheie):
                continue

            mesaj = f"**{entry.title}**\n\n{entry.summary[:300]}...\n\n" \
                    f"**{interpretare(entry.title + entry.summary)}**\n\n[Vezi articolul complet]({entry.link})"
            mesaje.append(mesaj)
            trimise += 1

            if trimise == 3:
                break
        if trimise == 3:
            break

    if mesaje:
        for m in mesaje:
            await interaction.followup.send(m)
    else:
        await interaction.followup.send("Nu am găsit știri recente despre tarife comerciale.")

@bot.tree.command(name="salarii", description="Trimite știri despre salarii, venituri și puterea de cumpărare.")
async def salarii_command(interaction: discord.Interaction):
    await interaction.response.defer()

    mesaje = []
    trimise = 0
    cuvinte_cheie = [
        "salariu", "salarii", "venituri", "creștere salarială", "putere de cumpărare",
        "salariu minim", "salariu mediu", "costul vieții", "indexare"
    ]

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title.lower()
            summary = entry.summary.lower() if "summary" in entry else ""
            content = title + summary

            if not any(cuv in content for cuv in cuvinte_cheie):
                continue

            mesaj = f"**{entry.title}**\n\n{entry.summary[:300]}...\n\n" \
                    f"**{interpretare(entry.title + entry.summary)}**\n\n[Vezi articolul complet]({entry.link})"
            mesaje.append(mesaj)
            trimise += 1

            if trimise == 3:
                break
        if trimise == 3:
            break

    if mesaje:
        for m in mesaje:
            await interaction.followup.send(m)
    else:
        await interaction.followup.send("Nu am găsit știri recente despre salarii sau venituri.")

@bot.tree.command(name="sp500", description="Trimite știri despre indicele S&P 500 și companiile din el.")
async def sp500_command(interaction: discord.Interaction):
    await interaction.response.defer()

    mesaje = []
    trimise = 0
    cuvinte_cheie = [
        "s&p 500", "sp500", "indicele s&p500", "apple", "microsoft", "amazon", "google",
        "meta", "nvidia", "tesla", "bursa sua", "wall street", "tsm", "oxy", "bac", "cop", "xom", "cvx", "dawn jones"
    ]

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title.lower()
            summary = entry.summary.lower() if "summary" in entry else ""
            content = title + summary

            if not any(cuv in content for cuv in cuvinte_cheie):
                continue

            mesaj = f"**{entry.title}**\n\n{entry.summary[:300]}...\n\n" \
                    f"**{interpretare(entry.title + entry.summary)}**\n\n[Vezi articolul complet]({entry.link})"
            mesaje.append(mesaj)
            trimise += 1

            if trimise == 3:
                break
        if trimise == 3:
            break

    if mesaje:
        for m in mesaje:
            await interaction.followup.send(m)
    else:
        await interaction.followup.send("Nu am găsit știri recente despre S&P 500.")

@bot.tree.command(name="piata_imobiliara", description="Trimite știri despre imobiliare, locuințe și prețurile din piață.")
async def piata_imobiliara_command(interaction: discord.Interaction):
    await interaction.response.defer()

    mesaje = []
    trimise = 0
    cuvinte_cheie = [
        "imobiliare", "piața imobiliară", "locuințe", "prețuri la apartamente", "chirie",
        "ansamblu rezidențial", "cerere imobiliară", "tranzacții imobiliare", "sector rezidențial",
        "construcții", "dezvoltatori"
    ]

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title.lower()
            summary = entry.summary.lower() if "summary" in entry else ""
            content = title + summary

            if not any(cuv in content for cuv in cuvinte_cheie):
                continue

            mesaj = f"**{entry.title}**\n\n{entry.summary[:300]}...\n\n" \
                    f"**{interpretare(entry.title + entry.summary)}**\n\n[Vezi articolul complet]({entry.link})"
            mesaje.append(mesaj)
            trimise += 1

            if trimise == 3:
                break
        if trimise == 3:
            break

    if mesaje:
        for m in mesaje:
            await interaction.followup.send(m)
    else:
        await interaction.followup.send("Nu am găsit știri recente despre piața imobiliară.")

@bot.tree.command(name="crypto", description="Trimite știri despre criptomonede, Bitcoin, Ethereum și piața cripto.")
async def cripto_command(interaction: discord.Interaction):
    await interaction.response.defer()

    mesaje = []
    trimise = 0
    cuvinte_cheie = [
        "bitcoin", "ethereum", "crypto", "criptomonede", "btc", "eth",
        "etf bitcoin", "etf crypto", "binance", "coinbase", "blockchain",
        "piața cripto", "reglementări cripto", "criptoactive", "crypto market"
    ]

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title.lower()
            summary = entry.summary.lower() if "summary" in entry else ""
            content = title + summary

            if not any(cuv in content for cuv in cuvinte_cheie):
                continue

            mesaj = f"**{entry.title}**\n\n{entry.summary[:300]}...\n\n" \
                    f"**{interpretare(entry.title + entry.summary)}**\n\n[Vezi articolul complet]({entry.link})"
            mesaje.append(mesaj)
            trimise += 1

            if trimise == 3:
                break
        if trimise == 3:
            break

    if mesaje:
        for m in mesaje:
            await interaction.followup.send(m)
    else:
        await interaction.followup.send("Nu am găsit știri recente despre piața cripto.")

@bot.tree.command(name="banci", description="Trimite știri despre bănci, sistemul bancar și reglementări financiare.")
async def banci_command(interaction: discord.Interaction):
    await interaction.response.defer()

    mesaje = []
    trimise = 0
    cuvinte_cheie = [
        "banci", "banca", "bancă", "bănci", "banca centrala", "reglementari bancare",
        "dobanzi bancare", "criza bancara", "faliment bancar", "credit bancar",
        "sistemul bancar", "provizioane", "lichiditate", "active bancare", "finanțare"
    ]

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title.lower()
            summary = entry.summary.lower() if "summary" in entry else ""
            content = title + summary

            if not any(cuv in content for cuv in cuvinte_cheie):
                continue

            mesaj = f"**{entry.title}**\n\n{entry.summary[:300]}...\n\n" \
                    f"**{interpretare(entry.title + entry.summary)}**\n\n[Vezi articolul complet]({entry.link})"
            mesaje.append(mesaj)
            trimise += 1

            if trimise == 3:
                break
        if trimise == 3:
            break

    if mesaje:
        for m in mesaje:
            await interaction.followup.send(m)
    else:
        await interaction.followup.send("Nu am găsit știri recente despre bănci.")


@bot.tree.command(name="inflatie", description="Trimite ultimele știri despre inflație, dobânzi și bănci centrale.")
async def inflatie_command(interaction: discord.Interaction):
    await interaction.response.defer()

    mesaje = []
    trimise = 0
    cuvinte_cheie = ["inflație", "inflatie", "dobândă", "dobanda", "bce", "fed", "rata dobânzilor", "dobanzi bnr"]

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title.lower()
            summary = entry.summary.lower() if "summary" in entry else ""
            content = title + summary

            if not any(cuv in content for cuv in cuvinte_cheie):
                continue

            mesaj = f"**{entry.title}**\n\n{entry.summary[:300]}...\n\n" \
                    f"**{interpretare(entry.title + entry.summary)}**\n\n[Vezi articolul complet]({entry.link})"
            mesaje.append(mesaj)
            trimise += 1

            if trimise == 3:
                break
        if trimise == 3:
            break

    if mesaje:
        for m in mesaje:
            await interaction.followup.send(m)
    else:
        await interaction.followup.send("Nu am găsit știri recente despre inflație sau dobânzi.")        

# Funcție de interpretare automată extinsă
def interpretare(text):
    text = text.lower()

    if "inflație" in text or "inflatie" in text:
        return "Impact: inflația influențează politica monetară – reacție variabilă pe bursă. [📈 Grafic inflație SUA](https://www.tradingeconomics.com/united-states/inflation-cpi)"
    if "petrol" in text or "brent" in text or "baril" in text:
        return "Impact: prețul petrolului afectează inflația și companiile din energie. [📈 Grafic Brent](https://www.tradingview.com/symbols/TVC-UKOIL/)"
    if "aur" in text:
        return "Impact: aurul semnalează adesea aversiune la risc – investitorii caută siguranță. [📈 Grafic XAUUSD](https://www.tradingview.com/symbols/XAUUSD/)"
    if "bitcoin" in text or "crypto" in text or "btc" in text or "eth" in text or "ethereum" in text:
        return "Impact: volatilitate crescută – piața cripto influențează sectorul tech. [📈 Grafic BTCUSD](https://www.tradingview.com/symbols/BTCUSD/)"
    if "nasdaq" in text:
        return "Impact: indicii tech reflectă sentimentul investitorilor. [📈 Grafic Nasdaq](https://www.tradingview.com/symbols/NASDAQ-IXIC/)"
    if "s&p 500" in text or "sp500" in text:
        return "Impact: S&P 500 este referință pentru întreaga piață americană. [📈 Grafic SPX](https://www.tradingview.com/symbols/SPX/)"
    if "șomaj" in text or "somaj" in text or "locuri de muncă" in text:
        return "Impact: șomajul reflectă încrederea în economie – poate influența politica monetară."
    if "dobând" in text or "dobanz" in text or "bce" in text or "fed" in text:
        return "Impact: modificările de dobândă afectează direct evaluările companiilor."
    if "recesiune" in text or "contracție" in text or "contractie" in text:
        return "Impact: semnal negativ – investitorii pot reduce expunerea la acțiuni."
    if "creștere economică" in text or "pib" in text:
        return "Impact: creșterea economică susține piețele – pozitiv dacă depășește așteptările."
    if "profit" in text or "rezultate financiare" in text:
        return "Impact: relevant pentru acțiunile companiei și sectorul aferent."
    if "taxe" in text or "tvă" in text or "impozit" in text:
        return "Impact: politicile fiscale pot afecta competitivitatea companiilor."
    if "bvb" in text or "bursei de valori" in text:
        return "Impact: direct asupra pieței din România – urmărit îndeaproape. [📈 Grafic BET](https://tradingeconomics.com/romania/stock-market)"

    return "Impact: analiză necesară în funcție de contextul pieței."






# Încarcă titlurile salvate anterior
def incarca_titluri():
    if os.path.exists("trimise.json"):
        with open("trimise.json", "r") as f:
            return set(json.load(f))
    return set()

# Salvează titlurile noi
def salveaza_titluri(titluri):
    with open("trimise.json", "w") as f:
        json.dump(list(titluri), f)

last_titles = incarca_titluri()
print(f"S-au încărcat {len(last_titles)} titluri deja trimise din trimise.json.")


@tasks.loop(minutes=60)
async def fetch_news():
                        channel = bot.get_channel(CHANNEL_ID)
                        trimise = 0
                        for feed_url in rss_feeds:
                            feed = feedparser.parse(feed_url)
                            for entry in feed.entries:
                                title = entry.title
                                if title in last_titles:
                                    continue

                                link = entry.link
                                summary = entry.summary if "summary" in entry else ""
                                timestamp = datetime.datetime.now().strftime("%d %b %Y, %H:%M")

                                message = f"**{title}**\n*{timestamp}*\n\n{summary[:400]}...\n\n" \
                                          f"**{interpretare(title + summary)}**\n\n[Vezi articolul complet]({link})"
                                await channel.send(message)
                                last_titles.add(title)
                                salveaza_titluri(last_titles)
                                trimise += 1

                        if trimise == 0:
                            await channel.send(f"*Nu s-au găsit știri noi în ultima oră ({datetime.datetime.now().strftime('%H:%M')}).*")


bot.run(TOKEN)
