import { StringSelectMenuInteraction, EmbedBuilder } from "discord.js";
import fs from "fs";

export async function handleViewEvent(interaction: StringSelectMenuInteraction) {
  const events = JSON.parse(fs.readFileSync("./data/events.json", "utf8")).events;
  const choice = interaction.values[0];

  if (choice === "allEvents") {
    const embed = new EmbedBuilder()
      .setColor(0x3498db)
      .setTitle("📅 All Events")
      .addFields(events.map((e: any) => ({
        name: e.title,
        value: `Date: <t:${e.dateUnix}:F>\nRoster: ${e.rosterId}\nCreated By: <@${e.createdBy}>`,
        inline: false
      })));
    await interaction.reply({ embeds: [embed] });
    return;
  }

  const event = events.find((e: any) => e.id === choice);
  if (!event) return interaction.reply({ content: "Event not found.", ephemeral: true });

  const embed = new EmbedBuilder()
    .setColor(0x3498db)
    .setTitle(`📅 Event: ${event.title}`)
    .addFields(
      { name: "Date", value: `<t:${event.dateUnix}:F>`, inline: true },
      { name: "Roster", value: event.rosterId || "None", inline: true },
      { name: "Created By", value: `<@${event.createdBy}>`, inline: true },
      { name: "Discord Event", value: event.linkedDiscordEventId ? "Linked" : "Not linked", inline: true }
    );

  await interaction.reply({ embeds: [embed] });
}
