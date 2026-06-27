import { SlashCommandBuilder, ChatInputCommandInteraction, EmbedBuilder } from "discord.js";
import { getGuildData } from "../utils/guildData";

export const data = new SlashCommandBuilder()
  .setName("view")
  .setDescription("View roster or event")
  .addStringOption(opt =>
    opt.setName("id").setDescription("Roster/Event ID").setRequired(true)
  );

export async function execute(interaction: ChatInputCommandInteraction) {
  const id = interaction.options.getString("id", true);
  const guildData = getGuildData(interaction.guildId!);

  const roster = guildData.rosters?.[id];
  const event = guildData.events?.[id];

  if (roster) {
    const embed = new EmbedBuilder()
      .setTitle(`📋 Roster: ${roster.name}`)
      .addFields(
        { name: "ID", value: roster.id },
        { name: "Role", value: roster.roleId ? `<@&${roster.roleId}>` : "None" },
        { name: "Created By", value: `<@${roster.createdBy}>` }
      );
    await interaction.reply({ embeds: [embed] });
    return;
  }

  if (event) {
    const embed = new EmbedBuilder()
      .setTitle(`📅 Event: ${event.title}`)
      .addFields(
        { name: "ID", value: event.id },
        { name: "Time", value: `<t:${event.dateUnix}:F>` },
        { name: "Roster", value: event.rosterId ?? "None" },
        { name: "Created By", value: `<@${event.createdBy}>` }
      );
    await interaction.reply({ embeds: [embed] });
    return;
  }

  await interaction.reply(`❌ No roster or event found with ID **${id}**.`);
}
