import {
  SlashCommandBuilder,
  ChatInputCommandInteraction,
  ActionRowBuilder,
  StringSelectMenuBuilder,
  EmbedBuilder
} from "discord.js";
import fs from "fs";

export const data = new SlashCommandBuilder()
  .setName("view")
  .setDescription("View an event or roster");

export async function execute(interaction: ChatInputCommandInteraction) {
  // First select menu: choose type
  const typeMenu = new StringSelectMenuBuilder()
    .setCustomId("viewType")
    .setPlaceholder("Choose what to view")
    .addOptions(
      { label: "Event", value: "event" },
      { label: "Roster", value: "roster" }
    );

  const row = new ActionRowBuilder<StringSelectMenuBuilder>().addComponents(typeMenu);

  await interaction.reply({
    content: "Select whether you want to view an event or a roster:",
    components: [row],
    ephemeral: true
  });
}
