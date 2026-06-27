import { SlashCommandBuilder, EmbedBuilder, ChatInputCommandInteraction } from "discord.js";
import { getGuildData } from "../utils/guildData";
import { ValueIsNullError } from "../utils/nullError";

export const data = new SlashCommandBuilder()
  .setName("view")
  .setDescription("View rosters or events")
  .addStringOption(opt =>
    opt.setName("type")
      .setDescription("Choose what to view")
      .setRequired(true)
      .addChoices(
        { name: "roster", value: "roster" },
        { name: "event", value: "event" },
        { name: "all", value: "all" }
      )
  )
  .addStringOption(opt =>
    opt.setName("name")
      .setDescription("Name of roster/event (optional)")
      .setRequired(false)
  );

export async function execute(interaction:ChatInputCommandInteraction) {
  const guildId = interaction.guildId;
  const type = interaction.options.getString("type", true);
  const name = interaction.options.getString("name");
  if (guildId==null) {
    throw new ValueIsNullError()
  }
  
  const guildData = getGuildData(guildId);

  let embed = new EmbedBuilder().setColor(0x00AE86);

  if (type === "roster") {
    if (name) {
      const roster = guildData.rosters?.[name];
      if (!roster) return interaction.reply({ content: `Roster '${name}' not found.`, ephemeral: true });

      embed.setTitle(`Roster: ${name}`).setDescription(JSON.stringify(roster, null, 2));
    } else {
      embed.setTitle("All Rosters").setDescription(Object.keys(guildData.rosters || {}).join(", ") || "None");
    }
  }

  else if (type === "event") {
    if (name) {
      const event = guildData.events?.[name];
      if (!event) return interaction.reply({ content: `Event '${name}' not found.`, ephemeral: true });

      embed.setTitle(`Event: ${name}`).setDescription(JSON.stringify(event, null, 2));
    } else {
      embed.setTitle("All Events").setDescription(Object.keys(guildData.events || {}).join(", ") || "None");
    }
  }

  else if (type === "all") {
    embed.setTitle("Guild Data Overview")
      .addFields(
        { name: "Rosters", value: Object.keys(guildData.rosters || {}).join(", ") || "None", inline: true },
        { name: "Events", value: Object.keys(guildData.events || {}).join(", ") || "None", inline: true }
      );
  }

  await interaction.reply({ embeds: [embed], ephemeral: false });
}
