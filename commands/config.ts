import {
  SlashCommandBuilder,
  ChatInputCommandInteraction,
  EmbedBuilder,
  ActionRowBuilder,
  StringSelectMenuBuilder
} from "discord.js";
import { getGuildData } from "../utils/guildData";

export const data = new SlashCommandBuilder()
  .setName("config")
  .setDescription("View and update bot config");

export async function execute(interaction: ChatInputCommandInteraction) {
  const guildData = getGuildData(interaction.guildId!);

  const embed = new EmbedBuilder()
    .setTitle("⚙️ Bot Configuration")
    .setDescription("Current settings")
    .addFields(
      { name: "Ping Minutes Before Event", value: guildData.config?.pingMinutesBefore?.toString() ?? "15", inline: true },
      { name: "Admin Role ID", value: guildData.config?.adminRoleId ?? "Not set", inline: true },
      { name: "Event Channel ID", value: guildData.config?.eventChannelId ?? "Not set", inline: true }
    )
    .setColor(0x3498db);

  const selectMenu = new StringSelectMenuBuilder()
    .setCustomId("config_select")
    .setPlaceholder("Choose a config key to edit")
    .addOptions([
      { label: "Ping Minutes Before Event", value: "pingMinutesBefore" },
      { label: "Admin Role ID", value: "adminRoleId" },
      { label: "Event Channel ID", value: "eventChannelId" }
    ]);

  const row = new ActionRowBuilder<StringSelectMenuBuilder>().addComponents(selectMenu);

  await interaction.reply({ embeds: [embed], components: [row] });
}
