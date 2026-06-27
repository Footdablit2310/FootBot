import { ChatInputCommandInteraction } from "discord.js";
import fs from "fs";
import { getGuildData, setGuildData } from "../utils/guildData";
import { ValueIsNullError } from "../utils/nullError";

export async function execute(interaction:ChatInputCommandInteraction) {
  const guildId = interaction.guildId;
  const rosterName = interaction.options.getString("name", true);
  const newCaptain = interaction.options.getString("captain");
  if(guildId == null){
    throw new ValueIsNullError()
  }

  const guildData = getGuildData(guildId);
  if (!guildData.rosters![rosterName]) {
    return interaction.reply(`Roster '${rosterName}' not found.`);
  }

  guildData.rosters![rosterName].Captain = newCaptain;
  setGuildData(guildId, guildData);

  await interaction.reply(`✏️ Roster '${rosterName}' updated for this guild.`);
}
