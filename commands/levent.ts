import { ChatInputCommandInteraction } from "discord.js";
import fs from "fs";
import { getGuildData, setGuildData } from "../utils/guildData";
import { ValueIsNullError } from "../utils/nullError";

export async function execute(interaction:ChatInputCommandInteraction) {
  const guildId = interaction.guildId;
  const eventName = interaction.options.getString("name", true);
  const discordEventId = interaction.options.getString("discord_event_id", true);4
  if(guildId == null){
    throw new ValueIsNullError()
  }

  const guildData = getGuildData(guildId);
  if (!guildData.events![eventName]) {
    return interaction.reply(`Event '${eventName}' not found.`);
  }

  guildData.events![eventName].linkedDiscordEventId = discordEventId;
  setGuildData(guildId, guildData);

  await interaction.reply(`🔗 Event '${eventName}' linked to Discord event ${discordEventId}.`);
}
