import { ChatInputCommandInteraction } from "discord.js";
import fs from "fs";
import { getGuildData, setGuildData } from "../utils/guildData";
import { ValueIsNullError } from "../utils/nullError";

export async function execute(interaction:ChatInputCommandInteraction) {
  const guildId = interaction.guildId;
  const eventName = interaction.options.getString("name", true);
  if (guildId==null) {
    throw new ValueIsNullError()
  }

  const guildData = getGuildData(guildId);
  guildData.events![eventName] = { createdAt: Date.now() };

  setGuildData(guildId, guildData);
  await interaction.reply(`📅 Event '${eventName}' created for this guild.`);
}
