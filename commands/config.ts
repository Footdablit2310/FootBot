import { ChatInputCommandInteraction } from "discord.js";
import fs from "fs";

export async function config(interaction: ChatInputCommandInteraction) {
  const configFile = "./data/config.json";
  const configData = JSON.parse(fs.readFileSync(configFile, "utf8"));

  const key = interaction.options.getString("key", true);
  const value = interaction.options.getString("value", true);

  configData[key] = value;
  fs.writeFileSync(configFile, JSON.stringify(configData, null, 2));

  await interaction.reply({ content: `⚙️ Updated config: ${key} = ${value}`, ephemeral: true });
}
