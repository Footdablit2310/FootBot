import { ChatInputCommandInteraction } from "discord.js";
import fs from "fs";
import { getGuildData, setGuildData } from "../utils/guildData";
import { ValueIsNullError } from "../utils/nullError";

export async function execute(interaction:ChatInputCommandInteraction) {
  const guildId = interaction.guildId;
  const key = interaction.options.getString("key", true);
  const value = interaction.options.getString("value", true);
  if(guildId == null){
    throw new ValueIsNullError()
  }
  const guildData = getGuildData(guildId);
  guildData.config![key] = value;

  setGuildData(guildId, guildData);
  await interaction.reply(`⚙️ Config '${key}' set to '${value}' for this guild.`);
}
