import { ChatInputCommandInteraction } from "discord.js";
import fs from "fs";
import { getGuildData, setGuildData } from "../utils/guildData";
import { ValueIsNullError } from "../utils/nullError";

export async function execute(interaction:ChatInputCommandInteraction) {
  const guildId = interaction.guildId;
  const rosterName = interaction.options.getString("name", true);
  if(guildId == null){
    throw new ValueIsNullError()
  }

  const guildData = getGuildData(guildId);
  delete guildData.rosters![rosterName];

  setGuildData(guildId, guildData);
  await interaction.reply(`🗑️ Roster '${rosterName}' deleted for this guild.`);
}
