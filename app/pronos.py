# Gestion des pronostiques, écriture et lecture
import json
import os
import discord
from config import logger


def pronos(id: int, pseudo: str, premier: str, second: str, troisieme: str, bt: str):
    file_path = 'data/Pronos.json'
    if not os.path.exists(file_path):
        pronos_database = {
            str(id): {
                "Pseudo": pseudo,
                "1": premier,
                "2": second,
                "3": troisieme,
                "Best Lap": bt,
                "Modif":False
            }
        }
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            pronos_database = json.load(f)
            if str(id) not in pronos_database:
                pronos_database[str(id)] = {
                    "Pseudo": pseudo,
                    "1": premier,
                    "2": second,
                    "3": troisieme,
                    "Best Lap": bt,
                    "Modif":False
                }
            else:
                if(pronos_database[str(id)]["Modif"] == True):
                    return False
                else:

                    pronos_database[str(id)]["Pseudo"] = pseudo
                    pronos_database[str(id)]["1"] = premier
                    pronos_database[str(id)]["2"] = second
                    pronos_database[str(id)]["3"] = troisieme
                    pronos_database[str(id)]["Best Lap"] = bt
                    pronos_database[str(id)]["Modif"] = True


    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(pronos_database, f, ensure_ascii=False, indent=4)
    return True
async def visualisation(interaction: discord.Interaction):
    
    file_path = "data/Pronos.json"
    with open(file_path, 'r', encoding='utf-8') as f:
            pronos_database = json.load(f)
    
    user = interaction.user.id 
    
    if str(user) in pronos_database:
        premier=pronos_database[str(user)]["1"]
        deuxieme=pronos_database[str(user)]["2"]
        troisieme=pronos_database[str(user)]["3"]
        best_lap=pronos_database[str(user)]["Best Lap"]
        modif=pronos_database[str(user)]["Modif"]
    
        embed = discord.Embed(
            title = f"🐐 Merci pour vos pronos {interaction.user} !",
            description="Voici tes pronostiques : ",
            color=discord.Color.red()
        )
        
        embed.add_field(name="Ton Premier 🥇 :", value=f"{premier}", inline=False)
        embed.add_field(name="Ton Deuxième 🥈 :", value=f"{deuxieme}", inline=False)
        embed.add_field(name="Ton Troisième 🥉 :", value=f"{troisieme}", inline=False)
        embed.add_field(name="Ton Meilleur Tour ⏱️ :", value=f"{best_lap}", inline=False) 
        if(modif):
            value="❌ Tu as déja modifié ton pronostic par le passé"
        else:
            value="✅ Tu peux modifier ton pronostic en relançant /pronos_course" 
        embed.add_field(name="Droit de modification :",value=value,inline=False) 
       

        embed.set_footer(text="Bot créé par F1F Team", icon_url="https://cdn.discordapp.com/attachments/1339299411360088226/1367477935392428083/Votre_texte_de_paragraphe_12.png")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1339299411360088226/1368544420504272987/Design_sans_titre_2.png")
        

        logger.info(f"{interaction.user.name} a regarder ses pronos course")
        
        await interaction.followup.send(embed=embed, ephemeral=True)  
        
        
        
    else:
        embed = discord.Embed(
            title = f"Désolé {interaction.user} !",
            description="On dirait que tu n'as pas encore fait de pronostique",
            color=discord.Color.red()
        )
        
        embed.set_footer(text="Bot créé par F1F Team", icon_url="https://cdn.discordapp.com/attachments/1339299411360088226/1367477935392428083/Votre_texte_de_paragraphe_12.png")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1339299411360088226/1368544420504272987/Design_sans_titre_2.png")
        logger.info(f"{interaction.user.name} a tenter de regarder ses pronos course alors qu'il n'en avais pas fais")
        await interaction.followup.send(embed=embed, ephemeral=True)
        
        
    

    

    
