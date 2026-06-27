import { ChatInputCommandInteraction } from "discord.js";
import fs from "fs";

export async function eroster(interaction: ChatInputCommandInteraction) {
  const rostersFile = "./data/rosters.json";
  const rostersData = JSON.parse(fs.readFileSync(rostersFile, "utf8"));

  const rosterId = interaction.options.getString("id", true);
  const newName = interaction.options.getString("name", true);

  const roster = rostersData.rosters.find((r: any) => r.id === rosterId);
  if (!roster) {
    await interaction.reply({ content: `❌ Roster not found`, ephemeral: true });
    return;
  }

  roster.name = newName;
  fs.writeFileSync(rostersFile, JSON.stringify(rostersData, null, 2));

  await interaction.reply({ content: `✏️ Renamed roster to **${newName}**`, ephemeral: true });
}
