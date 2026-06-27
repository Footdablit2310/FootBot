import { ChatInputCommandInteraction } from "discord.js";
import fs from "fs";

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
