import uuid
import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from .keys import *

currentGroupsPVE = {}
currentGroupsGank = {}

pveGroupTemplate = {
    "time_utc": "",
    "raidLeader": "",
    "healer": "",
    "blazing": "",
    "frost_1": "",
    "frost_2": "",
    "debuff": "",
}
gankGroupTemplate = {}

allowed_mentions = nextcord.AllowedMentions(everyone = True)

class DropDown(nextcord.ui.View):
    answer_1 = None
    answer_2 = None

    @nextcord.ui.select(
            placeholder="Are you Gay?",
            options=[
                nextcord.SelectOption(label="1", value="1"),
                nextcord.SelectOption(label="2", value="2"),
                nextcord.SelectOption(label="3", value="3"),
            ]
    )
    async def select_age(self, interaction:nextcord.Integration, select_item:nextcord.ui.Select):
        self.answer_1 = select_item.values

class MassConfirmation(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.timeout  = None

    @nextcord.ui.button(style = nextcord.ButtonStyle.green, emoji = "✅", custom_id="confirmationButton")
    async def raidLeader(self, button: nextcord.ui.Button, interacion: Interaction):
        if currentGroupsPVE[self.id]["raidLeader"] == interacion.user.display_name:
            view = RolesStaticPVE()
            embed = nextcord.Embed(description="\n ПВЕ статик от убеги\n Gear: **8.0 пушка / 7.0 сет**\n Time: **"+currentGroupsPVE[self.id]["time_utc"]+" UTC ("+currentGroupsPVE[self.id]["time_msk"]+" МСК)**\n\n :one:  **| Raid Leader - @"+currentGroupsPVE[self.id]["raidLeader"]+"** \n :two:  **| Хил - "+currentGroupsPVE[self.id]["healer"]+"**\n :three:  **| Блейза - "+currentGroupsPVE[self.id]["blazing"]+"**\n :four:  **| Шишка - "+currentGroupsPVE[self.id]["frost_1"]+"**\n :five:  **| Шишка - "+currentGroupsPVE[self.id]["frost_2"]+"**\n :six:  **| Охотник / Ава курса - "+currentGroupsPVE[self.id]["debuff"]+"**")
            embed.set_author(name="PVE Static")
            message = await interacion.edit(embed=embed, view=view)
            currentGroupsPVE[interacion.message.id] = currentGroupsPVE[self.id]
            del currentGroupsPVE[self.id]
            thread = await interacion.message.create_thread(name = "Builds")
            await thread.edit(locked=True)
            await thread.send(content="Healer", file=nextcord.File("images\static_pve\static_pve_heal.png"))
            await thread.send(content="Blazing", file=nextcord.File("images\static_pve\static_pve_blazing.png"))
            await thread.send(content="Frost", file=nextcord.File("images\static_pve\static_pve_frost.png"))
            await thread.send(content="Shadow caller", file=nextcord.File("images\static_pve\static_pve_sc.png"))
        else:
            print("Someone else trying to confirm this content!")
        #await interacion.user.send(file=nextcord.File("images\static_pve\static_pve_sc.png"))

class RolesStaticPVE(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.timeout  = None

    @nextcord.ui.button(style = nextcord.ButtonStyle.green, emoji = "2️⃣")
    async def healer(self, button: nextcord.ui.Button, interacion: Interaction):
        if currentGroupsPVE[interacion.message.id]["healer"] == "" and interacion.user.display_name not in currentGroupsPVE[interacion.message.id].values():
            currentGroupsPVE[interacion.message.id]["healer"] = interacion.user.display_name
            view = RolesStaticPVE()  
            embed = nextcord.Embed(description="\n ПВЕ статик от убеги\n Gear: **8.0 пушка / 7.0 сет**\n Time: **"+currentGroupsPVE[interacion.message.id]["time_utc"]+" UTC ("+currentGroupsPVE[interacion.message.id]["time_msk"]+" МСК)**\n\n :one:  | **Raid Leader - "+currentGroupsPVE[interacion.message.id]["raidLeader"]+"** \n :two:  **| Хил - "+currentGroupsPVE[interacion.message.id]["healer"]+"**\n :three:  **| Блейза - "+currentGroupsPVE[interacion.message.id]["blazing"]+"**\n :four:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_1"]+"**\n :five:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_2"]+"**\n :six:  **| Ава курса - "+currentGroupsPVE[interacion.message.id]["debuff"]+"**")
            embed.set_author(name="PVE Static")
            message = await interacion.edit(embed=embed, view=view)
        elif currentGroupsPVE[interacion.message.id]["healer"] == interacion.user.display_name: 
            currentGroupsPVE[interacion.message.id]["healer"] = ""
            view = RolesStaticPVE()  
            embed = nextcord.Embed(description="\n ПВЕ статик от убеги\n Gear: **8.0 пушка / 7.0 сет**\n Time: **"+currentGroupsPVE[interacion.message.id]["time_utc"]+" UTC ("+currentGroupsPVE[interacion.message.id]["time_msk"]+" МСК)**\n\n :one:  | **Raid Leader - "+currentGroupsPVE[interacion.message.id]["raidLeader"]+"** \n :two:  **| Хил - "+currentGroupsPVE[interacion.message.id]["healer"]+"**\n :three:  **| Блейза - "+currentGroupsPVE[interacion.message.id]["blazing"]+"**\n :four:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_1"]+"**\n :five:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_2"]+"**\n :six:  **| Ава курса - "+currentGroupsPVE[interacion.message.id]["debuff"]+"**")
            embed.set_author(name="PVE Static")
            message = await interacion.edit(embed=embed, view=view)
        elif currentGroupsPVE[interacion.message.id]["healer"] == "" and interacion.user.display_name in currentGroupsPVE[interacion.message.id].values():
            print("Someone want more than one role")
        elif currentGroupsPVE[interacion.message.id]["healer"] != "":
            print("Healer role already assigned")
    
    @nextcord.ui.button(style = nextcord.ButtonStyle.green, emoji = "3️⃣")
    async def blazing(self, button: nextcord.ui.Button, interacion: Interaction):
        if currentGroupsPVE[interacion.message.id]["blazing"] == "" and interacion.user.display_name not in currentGroupsPVE[interacion.message.id].values():
            currentGroupsPVE[interacion.message.id]["blazing"] = interacion.user.display_name
            view = RolesStaticPVE()  
            embed = nextcord.Embed(description="\n ПВЕ статик от убеги\n Gear: **8.0 пушка / 7.0 сет**\n Time: **"+currentGroupsPVE[interacion.message.id]["time_utc"]+" UTC ("+currentGroupsPVE[interacion.message.id]["time_msk"]+" МСК)**\n\n :one:  | **Raid Leader - "+currentGroupsPVE[interacion.message.id]["raidLeader"]+"** \n :two:  **| Хил - "+currentGroupsPVE[interacion.message.id]["healer"]+"**\n :three:  **| Блейза - "+currentGroupsPVE[interacion.message.id]["blazing"]+"**\n :four:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_1"]+"**\n :five:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_2"]+"**\n :six:  **| Ава курса - "+currentGroupsPVE[interacion.message.id]["debuff"]+"**")
            embed.set_author(name="PVE Static")
            message = await interacion.edit(embed=embed, view=view)
        elif currentGroupsPVE[interacion.message.id]["blazing"] == interacion.user.display_name:
            currentGroupsPVE[interacion.message.id]["blazing"] = ""
            view = RolesStaticPVE()
            embed = nextcord.Embed(description="||@everyone||\n ПВЕ статик от убеги\n Gear: **8.0 пушка / 7.0 сет**\n Time: **"+currentGroupsPVE[interacion.message.id]["time_utc"]+" UTC ("+currentGroupsPVE[interacion.message.id]["time_msk"]+" МСК)**\n\n :one:  | **Raid Leader - "+currentGroupsPVE[interacion.message.id]["raidLeader"]+"** \n :two:  **| Хил - "+currentGroupsPVE[interacion.message.id]["healer"]+"**\n :three:  **| Блейза - "+currentGroupsPVE[interacion.message.id]["blazing"]+"**\n :four:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_1"]+"**\n :five:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_2"]+"**\n :six:  **| Ава курса - "+currentGroupsPVE[interacion.message.id]["debuff"]+"**")
            embed.set_author(name="PVE Static")
            message = await interacion.edit(embed=embed, view=view)
        elif currentGroupsPVE[interacion.message.id]["blazing"] == "" and interacion.user.display_name in currentGroupsPVE[interacion.message.id].values():
            print("Someone want more than one role")
        elif currentGroupsPVE[interacion.message.id]["blazing"] != "":
            print("Blazing role already assigned")
            

    @nextcord.ui.button(style = nextcord.ButtonStyle.green, emoji = "4️⃣")
    async def frost_1(self, button: nextcord.ui.Button, interacion: Interaction):
        if currentGroupsPVE[interacion.message.id]["frost_1"] == "" and interacion.user.display_name not in currentGroupsPVE[interacion.message.id].values():
            currentGroupsPVE[interacion.message.id]["frost_1"] = interacion.user.display_name
            view = RolesStaticPVE()  
            embed = nextcord.Embed(description="\n ПВЕ статик от убеги\n Gear: **8.0 пушка / 7.0 сет**\n Time: **"+currentGroupsPVE[interacion.message.id]["time_utc"]+" UTC ("+currentGroupsPVE[interacion.message.id]["time_msk"]+" МСК)**\n\n :one:  | **Raid Leader - "+currentGroupsPVE[interacion.message.id]["raidLeader"]+"** \n :two:  **| Хил - "+currentGroupsPVE[interacion.message.id]["healer"]+"**\n :three:  **| Блейза - "+currentGroupsPVE[interacion.message.id]["blazing"]+"**\n :four:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_1"]+"**\n :five:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_2"]+"**\n :six:  **| Ава курса - "+currentGroupsPVE[interacion.message.id]["debuff"]+"**")
            embed.set_author(name="PVE Static")
            message = await interacion.edit(embed=embed, view=view)
        elif currentGroupsPVE[interacion.message.id]["frost_1"] == interacion.user.display_name:
            currentGroupsPVE[interacion.message.id]["frost_1"] = ""
            view = RolesStaticPVE()  
            embed = nextcord.Embed(description="\n ПВЕ статик от убеги\n Gear: **8.0 пушка / 7.0 сет**\n Time: **"+currentGroupsPVE[interacion.message.id]["time_utc"]+" UTC ("+currentGroupsPVE[interacion.message.id]["time_msk"]+" МСК)**\n\n :one:  | **Raid Leader - "+currentGroupsPVE[interacion.message.id]["raidLeader"]+"** \n :two:  **| Хил - "+currentGroupsPVE[interacion.message.id]["healer"]+"**\n :three:  **| Блейза - "+currentGroupsPVE[interacion.message.id]["blazing"]+"**\n :four:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_1"]+"**\n :five:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_2"]+"**\n :six:  **| Ава курса - "+currentGroupsPVE[interacion.message.id]["debuff"]+"**")
            embed.set_author(name="PVE Static")
            message = await interacion.edit(embed=embed, view=view)
        elif currentGroupsPVE[interacion.message.id]["frost_1"] == "" and interacion.user.display_name in currentGroupsPVE[interacion.message.id].values():
            print("Someone want more than one role")
        elif currentGroupsPVE[interacion.message.id]["frost_1"] != "":
            print("Frost role already assigned")
    
    @nextcord.ui.button(style = nextcord.ButtonStyle.green, emoji = "5️⃣")
    async def frost_2(self, button: nextcord.ui.Button, interacion: Interaction):
        if currentGroupsPVE[interacion.message.id]["frost_2"] == "" and interacion.user.display_name not in currentGroupsPVE[interacion.message.id].values():
            currentGroupsPVE[interacion.message.id]["frost_2"] = interacion.user.display_name
            view = RolesStaticPVE()  
            embed = nextcord.Embed(description="\n ПВЕ статик от убеги\n Gear: **8.0 пушка / 7.0 сет**\n Time: **"+currentGroupsPVE[interacion.message.id]["time_utc"]+" UTC ("+currentGroupsPVE[interacion.message.id]["time_msk"]+" МСК)**\n\n :one:  | **Raid Leader - "+currentGroupsPVE[interacion.message.id]["raidLeader"]+"** \n :two:  **| Хил - "+currentGroupsPVE[interacion.message.id]["healer"]+"**\n :three:  **| Блейза - "+currentGroupsPVE[interacion.message.id]["blazing"]+"**\n :four:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_1"]+"**\n :five:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_2"]+"**\n :six:  **| Ава курса - "+currentGroupsPVE[interacion.message.id]["debuff"]+"**")
            embed.set_author(name="PVE Static")
            message = await interacion.edit(embed=embed, view=view)
        elif currentGroupsPVE[interacion.message.id]["frost_2"] == interacion.user.display_name:
            currentGroupsPVE[interacion.message.id]["frost_2"] = ""
            view = RolesStaticPVE()  
            embed = nextcord.Embed(description="\n ПВЕ статик от убеги\n Gear: **8.0 пушка / 7.0 сет**\n Time: **"+currentGroupsPVE[interacion.message.id]["time_utc"]+" UTC ("+currentGroupsPVE[interacion.message.id]["time_msk"]+" МСК)**\n\n :one:  | **Raid Leader - "+currentGroupsPVE[interacion.message.id]["raidLeader"]+"** \n :two:  **| Хил - "+currentGroupsPVE[interacion.message.id]["healer"]+"**\n :three:  **| Блейза - "+currentGroupsPVE[interacion.message.id]["blazing"]+"**\n :four:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_1"]+"**\n :five:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_2"]+"**\n :six:  **| Ава курса - "+currentGroupsPVE[interacion.message.id]["debuff"]+"**")
            embed.set_author(name="PVE Static")
            message = await interacion.edit(embed=embed, view=view)
        elif currentGroupsPVE[interacion.message.id]["frost_2"] == "" and interacion.user.display_name in currentGroupsPVE[interacion.message.id].values():
            print("Someone want more than one role")
        elif currentGroupsPVE[interacion.message.id]["frost_2"] != "":
            print("Frost role already assigned")

    @nextcord.ui.button(style = nextcord.ButtonStyle.green, emoji = "6️⃣")
    async def debuff(self, button: nextcord.ui.Button, interacion: Interaction):
        if currentGroupsPVE[interacion.message.id]["debuff"] == "" and interacion.user.display_name not in currentGroupsPVE[interacion.message.id].values():
            currentGroupsPVE[interacion.message.id]["debuff"] = interacion.user.display_name
            view = RolesStaticPVE()  
            embed = nextcord.Embed(description="\n ПВЕ статик от убеги\n Gear: **8.0 пушка / 7.0 сет**\n Time: **"+currentGroupsPVE[interacion.message.id]["time_utc"]+" UTC ("+currentGroupsPVE[interacion.message.id]["time_msk"]+" МСК)**\n\n :one:  | **Raid Leader - "+currentGroupsPVE[interacion.message.id]["raidLeader"]+"** \n :two:  **| Хил - "+currentGroupsPVE[interacion.message.id]["healer"]+"**\n :three:  **| Блейза - "+currentGroupsPVE[interacion.message.id]["blazing"]+"**\n :four:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_1"]+"**\n :five:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_2"]+"**\n :six:  **| Ава курса - "+currentGroupsPVE[interacion.message.id]["debuff"]+"**")
            embed.set_author(name="PVE Static")
            message = await interacion.edit(embed=embed, view=view)
        elif currentGroupsPVE[interacion.message.id]["debuff"] == interacion.user.display_name:
            currentGroupsPVE[interacion.message.id]["debuff"] = ""
            view = RolesStaticPVE()  
            embed = nextcord.Embed(description="\n ПВЕ статик от убеги\n Gear: **8.0 пушка / 7.0 сет**\n Time: **"+currentGroupsPVE[interacion.message.id]["time_utc"]+" UTC ("+currentGroupsPVE[interacion.message.id]["time_msk"]+" МСК)**\n\n :one:  | **Raid Leader - "+currentGroupsPVE[interacion.message.id]["raidLeader"]+"** \n :two:  **| Хил - "+currentGroupsPVE[interacion.message.id]["healer"]+"**\n :three:  **| Блейза - "+currentGroupsPVE[interacion.message.id]["blazing"]+"**\n :four:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_1"]+"**\n :five:  **| Шишка - "+currentGroupsPVE[interacion.message.id]["frost_2"]+"**\n :six:  **| Ава курса - "+currentGroupsPVE[interacion.message.id]["debuff"]+"**")
            embed.set_author(name="PVE Static")
            message = await interacion.edit(embed=embed, view=view)
        elif currentGroupsPVE[interacion.message.id]["debuff"] == "" and interacion.user.display_name in currentGroupsPVE[interacion.message.id].values():
            print("Someone want more than one role")
        elif currentGroupsPVE[interacion.message.id]["debuff"] != "":
            print("Frost role already assigned")

class RolesGank(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.timeout  = None
     
    @nextcord.ui.button(style = nextcord.ButtonStyle.green, emoji = "2️⃣")
    async def healer(self, button: nextcord.ui.Button, interacion: Interaction):
        await interacion.response.send_message("You are taked up Healer role", ephemeral = False)
    
    @nextcord.ui.button(style = nextcord.ButtonStyle.green, emoji = "3️⃣")
    async def bearpaws_1(self, button: nextcord.ui.Button, interacion: Interaction):
        await interacion.response.send_message("You are taked up Bearpaws role", ephemeral = False)

    @nextcord.ui.button(style = nextcord.ButtonStyle.green, emoji = "4️⃣")
    async def bearpaws_2(self, button: nextcord.ui.Button, interacion: Interaction):
        await interacion.response.send_message("You are taked up Bearpaws role", ephemeral = False)
    
    @nextcord.ui.button(style = nextcord.ButtonStyle.green, emoji = "5️⃣")
    async def doublebladed(self, button: nextcord.ui.Button, interacion: Interaction):
        await interacion.response.send_message("You are taked up Doublebladed staff role", ephemeral = False)

    @nextcord.ui.button(style = nextcord.ButtonStyle.green, emoji = "6️⃣")
    async def cursed(self, button: nextcord.ui.Button, interacion: Interaction):
        await interacion.response.send_message("You are taked up Cursed staff role", ephemeral = False)
        
    @nextcord.ui.button(style = nextcord.ButtonStyle.green, emoji = "7️⃣")
    async def claws(self, button: nextcord.ui.Button, interacion: Interaction):
        await interacion.response.send_message("You are taked up Claws role", ephemeral = False)

class Raid(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name = "massup", description = "Test slash command", guild_ids=[serverId])
    async def massup(self, interaction: Interaction, type: str, time_utc: str):
        member_role = interaction.guild.get_role(content_role_to_mention_id)
        time_words = time_utc.split(":")
        time_words[0] = int(time_words[0])+3
        if time_words[0] >= 24:
            time_words[0] = str(time_words[0] - 24)
        else:
            time_words[0] = str(time_words[0])
        print(time_words)
        time_msk = str(time_words[0])+":"+str(time_words[1])
        if type == "staticPVE":
            view = MassConfirmation()  
            embed = nextcord.Embed(description="\n ПВЕ статик от убеги\n Gear: **8.0 пушка / 7.0 сет**\n Time: **"+time_utc+" UTC ("+time_msk+" МСК)**\n\n :one:  | Raid Leader - ~~"+interaction.user.display_name+"~~\n :two:  | Хил -\n :three:  | Блейза -\n :four:  | Шишка -\n :five:  | Шишка - \n :six:  | Ава курса -")
            embed.set_author(name="PVE Static")
            message = await interaction.response.send_message(content=member_role.mention, embed=embed, view=view, allowed_mentions=allowed_mentions)
            currentGroupsPVE[view.id] = pveGroupTemplate.copy()
            currentGroupsPVE[view.id]["raidLeader"] = interaction.user.display_name
            currentGroupsPVE[view.id]["time_utc"] = time_utc
            currentGroupsPVE[view.id]["time_msk"] = time_msk
        elif type == "gank":
            view = MassConfirmation()  
            embed = nextcord.Embed(description="\n Ганк от убеги\n Gear: **8.0 эквивалент**\n Time: **"+time_utc+" UTC**\n\n :one:  | Булава - **Matvey4a** \n :two:  | Хил -\n :three:  | Бирики -\n :four:  | Бирики -\n :five:  | Шест - \n :six:  | Курса -\n :seven:  | Когти -")
            embed.set_author(name="Gank")
            message = await interaction.response.send_message(embed=embed, view=view, allowed_mentions=allowed_mentions)
        else:
            return
        if message:
            print(currentGroupsPVE)

def setup(client):
    client.add_cog(Raid(client))
