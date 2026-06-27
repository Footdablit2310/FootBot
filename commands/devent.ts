import { ChatInputCommandInteraction } from "discord.js";
import fs from "fs";
import { getGuildData, setGuildData } from "../utils/guildData";
import { ValueIsNullError } from "../utils/nullError";

export async function devent(interaction: ChatInputCommandInteraction) {
  const eventsFile = "./data/events.json";
  const eventsData = JSON.parse(fs.readFileSync(eventsFile, "utf8"));

  const eventId = interaction.options.getString("id", true);
  const index = eventsData.events.findIndex((e: any) => e.id === eventId);

  if (index === -1) {
    await interaction.reply({ content: `❌ Event not found`, ephemeral: true });
    return;
  }

  const removed = eventsData.events.splice(index, 1)[0];
  fs.writeFileSync(eventsFile, JSON.stringify(eventsData, null, 2));

  await interaction.reply({ content: `🗑️ Deleted event **${removed.title}**`, ephemeral: true });
}
export async function execute(interaction:ChatInputCommandInteraction) {
  const guildId = interaction.guildId;
  const eventName = interaction.options.getString("name", true);
  if(guildId == null){
    throw new ValueIsNullError()
  }

  const guildData = getGuildData(guildId);
  delete guildData.events![eventName];

  setGuildData(guildId, guildData);
  await interaction.reply(`🗑️ Event '${eventName}' deleted for this guild.`);
}
