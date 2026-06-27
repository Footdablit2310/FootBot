import { ChatInputCommandInteraction } from "discord.js";
import fs from "fs";

export async function croster(interaction: ChatInputCommandInteraction) {
  const rostersFile = "./data/rosters.json";
  const rostersData = JSON.parse(fs.readFileSync(rostersFile, "utf8"));

  const newRoster = {
    id: Date.now().toString(),
    name: `Roster-${Date.now()}`,
    members: {},
    roles: {},
    locFallbackRole: null
  };

  rostersData.rosters.push(newRoster);
  fs.writeFileSync(rostersFile, JSON.stringify(rostersData, null, 2));

  await interaction.reply({ content: `✅ Created roster **${newRoster.name}**`, ephemeral: true });
}
