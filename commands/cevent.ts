import { ChatInputCommandInteraction } from "discord.js";
import fs from "fs";

export async function cevent(interaction: ChatInputCommandInteraction) {
  const eventsFile = "./data/events.json";
  const eventsData = JSON.parse(fs.readFileSync(eventsFile, "utf8"));

  const newEvent = {
    id: Date.now().toString(),
    title: interaction.options.getString("title", true),
    dateUnix: Math.floor(Date.now() / 1000),
    rosterId: null,
    createdBy: interaction.user.id,
    linkedDiscordEventId: null
  };

  eventsData.events.push(newEvent);
  fs.writeFileSync(eventsFile, JSON.stringify(eventsData, null, 2));

  await interaction.reply({ content: `📅 Created event **${newEvent.title}**`, ephemeral: true });
}
