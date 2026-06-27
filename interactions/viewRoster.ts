import { StringSelectMenuInteraction, EmbedBuilder } from "discord.js";
import fs from "fs";

export async function handleViewRoster(interaction: StringSelectMenuInteraction) {
  const rosters = JSON.parse(fs.readFileSync("./data/rosters.json", "utf8")).rosters;
  const choice = interaction.values[0];

  if (choice === "allRosters") {
    const embed = new EmbedBuilder()
      .setColor(0x2ecc71)
      .setTitle("👥 All Rosters")
      .addFields(rosters.map((r: any) => ({
        name: r.name,
        value: `Members: ${Object.entries(r.members).map(([pos, uid]) => `**${pos}:** <@${uid}>`).join(", ")}`,
        inline: false
      })));
    await interaction.reply({ embeds: [embed] });
    return;
  }

  const roster = rosters.find((r: any) => r.id === choice);
  if (!roster) return interaction.reply({ content: "Roster not found.", ephemeral: true });

  const embed = new EmbedBuilder()
    .setColor(0x2ecc71)
    .setTitle(`👥 Roster: ${roster.name}`)
    .addFields(
      { name: "Members", value: Object.entries(roster.members).map(([pos, uid]) => `**${pos}:** <@${uid}>`).join("\n") || "None" },
      { name: "Roles", value: Object.entries(roster.roles).map(([pos, rid]) => `**${pos}:** <@&${rid}>`).join("\n") || "None" },
      { name: "Fallback Role", value: roster.locFallbackRole ? `<@&${roster.locFallbackRole}>` : "None" }
    );

  await interaction.reply({ embeds: [embed] });
}
