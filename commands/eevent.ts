import { ChatInputCommandInteraction } from "discord.js";
import fs from "fs";

export async function eevent(interaction: ChatInputCommandInteraction) {
  const eventsFile = "./data/events.json";
  const eventsData = JSON.parse(fs.readFileSync(eventsFile, "utf8"));

  const eventId = interaction.options.getString("id", true);
  const newTitle = interaction.options.getString("title", true);

  const event = eventsData.events.find((e: any) => e.id === eventId);
  if (!event) {
    await interaction.reply({ content: `❌ Event not found`, ephemeral: true });
    return;
  }

  event.title = newTitle;
  fs.writeFileSync(eventsFile, JSON.stringify(eventsData, null, 2));

  await interaction.reply({ content: `✏️ Renamed event to **${newTitle}**`, ephemeral: true });
}
