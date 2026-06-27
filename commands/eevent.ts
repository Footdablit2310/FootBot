import { ChatInputCommandInteraction } from "discord.js";
import fs from "fs";
import { getGuildData, setGuildData } from "../utils/guildData";
import { ValueIsNullError } from "../utils/nullError";

export async function execute(interaction:ChatInputCommandInteraction) {
  const guildId = interaction.guildId;
  const eventName = interaction.options.getString("name", true);
  const newDate = interaction.options.getString("date");
  if(guildId == null){
    throw new ValueIsNullError()
  }

  const guildData = getGuildData(guildId);
  if (!guildData.events![eventName]) {
    return interaction.reply(`Event '${eventName}' not found.`);
  }
  

  guildData.events![eventName].date = newDate;
  setGuildData(guildId, guildData);

  await interaction.reply(`✏️ Event '${eventName}' updated for this guild.`);
}
