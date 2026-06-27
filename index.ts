// src/index.ts
import { Client, GatewayIntentBits, Interaction, StringSelectMenuInteraction } from "discord.js";
import fs from "fs";
import path from "path";
import dotenv from "dotenv";

dotenv.config();

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

const commands = new Map<string, any>();
const commandsPath = path.join(__dirname, "commands");
const files = fs.readdirSync(commandsPath).filter(f => f.endsWith(".ts") || f.endsWith(".js"));

for (const file of files) {
  const cmd = require(path.join(commandsPath, file));
  if ("data" in cmd && "execute" in cmd) {
    commands.set(cmd.data.name, cmd);
  }
}

client.on("interactionCreate", async (interaction: Interaction) => {
  if (interaction.isChatInputCommand()) {
    const command = commands.get(interaction.commandName);
    if (command) await command.execute(interaction);
  }

  if (interaction.isStringSelectMenu()) {
    const [action, id] = interaction.values[0].split("_");
    switch (action) {
      case "view":
        await interaction.reply(`👀 Viewing event/roster ${id}`);
        break;
      case "edit":
        await interaction.reply(`✏️ Editing ${id}`);
        break;
      case "delete":
        await interaction.reply(`🗑️ Deleted ${id}`);
        break;
      case "ping":
        await interaction.reply(`🔔 Pinging roster for event ${id}`);
        break;
      default:
        await interaction.reply("❌ Unknown action");
    }
  }
});

client.login(process.env.DISCORD_TOKEN);
