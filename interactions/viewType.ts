import {
  StringSelectMenuInteraction,
  ActionRowBuilder,
  StringSelectMenuBuilder
} from "discord.js";
import fs from "fs";

export async function handleViewType(interaction: StringSelectMenuInteraction) {
  const type = interaction.values[0];

  if (type === "event") {
    const events = JSON.parse(fs.readFileSync("./data/events.json", "utf8")).events;
    const options = events.map((e: any) => ({
      label: e.title,
      description: `Created by <@${e.createdBy}>`,
      value: e.id
    }));
    options.push({ label: "All Events", value: "allEvents" });

    const menu = new StringSelectMenuBuilder()
      .setCustomId("viewEvent")
      .setPlaceholder("Choose an event")
      .addOptions(options);

    const row = new ActionRowBuilder<StringSelectMenuBuilder>().addComponents(menu);
    await interaction.reply({ content: "Select an event:", components: [row], ephemeral: true });
  }

  if (type === "roster") {
    const rosters = JSON.parse(fs.readFileSync("./data/rosters.json", "utf8")).rosters;
    const options = rosters.map((r: any) => ({
      label: r.name,
      description: `Roster ID: ${r.id}`,
      value: r.id
    }));
    options.push({ label: "All Rosters", value: "allRosters" });

    const menu = new StringSelectMenuBuilder()
      .setCustomId("viewRoster")
      .setPlaceholder("Choose a roster")
      .addOptions(options);

    const row = new ActionRowBuilder<StringSelectMenuBuilder>().addComponents(menu);
    await interaction.reply({ content: "Select a roster:", components: [row], ephemeral: true });
  }
}
