import random, time, json, copy, threading
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from datetime import datetime

from .keys import *

allowed_mentions = nextcord.AllowedMentions(everyone = True)

data_file_path = "bot_data/data.json"
comps_list_path = "bot_data/comps_list.json"
comps_list_data = []
contents_list_data = []

role_to_mention = content_role_to_mention_id

RaidGroupTemplate = {
    "content_date": "29.02.2024", # Format dd.mm.year
    "content_time": "14:45", # Format hh:mm (UTC)
    "content_title": "",
    "party_1": {
        "1": "",
        "2": "",
        "3": "",
        "4": "",
        "5": "",
        "6": "",
        "7": "",
        "8": "",
        "9": "",
        "10": "",
        "11": "",
        "12": "",
        "13": "",
        "14": "",
        "15": "",
        "16": "",
        "17": "",
        "18": "",
        "19": "",
        "20": "",
    },
    "party_2": {
        "21": "",
        "22": "",
        "23": "",
        "24": "",
        "25": "",
        "26": "",
        "27": "",
        "28": "",
        "29": "",
        "30": "",
        "31": "",
        "32": "",
        "33": "",
        "34": "",
        "35": "",
        "36": "",
        "37": "",
        "38": "",
        "39": "",
        "40": "",
    },
    "members": {
        "1": "",
        "2": "",
        "3": "",
        "4": "",
        "5": "",
        "6": "",
        "7": "",
        "8": "",
        "9": "",
        "10": "",
        "11": "",
        "12": "",
        "13": "",
        "14": "",
        "15": "",
        "16": "",
        "17": "",
        "18": "",
        "19": "",
        "20": "",
        "21": "",
        "22": "",
        "23": "",
        "24": "",
        "25": "",
        "26": "",
        "27": "",
        "28": "",
        "29": "",
        "30": "",
        "31": "",
        "32": "",
        "33": "",
        "34": "",
        "35": "",
        "36": "",
        "37": "",
        "38": "",
        "39": "",
        "40": "",
    },
    "content_id": "", # Unique content id
    "content_comp": "",
    "content_message_id": "",
    "images": {},
    "content_leader_id": "",
}
NewContentTemplate = {
        "comp_title": "",
        "party_1": {
            "1": "",
            "2": "",
            "3": "",
            "4": "",
            "5": "",
            "6": "",
            "7": "",
            "8": "",
            "9": "",
            "10": "",
            "11": "",
            "12": "",
            "13": "",
            "14": "",
            "15": "",
            "16": "",
            "17": "",
            "18": "",
            "19": "",
            "20": ""
        },
        "party_2": {
            "21": "",
            "22": "",
            "23": "",
            "24": "",
            "25": "",
            "26": "",
            "27": "",
            "28": "",
            "29": "",
            "30": "",
            "31": "",
            "32": "",
            "33": "",
            "34": "",
            "35": "",
            "36": "",
            "37": "",
            "38": "",
            "39": "",
            "40": ""
        },
        "images": {},
        "comp_creator_id": None,
}

# Generate unique content id
def GenerateUniqueContentId():
    def RandomInt(isFirstNumber = False):
        if isFirstNumber == True:
            return str(random.randint(1,9))
        else:
            return str(random.randint(0,9))
        
    new_conent_id = RandomInt(True)+RandomInt()+RandomInt()+RandomInt()+RandomInt()+RandomInt()

    all_contents_id = []
    with open(data_file_path, "r") as content_data:
        data = json.load(content_data)

    for i in data:
        all_contents_id.append(i["content_id"])
    
    if new_conent_id not in all_contents_id:
        content_data.close()
        return new_conent_id
    else:
        return GenerateUniqueContentId()

# Formating date for message output
def DateFormating(date:str):
    month_from_number = {
        "1": "January",
        "2": "February",
        "3": "March",
        "4": "April",
        "5": "May",
        "6": "June",
        "7": "July",
        "8": "August",
        "9": "September",
        "10": "October",
        "11": "November",
        "12": "December",
    }
    days_in_month = {
        "1": 31,
        "2": 28,
        "3": 31,
        "4": 30,
        "5": 31,
        "6": 30,
        "7": 31,
        "8": 30,
        "9": 31,
        "10": 30,
        "11": 31,
        "12": 30,
    }        
    
    splited_date = date.split(".")
    if int(splited_date[2]) % 4 == 0:
        days_in_month["2"] = 29
    if splited_date[1][0] == "0":
        splited_date[1] = splited_date[1][1]
    if splited_date[0][0] == "0":
        splited_date[0] = splited_date[0][1]
    
    if int(splited_date[0]) > days_in_month[splited_date[1]]:
        return "Date formating Error: non-existent day"

    try:
        formated_date = f"{splited_date[0]} {month_from_number[splited_date[1]]}"
        return str(formated_date)
    except:
        return "Date formating Error"

# Forating content time into utc and msk message output 
def TimeFormating(raid_time_utc:str):
    splited_time = raid_time_utc.split(":")
    temporary_raid_time_msk = int(splited_time[0]) + 3
    if temporary_raid_time_msk >= 24:
        temporary_raid_time_msk = str(temporary_raid_time_msk - 24)
    else:
        temporary_raid_time_msk = str(temporary_raid_time_msk)
    raid_time_msk = temporary_raid_time_msk + ":" + str(splited_time[1])

    return str(raid_time_utc), str(raid_time_msk)

def ClearOldData():
    current_date = datetime.utcnow().strftime('%d-%m-%Y').split("-")
    with open(data_file_path, "r") as data:
            contents_list_data = json.load(data)

    content_to_delete = []

    for i in range(len(contents_list_data)):
        content_date = contents_list_data[i]["content_date"].split(".")
        if current_date[2] > content_date[2]:
            content_to_delete.append(contents_list_data[i]["content_id"])
        if current_date[2] == content_date[2] and current_date[1] > content_date[1]:
            content_to_delete.append(contents_list_data[i]["content_id"])
        if current_date[2] == content_date[2] and current_date[1] == content_date[1] and current_date[0] > content_date[0]:
            content_to_delete.append(contents_list_data[i]["content_id"])
    
    for i in range(len(content_to_delete)):
        CancelContent(content_id=content_to_delete[i])     

    print(f"OLD data cleared, {len(content_to_delete)}  contents deleted!")

def StartClearData():
    while True:
        time.sleep(clear_old_data_time)
        ClearOldData()

# Add new content to all contents list JSON file 
def AddNewComp(content_title:str, roles:str, comp_creator_id:int):
    new_comp = copy.deepcopy(NewContentTemplate)
    new_comp["comp_title"] = content_title
    new_comp["comp_creator_id"] = comp_creator_id
    splited_roles = roles.split(";")
    roles_number = len(splited_roles)
    
    with open(comps_list_path) as comps_list:
        comps_list_data = json.load(comps_list)
    
    comps_list.close()

    for i in range(roles_number):
        if splited_roles[i][0] == " ":
            splited_roles[i] = splited_roles[i][1:64]
    
    for i in range(roles_number):
        current_role_id = i + 1
        if current_role_id <= 20:
            new_comp["party_1"][str(current_role_id)] = splited_roles[i]
        elif current_role_id > 20:
            new_comp["party_2"][str(current_role_id)] = splited_roles[i]
    
    comps_list_data.append(new_comp)

    with open(comps_list_path, "w") as comps_list:
        json.dump(comps_list_data, comps_list, indent=4, separators=(",", ": "))

    comps_list.close()

def UpdateComp(comp_title:str, roles:str):
    new_comp = copy.deepcopy(NewContentTemplate)
    splited_roles = roles.split(";")
    roles_number = len(splited_roles)

    with open(comps_list_path) as comps_list:
        comps_list_data = json.load(comps_list)
    comps_list.close()

    for i in range(roles_number):
        if splited_roles[i][0] == " ":
            splited_roles[i] = splited_roles[i][1:64]

    for comp in comps_list_data:
        if comp["comp_title"] == comp_title:
            comp["party_1"] = new_comp["party_1"]
            comp["party_2"] = new_comp["party_2"]
            for i in range(roles_number):
                current_role_id = i + 1
                if current_role_id <= 20:
                    comp["party_1"][str(current_role_id)] = splited_roles[i]
                elif current_role_id > 20:
                    comp["party_2"][str(current_role_id)] = splited_roles[i]
            break
            
    with open(comps_list_path, "w") as comps_list:
        json.dump(comps_list_data, comps_list, indent=4, separators=(",", ": "))

    comps_list.close()

# Add an existing content from all contents list JSON file 
def RemoveComp(content_title:str):
    with open(comps_list_path, "r") as comps_list:
        comps_list_data = json.load(comps_list)

    for i in range(len(comps_list_data)):
        if comps_list_data[i]["comp_title"] == content_title:
            del comps_list_data[i]
            break

    with open(comps_list_path, "w") as comps_list:
        json.dump(comps_list_data, comps_list, indent=4, separators=(",", ": "))

    comps_list.close()

def StartNewContent(comp_title:str, content_title:str, content_date:str, content_time:str, content_leader_id: int):
    with open(comps_list_path, "r") as comps_list:
        comps_list_data = json.load(comps_list)
    
    comp = {}
    for i in range(len(comps_list_data)):
        if comps_list_data[i]["comp_title"] == comp_title:
            comp = comps_list_data[i]
    
    new_content = RaidGroupTemplate.copy()
    new_content["content_id"] = GenerateUniqueContentId()
    new_content["content_title"] = content_title
    new_content["content_time"] = content_time
    new_content["content_date"] = content_date
    new_content["party_1"] = comp["party_1"]
    new_content["party_2"] = comp["party_2"]
    new_content["content_comp"] = comp["comp_title"]
    new_content["content_leader_id"] = content_leader_id
    if len(comp["images"]) != 0:
        new_content["images"] = comp["images"]

    with open(data_file_path) as contents_list:
        contents_list_data = json.load(contents_list)
    
    contents_list_data.append(new_content)

    with open(data_file_path, "w") as contents_list:
        json.dump(contents_list_data, contents_list, indent=4, separators=(",", ": "))

    contents_list.close()
    return new_content["content_id"]

def CancelContent(content_id:str):
    with open(data_file_path, "r") as contents_list:
        contents_list_data = json.load(contents_list)

    for i in range(len(contents_list_data)):
        if contents_list_data[i]["content_id"] == content_id:
            del contents_list_data[i]
            break

    with open(data_file_path, "w") as contents_list:
        json.dump(contents_list_data, contents_list, indent=4, separators=(",", ": "))

    contents_list.close()

def UpdateContent(content_id:str, variable_to_update:str, new_variable_value):
    content_for_update = {}

    with open(data_file_path, "r") as contents_list:
        contents_list_data = json.load(contents_list)

    for i in range(len(contents_list_data)):
        if contents_list_data[i]["content_id"] == content_id:
            try:
                contents_list_data[i][str(variable_to_update)] = new_variable_value
            except:
                print(f"Failed to update cotent value {variable_to_update}")
            break

    contents_list.close()
    
    with open(data_file_path, "w") as contents_list:
        json.dump(contents_list_data, contents_list, indent=4, separators=(",", ": "))

    contents_list.close()

def UpdateMemberInContent(content_id:str, update_state:str, member_id:int, role_id:str = None):
    with open(data_file_path, "r") as contents_list:
        contents_list_data = json.load(contents_list)

    for i in range(len(contents_list_data)):
        if contents_list_data[i]["content_id"] == content_id:
            if update_state == "signup":
                if member_id not in contents_list_data[i]["members"].values():
                    for x in range(len(contents_list_data[i]["members"])):
                        if str(x+1) == str(role_id):
                            contents_list_data[i]["members"][str(x+1)] = member_id
                else:
                    for x in range(len(contents_list_data[i]["members"])):
                        if contents_list_data[i]["members"][str(x+1)] == member_id:
                            contents_list_data[i]["members"][str(x+1)] = ""
                        if str(x+1) == str(role_id):
                            contents_list_data[i]["members"][str(x+1)] = member_id
            elif update_state == "kick":
                for x in range(len(contents_list_data[i]["members"])):
                    if contents_list_data[i]["members"][str(x+1)] == member_id:
                        contents_list_data[i]["members"][str(x+1)] = ""
            elif update_state == "changerole":
                for x in range(len(contents_list_data[i]["members"])):
                    if contents_list_data[i]["members"][str(x+1)] == member_id:
                        contents_list_data[i]["members"][str(x+1)] = ""
                    elif str(x+1) == role_id:
                        contents_list_data[i]["members"][str(x+1)] = member_id
            break
    
    with open(data_file_path, "w") as contents_list:
        json.dump(contents_list_data, contents_list, indent=4, separators=(",", ": "))

    contents_list.close()

# Dropdown Selection Menu, role assignment
class RoleSelect(nextcord.ui.Select):
    def __init__(self):
        super().__init__(min_values=1, max_values=1)
        self.original_message = None

    async def callback(self, interaction:nextcord.Interaction):
        content_data = {}
        role_id = self.values[0]

        with open(data_file_path, "r") as contents_list:
            contents_list_data = json.load(contents_list)

        for i in range(len(contents_list_data)):
            if contents_list_data[i]["content_id"] == self.original_message.embeds[0]._footer["text"][12:18]:
                for x in range(len(contents_list_data[i]["members"])):
                    if contents_list_data[i]["members"][str(x+1)] == interaction.user.id:
                        contents_list_data[i]["members"][str(x+1)] = ""

                if contents_list_data[i]["members"][str(role_id)] == "":
                    if interaction.user.id not in contents_list_data[i]["members"].values():
                        contents_list_data[i]["members"][str(role_id)] = interaction.user.id
                content_data = contents_list_data[i]

                with open(data_file_path, "w") as contents_list:
                    json.dump(contents_list_data, contents_list, indent=4, separators=(",", ": "))

                time_utc, time_msk = TimeFormating(content_data["content_time"])
                embed = nextcord.Embed(description=f"Date: **{DateFormating(content_data['content_date'])}**\nTime: **{time_utc} (UTC) | {time_msk} (МСК)**", colour=0xe3eed8)
                embed.set_author(name=content_data["content_title"])

                if content_data["party_2"]["21"] == "":
                    party_1_string = ""  
                    for i in range(len(content_data["party_1"])):
                        if content_data["party_1"][str(i+1)] != "" and content_data["members"][str(i+1)] == "":
                            party_1_string = party_1_string + f"🟨 {str(i+1)}. {content_data['party_1'][str(i+1)]}\n"
                        elif content_data["party_1"][str(i+1)] != "" and content_data["members"][str(i+1)] != "":
                            party_1_string = party_1_string + f"✅ {str(i+1)}. {content_data['party_1'][str(i+1)]} - <@{content_data['members'][str(i+1)]}>\n"
                    embed.add_field(name="⚔️ Party 1", value=party_1_string, inline=True)
                elif content_data["party_2"]["21"] != "":
                    party_1_string = ""  
                    for i in range(len(content_data["party_1"])):
                        if content_data["party_1"][str(i+1)] != "" and content_data["members"][str(i+1)] == "":
                            party_1_string = party_1_string + f"🟨 {str(i+1)}. {content_data['party_1'][str(i+1)]}\n"
                        elif content_data["party_1"][str(i+1)] != "" and content_data["members"][str(i+1)] != "":
                            party_1_string = party_1_string + f"✅ {str(i+1)}. {content_data['party_1'][str(i+1)]} - <@{content_data['members'][str(i+1)]}>\n"
                    embed.add_field(name="⚔️ Party 1", value=party_1_string, inline=True)
                    party_2_string = ""  
                    for i in range(20,len(content_data["party_2"])+20):
                        if content_data["party_2"][str(i+1)] != "" and content_data["members"][str(i+1)] == "":
                            party_2_string = party_2_string + f"🟨 {str(i+1)}. {content_data['party_2'][str(i+1)]}\n"
                        elif content_data["party_2"][str(i+1)] != "" and content_data["members"][str(i+1)] != "":
                            party_2_string = party_2_string + f"✅ {str(i+1)}. {content_data['party_2'][str(i+1)]} - <@{content_data['members'][str(i+1)]}>\n"
                    embed.add_field(name="⚔️ Party 2", value=party_2_string, inline=True)

                embed.set_footer(text=f"content_id: {content_data['content_id']}")

                await self.original_message.edit(embed=embed, allowed_mentions=allowed_mentions)
                await interaction.response.edit_message(content="Success", view=None, embed=None, delete_after=.3)
                                
                contents_list.close()

                break              

class DropDown(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = None

class MainButtons(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.timeout = None

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="Join", custom_id="join_button")
    async def join(self, button: nextcord.ui.Button, interacion: Interaction):
        view = DropDown()
        role_select = RoleSelect()
        role_select.original_message = interacion.message

        content_id = interacion.message.embeds[0]._footer["text"][12:18]
        content_data = {}
        with open(data_file_path, "r") as contents_list:
            contents_list_data = json.load(contents_list)

        for i in range(len(contents_list_data)):
            if contents_list_data[i]["content_id"] == content_id:
                content_data = contents_list_data[i]
                break
        
        for i in range(len(content_data["party_1"])):
            if content_data["party_1"][str(i+1)] != "" and content_data["members"][str(i+1)] == "":
                role_select.add_option(label=f"{str(i+1)}. {content_data['party_1'][str(i+1)]}", value=str(i+1))
        if content_data["party_2"]["21"] != "":
            for i in range(20,len(content_data["party_2"])+20):
                if content_data["party_2"][str(i+1)] != "" and content_data["members"][str(i+1)] == "":
                    role_select.add_option(label=f"{str(i+1)}. {content_data['party_2'][str(i+1)]}", value=str(i+1))

        view.add_item(role_select)

        await interacion.send(content="Let's choose your role.", view=view, ephemeral=True)
    
    @nextcord.ui.button(style=nextcord.ButtonStyle.red, label="Leave", custom_id="leave_button")
    async def leave(self, button: nextcord.ui.Button, interaction: Interaction):
        content_data = {}

        with open(data_file_path, "r") as contents_list:
            contents_list_data = json.load(contents_list)

        for i in range(len(contents_list_data)):
            if contents_list_data[i]["content_id"] == interaction.message.embeds[0]._footer["text"][12:18]:
                for x in range(len(contents_list_data[i]["members"])):
                    if contents_list_data[i]["members"][str(x+1)] == interaction.user.id:
                        contents_list_data[i]["members"][str(x+1)] = ""
                content_data = contents_list_data[i]

                with open(data_file_path, "w") as contents_list:
                    json.dump(contents_list_data, contents_list, indent=4, separators=(",", ": "))
                time_utc, time_msk = TimeFormating(content_data["content_time"])
                embed = nextcord.Embed(description=f"Date: **{DateFormating(content_data['content_date'])}**\nTime: **{time_utc} (UTC) | {time_msk} (МСК)**", colour=0xe3eed8)
                embed.set_author(name=content_data["content_title"])

                if content_data["party_2"]["21"] == "":
                    party_1_string = ""  
                    for i in range(len(content_data["party_1"])):
                        if content_data["party_1"][str(i+1)] != "" and content_data["members"][str(i+1)] == "":
                            party_1_string = party_1_string + f"🟨 {str(i+1)}. {content_data['party_1'][str(i+1)]}\n"
                        elif content_data["party_1"][str(i+1)] != "" and content_data["members"][str(i+1)] != "":
                            party_1_string = party_1_string + f"✅ {str(i+1)}. {content_data['party_1'][str(i+1)]} - <@{content_data['members'][str(i+1)]}>\n"
                    embed.add_field(name="⚔️ Party 1", value=party_1_string, inline=True)
                elif content_data["party_2"]["21"] != "":
                    party_1_string = ""  
                    for i in range(len(content_data["party_1"])):
                        if content_data["party_1"][str(i+1)] != "" and content_data["members"][str(i+1)] == "":
                            party_1_string = party_1_string + f"🟨 {str(i+1)}. {content_data['party_1'][str(i+1)]}\n"
                        elif content_data["party_1"][str(i+1)] != "" and content_data["members"][str(i+1)] != "":
                            party_1_string = party_1_string + f"✅ {str(i+1)}. {content_data['party_1'][str(i+1)]} - <@{content_data['members'][str(i+1)]}>\n"
                    embed.add_field(name="⚔️ Party 1", value=party_1_string, inline=True)
                    party_2_string = ""  
                    for i in range(20,len(content_data["party_2"])+20):
                        if content_data["party_2"][str(i+1)] != "" and content_data["members"][str(i+1)] == "":
                            party_2_string = party_2_string + f"🟨 {str(i+1)}. {content_data['party_2'][str(i+1)]}\n"
                        elif content_data["party_2"][str(i+1)] != "" and content_data["members"][str(i+1)] != "":
                            party_2_string = party_2_string + f"✅ {str(i+1)}. {content_data['party_2'][str(i+1)]} - <@{content_data['members'][str(i+1)]}>\n"
                    embed.add_field(name="⚔️ Party 2", value=party_2_string, inline=True)

                embed.set_footer(text=f"content_id: {content_data['content_id']}")

                await interaction.message.edit(embed=embed, allowed_mentions=allowed_mentions)

    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, label="Ping 📢", custom_id="ping_button")
    async def ping(self, button: nextcord.ui.Button, interaction: Interaction):
        content_data = {}

        with open(data_file_path, "r") as contents_list:
            contents_list_data = json.load(contents_list)

        for i in range(len(contents_list_data)):
            if contents_list_data[i]["content_id"] == interaction.message.embeds[0]._footer["text"][12:18]:
                content_data = contents_list_data[i]
                break

        if content_data["content_leader_id"] == interaction.user.id:
            members_to_ping = content_data["members"]

            ping_string = ""

            for i in range(len(members_to_ping)):
                print(str(members_to_ping[str(i+1)]))
                if str(members_to_ping[str(i+1)]) != "":
                    ping_string = ping_string + f"<@{str(members_to_ping[str(i+1)])}>"

            if ping_string != "":
                ping_string = ping_string + " Content massing now!"
                await interaction.response.send_message(content=ping_string)
            else:
                await interaction.response.send_message(content="No players on content", ephemeral=True, delete_after=3)
        else:
            await interaction.response.send_message(content="You're not the leader of content!", ephemeral=True, delete_after=3)

class Content(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="content", description="Make content ping", guild_ids=[serverId])
    async def content(
        self,
        interaction:Interaction,
        content_title:str = nextcord.SlashOption(description="Content Title"), 
        content_comp:str = nextcord.SlashOption(description="Content composition"),
        content_date:str = nextcord.SlashOption(description="Content date (dd.mm.yyyy)"),
        content_time:str = nextcord.SlashOption(description="Content time UTC (hh:mm)"),
        ):
        content_id = StartNewContent(content_comp, content_title, content_date, content_time, interaction.user.id)
        member_role = interaction.guild.get_role(role_to_mention) # Mention some role
        time_utc, time_msk = TimeFormating(content_time)
        embed = nextcord.Embed(description=f"Date: **{DateFormating(content_date)}**\nTime: **{time_utc} (UTC) | {time_msk} (МСК)**", colour=0xe3eed8)
        embed.set_author(name=content_title)

        view = MainButtons()

        with open(comps_list_path, "r") as comps_list:
            comps_list_data = json.load(comps_list)
    
        comp = {}
        for i in range(len(comps_list_data)):
            if comps_list_data[i]["comp_title"] == content_comp:
                comp = comps_list_data[i]

        if comp["party_2"]["21"] == "":
            party_1_string = ""  
            for i in range(len(comp["party_1"])):
                if comp["party_1"][str(i+1)] != "":
                    party_1_string = party_1_string + f"🟨 {str(i+1)}. {comp['party_1'][str(i+1)]}\n"
            embed.add_field(name="⚔️ Party 1", value=party_1_string, inline=True)
        elif comp["party_2"]["21"] != "":
            party_1_string = ""  
            for i in range(len(comp["party_1"])):
                if comp["party_1"][str(i+1)] != "":
                    party_1_string = party_1_string + f"🟨 {str(i+1)}. {comp['party_1'][str(i+1)]}\n"
            embed.add_field(name="⚔️ Party 1", value=party_1_string, inline=True)
            party_2_string = ""  
            for i in range(20,len(comp["party_2"])+20):
                if comp["party_2"][str(i+1)] != "":
                    party_2_string = party_2_string + f"🟨 {str(i+1)}. {comp['party_2'][str(i+1)]}\n"
            embed.add_field(name="⚔️ Party 2", value=party_2_string, inline=True)

        embed.set_footer(text=f"content_id: {content_id}")

        message = await interaction.response.send_message(content=member_role.mention, view=view, embed=embed, allowed_mentions=allowed_mentions)
        full_message = await message.fetch()
        message_id = full_message.id

        content_data = {}

        with open(data_file_path, "r") as contents_list:
            contents_list_data = json.load(contents_list)

        for i in range(len(contents_list_data)):
            if contents_list_data[i]["content_id"] == content_id:
                content_data = contents_list_data[i]
        content_data["content_message_id"] = message_id

        contents_list.close()

        with open(data_file_path, "w") as contents_list:
            json.dump(contents_list_data, contents_list, indent=4, separators=(",", ": "))

        thread = await full_message.create_thread(name = "Builds / Q&A")
        await thread.edit(locked=False)

        if len(content_data["images"]) != 0:
            for i in content_data["images"]:
                await thread.send(content="", file=nextcord.File(str(content_data["images"][i])))
        else:
            print("No Images in content comp")

        contents_list.close()
        comps_list.close()
        
    @nextcord.slash_command(name="newcomp", description="Make new content composition", guild_ids=[serverId])
    async def newComp(
        self,
        interaction:Interaction,
        content_title:str = nextcord.SlashOption(description="Content Title"), 
        roles:str = nextcord.SlashOption(description="Write roles splited by (; )"),
        ):
        AddNewComp(content_title=content_title, roles=roles, comp_creator_id=interaction.user.id)
        await interaction.response.send_message(content="Successfuly created new content composition!", ephemeral=True, delete_after=3)

    @nextcord.slash_command(name="updatecomp", description="Update an existing content composition", guild_ids=[serverId])
    async def updateComp(
            self,
            interaction:Interaction,
            comp_title:str = nextcord.SlashOption(description="Comp Title"), 
            roles:str = nextcord.SlashOption(description="Write roles splited by (; )"),
        ):

        comp_creator_id = None

        with open(comps_list_path, "r") as comps_list:
            contents_list_data = json.load(comps_list)
            for data in contents_list_data:
                if data["comp_title"] == comp_title:
                    comp_creator_id = data["comp_creator_id"]
                    break
        
        if comp_creator_id == interaction.user.id:
            UpdateComp(comp_title=comp_title, roles=roles)
            await interaction.response.send_message(content="Successfuly updated content composition!", ephemeral=True, delete_after=3)
        else:
            await interaction.response.send_message(content="You're not comp creator", ephemeral=True, delete_after=3)

    @nextcord.slash_command(name="removecomp", description="Remove content composition", guild_ids=[serverId])
    async def removeComp(
        self,
        interaction:Interaction,
        comp_title:str = nextcord.SlashOption(description="Comp Title"), 
        ):

        comp_creator_id = None

        with open(comps_list_path, "r") as comps_list:
            contents_list_data = json.load(comps_list)
            for data in contents_list_data:
                if data["comp_title"] == comp_title:
                    comp_creator_id = data["comp_creator_id"]
                    break
        
        if comp_creator_id == interaction.user.id:
            RemoveComp(content_title=comp_title)
            await interaction.response.send_message(content="Successfuly removed content composition!", ephemeral=True, delete_after=3)
        else:
            await interaction.response.send_message(content="You're not comp creator", ephemeral=True, delete_after=3)

    @nextcord.slash_command(name="compslist", description="Show all content compositions", guild_ids=[serverId])
    async def compsList(
        self,
        interaction:Interaction,
        ):

        with open(comps_list_path, "r") as comps_list:
            comps_list_data = json.load(comps_list)

        comps = ""
        for i in range(len(comps_list_data)):
            comps = comps + f"{comps_list_data[i]['comp_title']} \n"

        embed = nextcord.Embed(colour=0xd15400)

        embed.add_field(name="", value=comps, inline=True)

        await interaction.response.send_message(content="", ephemeral=True, embed=embed)
    
    @nextcord.slash_command(name="cancelcontent", description="Cancel content by content_id", guild_ids=[serverId])
    async def cancelcontent(
        self,
        interaction:Interaction,
        content_id:str = nextcord.SlashOption(description="Content ID"),
        ):

        content_leader_id = None
        message_id = None

        with open(data_file_path, "r") as data:
            contents_list_data = json.load(data)
        
        for i in range(len(contents_list_data)):
            if contents_list_data[i]["content_id"] == content_id:
                message_id = contents_list_data[i]["content_message_id"]
                content_leader_id = contents_list_data[i]["content_leader_id"]

        if content_leader_id == interaction.user.id:
            CancelContent(content_id=content_id)

            message = await interaction.channel.fetch_message(message_id)
            await message.delete()
            await interaction.response.send_message(content=f"Successfuly canceled content ({content_id})", ephemeral=True, delete_after=3)
        else:
            await interaction.response.send_message(content=f"You're not hosting this content ({content_id})", ephemeral=True, delete_after=3)

    @nextcord.slash_command(name="signupmember", description="Sign up member to content by content_id and member name", guild_ids=[serverId])
    async def signupmember(
            self,
            interaction: Interaction,
            content_id:str = nextcord.SlashOption(description="Content ID"),
            member_name:str = nextcord.SlashOption(description="@PlayerNickname"),
            role_id: int = nextcord.SlashOption(description="Role Number"),
        ):

        content_to_update = {}
        message_id = None
        content_leader_id = None

        with open(data_file_path, "r") as contents_list:
            contents_list_data = json.load(contents_list)
            for data in contents_list_data:
                if data["content_id"] == content_id:
                    content_leader_id = data["content_leader_id"]
                    break
        contents_list.close()
        
        if content_leader_id == interaction.user.id:
            member_id = member_name[2:-1]
            UpdateMemberInContent(content_id, "signup", int(member_id), role_id)

            with open(data_file_path, "r") as contents_list:
                contents_list_data = json.load(contents_list)
                for data in contents_list_data:
                    if data["content_id"] == content_id:
                        content_to_update = data
                        message_id = data["content_message_id"]
                        break
            contents_list.close()
            
            time_utc, time_msk = TimeFormating(content_to_update["content_time"])
            embed = nextcord.Embed(description=f"Date: **{DateFormating(content_to_update['content_date'])}**\nTime: **{time_utc} (UTC) | {time_msk} (МСК)**", colour=0xe3eed8)
            embed.set_author(name=content_to_update["content_title"])

            if content_to_update["party_2"]["21"] == "":
                party_1_string = ""  
                for i in range(len(content_to_update["party_1"])):
                    if content_to_update["party_1"][str(i+1)] != "" and content_to_update["members"][str(i+1)] == "":
                        party_1_string = party_1_string + f"🟨 {str(i+1)}. {content_to_update['party_1'][str(i+1)]}\n"
                    elif content_to_update["party_1"][str(i+1)] != "" and content_to_update["members"][str(i+1)] != "":
                        party_1_string = party_1_string + f"✅ {str(i+1)}. {content_to_update['party_1'][str(i+1)]} - <@{content_to_update['members'][str(i+1)]}>\n"
                embed.add_field(name="⚔️ Party 1", value=party_1_string, inline=True)
            elif content_to_update["party_2"]["21"] != "":
                party_1_string = ""  
                for i in range(len(content_to_update["party_1"])):
                    if content_to_update["party_1"][str(i+1)] != "" and content_to_update["members"][str(i+1)] == "":
                        party_1_string = party_1_string + f"🟨 {str(i+1)}. {content_to_update['party_1'][str(i+1)]}\n"
                    elif content_to_update["party_1"][str(i+1)] != "" and content_to_update["members"][str(i+1)] != "":
                        party_1_string = party_1_string + f"✅ {str(i+1)}. {content_to_update['party_1'][str(i+1)]} - <@{content_to_update['members'][str(i+1)]}>\n"
                embed.add_field(name="⚔️ Party 1", value=party_1_string, inline=True)
                party_2_string = ""  
                for i in range(20,len(content_to_update["party_2"])+20):
                    if content_to_update["party_2"][str(i+1)] != "" and content_to_update["members"][str(i+1)] == "":
                        party_2_string = party_2_string + f"🟨 {str(i+1)}. {content_to_update['party_2'][str(i+1)]}\n"
                    elif content_to_update["party_2"][str(i+1)] != "" and content_to_update["members"][str(i+1)] != "":
                        party_2_string = party_2_string + f"✅ {str(i+1)}. {content_to_update['party_2'][str(i+1)]} - <@{content_to_update['members'][str(i+1)]}>\n"
                embed.add_field(name="⚔️ Party 2", value=party_2_string, inline=True)

            embed.set_footer(text=f"content_id: {content_to_update['content_id']}")

            message = await interaction.channel.fetch_message(message_id)
            await message.edit(embed=embed, allowed_mentions=allowed_mentions)
            await interaction.response.send_message(content="Success", ephemeral=True, delete_after=.5)
                                    
            contents_list.close()
        else:
            await interaction.response.send_message(content="You're not the leader of content!", ephemeral=True, delete_after=3)

    @nextcord.slash_command(name="kickoffmember", description="Kick off member from content by content_id and member name", guild_ids=[serverId])
    async def kickoffmember(
            self,
            interaction: Interaction,
            content_id:str = nextcord.SlashOption(description="Content ID"),
            member_name:str = nextcord.SlashOption(description="@PlayerNickname"),
        ):

        content_to_update = {}
        message_id = None
        content_leader_id = None

        with open(data_file_path, "r") as contents_list:
            contents_list_data = json.load(contents_list)
            for data in contents_list_data:
                if data["content_id"] == content_id:
                    content_leader_id = data["content_leader_id"]
                    break
        contents_list.close()
        
        if content_leader_id == interaction.user.id:
            member_id = member_name[2:-1]
            UpdateMemberInContent(content_id, "kick", int(member_id))

            with open(data_file_path, "r") as contents_list:
                contents_list_data = json.load(contents_list)
                for data in contents_list_data:
                    if data["content_id"] == content_id:
                        content_to_update = data
                        message_id = data["content_message_id"]
                        break
            
            time_utc, time_msk = TimeFormating(content_to_update["content_time"])
            embed = nextcord.Embed(description=f"Date: **{DateFormating(content_to_update['content_date'])}**\nTime: **{time_utc} (UTC) | {time_msk} (МСК)**", colour=0xe3eed8)
            embed.set_author(name=content_to_update["content_title"])

            if content_to_update["party_2"]["21"] == "":
                party_1_string = ""  
                for i in range(len(content_to_update["party_1"])):
                    if content_to_update["party_1"][str(i+1)] != "" and content_to_update["members"][str(i+1)] == "":
                        party_1_string = party_1_string + f"🟨 {str(i+1)}. {content_to_update['party_1'][str(i+1)]}\n"
                    elif content_to_update["party_1"][str(i+1)] != "" and content_to_update["members"][str(i+1)] != "":
                        party_1_string = party_1_string + f"✅ {str(i+1)}. {content_to_update['party_1'][str(i+1)]} - <@{content_to_update['members'][str(i+1)]}>\n"
                embed.add_field(name="⚔️ Party 1", value=party_1_string, inline=True)
            elif content_to_update["party_2"]["21"] != "":
                party_1_string = ""  
                for i in range(len(content_to_update["party_1"])):
                    if content_to_update["party_1"][str(i+1)] != "" and content_to_update["members"][str(i+1)] == "":
                        party_1_string = party_1_string + f"🟨 {str(i+1)}. {content_to_update['party_1'][str(i+1)]}\n"
                    elif content_to_update["party_1"][str(i+1)] != "" and content_to_update["members"][str(i+1)] != "":
                        party_1_string = party_1_string + f"✅ {str(i+1)}. {content_to_update['party_1'][str(i+1)]} - <@{content_to_update['members'][str(i+1)]}>\n"
                embed.add_field(name="⚔️ Party 1", value=party_1_string, inline=True)
                party_2_string = ""  
                for i in range(20,len(content_to_update["party_2"])+20):
                    if content_to_update["party_2"][str(i+1)] != "" and content_to_update["members"][str(i+1)] == "":
                        party_2_string = party_2_string + f"🟨 {str(i+1)}. {content_to_update['party_2'][str(i+1)]}\n"
                    elif content_to_update["party_2"][str(i+1)] != "" and content_to_update["members"][str(i+1)] != "":
                        party_2_string = party_2_string + f"✅ {str(i+1)}. {content_to_update['party_2'][str(i+1)]} - <@{content_to_update['members'][str(i+1)]}>\n"
                embed.add_field(name="⚔️ Party 2", value=party_2_string, inline=True)

            embed.set_footer(text=f"content_id: {content_to_update['content_id']}")

            message = await interaction.channel.fetch_message(message_id)
            await message.edit(embed=embed, allowed_mentions=allowed_mentions)
            await interaction.response.send_message(content="Success", ephemeral=True, delete_after=.5)
                                    
            contents_list.close()
        else:
            await interaction.response.send_message(content="You're not the leader of content!", ephemeral=True, delete_after=3)

    @nextcord.slash_command(name="changedate", description="Change date in content by content_id", guild_ids=[serverId])
    async def changedate(
            self,
            interaction:Interaction,
            content_id:str = nextcord.SlashOption(description="Content ID"),
            new_date:str = nextcord.SlashOption(description="New content date"),
        ):

        content_to_update = {}
        message_id = None
        content_leader_id = None

        with open(data_file_path, "r") as contents_list:
            contents_list_data = json.load(contents_list)
            for data in contents_list_data:
                if data["content_id"] == content_id:
                    content_leader_id = data["content_leader_id"]
                    break
        contents_list.close()
        
        if content_leader_id == interaction.user.id:
            UpdateContent(content_id, "content_date", new_date)

            with open(data_file_path, "r") as contents_list:
                contents_list_data = json.load(contents_list)
                for data in contents_list_data:
                    if data["content_id"] == content_id:
                        content_to_update = data
                        message_id = data["content_message_id"]
                        break

            time_utc, time_msk = TimeFormating(content_to_update["content_time"])
            embed = nextcord.Embed(description=f"Date: **{DateFormating(content_to_update['content_date'])}**\nTime: **{time_utc} (UTC) | {time_msk} (МСК)**", colour=0xe3eed8)
            embed.set_author(name=content_to_update["content_title"])

            if content_to_update["party_2"]["21"] == "":
                party_1_string = ""  
                for i in range(len(content_to_update["party_1"])):
                    if content_to_update["party_1"][str(i+1)] != "" and content_to_update["members"][str(i+1)] == "":
                        party_1_string = party_1_string + f"🟨 {str(i+1)}. {content_to_update['party_1'][str(i+1)]}\n"
                    elif content_to_update["party_1"][str(i+1)] != "" and content_to_update["members"][str(i+1)] != "":
                        party_1_string = party_1_string + f"✅ {str(i+1)}. {content_to_update['party_1'][str(i+1)]} - <@{content_to_update['members'][str(i+1)]}>\n"
                embed.add_field(name="⚔️ Party 1", value=party_1_string, inline=True)
            elif content_to_update["party_2"]["21"] != "":
                party_1_string = ""  
                for i in range(len(content_to_update["party_1"])):
                    if content_to_update["party_1"][str(i+1)] != "" and content_to_update["members"][str(i+1)] == "":
                        party_1_string = party_1_string + f"🟨 {str(i+1)}. {content_to_update['party_1'][str(i+1)]}\n"
                    elif content_to_update["party_1"][str(i+1)] != "" and content_to_update["members"][str(i+1)] != "":
                        party_1_string = party_1_string + f"✅ {str(i+1)}. {content_to_update['party_1'][str(i+1)]} - <@{content_to_update['members'][str(i+1)]}>\n"
                embed.add_field(name="⚔️ Party 1", value=party_1_string, inline=True)
                party_2_string = ""  
                for i in range(20,len(content_to_update["party_2"])+20):
                    if content_to_update["party_2"][str(i+1)] != "" and content_to_update["members"][str(i+1)] == "":
                        party_2_string = party_2_string + f"🟨 {str(i+1)}. {content_to_update['party_2'][str(i+1)]}\n"
                    elif content_to_update["party_2"][str(i+1)] != "" and content_to_update["members"][str(i+1)] != "":
                        party_2_string = party_2_string + f"✅ {str(i+1)}. {content_to_update['party_2'][str(i+1)]} - <@{content_to_update['members'][str(i+1)]}>\n"
                embed.add_field(name="⚔️ Party 2", value=party_2_string, inline=True)

            embed.set_footer(text=f"content_id: {content_to_update['content_id']}")

            message = await interaction.channel.fetch_message(message_id)
            await message.edit(embed=embed, allowed_mentions=allowed_mentions)
            await interaction.response.send_message(content="Success", ephemeral=True, delete_after=.5)
                                    
            contents_list.close()
        else:
            await interaction.response.send_message(content="You're not content creator!", ephemeral=True, delete_after=3)

    @nextcord.slash_command(name="changetime", description="Change time in content by content_id", guild_ids=[serverId])
    async def changetime(
            self,
            interaction:Interaction,
            content_id:str = nextcord.SlashOption(description="Content ID"),
            new_time:str = nextcord.SlashOption(description="New content time"),
        ):

        content_to_update = {}
        message_id = None
        content_leader_id = None

        with open(data_file_path, "r") as contents_list:
            contents_list_data = json.load(contents_list)
            for data in contents_list_data:
                if data["content_id"] == content_id:
                    content_leader_id = data["content_leader_id"]
                    break
        contents_list.close()
        
        if content_leader_id == interaction.user.id:
            UpdateContent(content_id, "content_time", new_time)

            with open(data_file_path, "r") as contents_list:
                contents_list_data = json.load(contents_list)
                for data in contents_list_data:
                    if data["content_id"] == content_id:
                        content_to_update = data
                        message_id = data["content_message_id"]
                        break

            time_utc, time_msk = TimeFormating(content_to_update["content_time"])
            embed = nextcord.Embed(description=f"Date: **{DateFormating(content_to_update['content_date'])}**\nTime: **{time_utc} (UTC) | {time_msk} (МСК)**", colour=0xe3eed8)
            embed.set_author(name=content_to_update["content_title"])

            if content_to_update["party_2"]["21"] == "":
                party_1_string = ""  
                for i in range(len(content_to_update["party_1"])):
                    if content_to_update["party_1"][str(i+1)] != "" and content_to_update["members"][str(i+1)] == "":
                        party_1_string = party_1_string + f"🟨 {str(i+1)}. {content_to_update['party_1'][str(i+1)]}\n"
                    elif content_to_update["party_1"][str(i+1)] != "" and content_to_update["members"][str(i+1)] != "":
                        party_1_string = party_1_string + f"✅ {str(i+1)}. {content_to_update['party_1'][str(i+1)]} - <@{content_to_update['members'][str(i+1)]}>\n"
                embed.add_field(name="⚔️ Party 1", value=party_1_string, inline=True)
            elif content_to_update["party_2"]["21"] != "":
                party_1_string = ""  
                for i in range(len(content_to_update["party_1"])):
                    if content_to_update["party_1"][str(i+1)] != "" and content_to_update["members"][str(i+1)] == "":
                        party_1_string = party_1_string + f"🟨 {str(i+1)}. {content_to_update['party_1'][str(i+1)]}\n"
                    elif content_to_update["party_1"][str(i+1)] != "" and content_to_update["members"][str(i+1)] != "":
                        party_1_string = party_1_string + f"✅ {str(i+1)}. {content_to_update['party_1'][str(i+1)]} - <@{content_to_update['members'][str(i+1)]}>\n"
                embed.add_field(name="⚔️ Party 1", value=party_1_string, inline=True)
                party_2_string = ""  
                for i in range(20,len(content_to_update["party_2"])+20):
                    if content_to_update["party_2"][str(i+1)] != "" and content_to_update["members"][str(i+1)] == "":
                        party_2_string = party_2_string + f"🟨 {str(i+1)}. {content_to_update['party_2'][str(i+1)]}\n"
                    elif content_to_update["party_2"][str(i+1)] != "" and content_to_update["members"][str(i+1)] != "":
                        party_2_string = party_2_string + f"✅ {str(i+1)}. {content_to_update['party_2'][str(i+1)]} - <@{content_to_update['members'][str(i+1)]}>\n"
                embed.add_field(name="⚔️ Party 2", value=party_2_string, inline=True)

            embed.set_footer(text=f"content_id: {content_to_update['content_id']}")

            message = await interaction.channel.fetch_message(message_id)
            await message.edit(embed=embed, allowed_mentions=allowed_mentions)
            await interaction.response.send_message(content="Success", ephemeral=True, delete_after=.5)
                                    
            contents_list.close()
        else:
            await interaction.response.send_message(content="You're not content creator!", ephemeral=True, delete_after=3)


def setup(client):
    threading.Thread(target=StartClearData).start()
    client.add_cog(Content(client))
