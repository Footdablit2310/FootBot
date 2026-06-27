import { ChatInputCommandInteraction } from "discord.js";
import fs from "fs";

export async function droster(interaction: ChatInputCommandInteraction) {
  const rostersFile = "./data/rosters.json";
  const rostersData = JSON.parse(fs.readFileSync(rostersFile, "utf8"));

  const rosterId = interaction.options.getString("id", true);
  const index = rostersData.rosters.findIndex((r: any) => r.id === rosterId);

  if (index === -1) {
    await interaction.reply({ content: `❌ Roster not found`, ephemeral: true });
    return;
  }

  const removed = rostersData.rosters.splice(index, 1)[0];
  fs.writeFileSync(rostersFile, JSON.stringify(rostersData, null, 2));

  await interaction.reply({ content: `🗑️ Deleted roster **${removed.name}**`, ephemeral: true });
}
