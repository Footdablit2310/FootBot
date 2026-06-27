import {
  Client,
  GatewayIntentBits,
  Interaction,
  StringSelectMenuInteraction,
  ModalBuilder,
  TextInputBuilder,
  TextInputStyle,
  ActionRowBuilder
} from "discord.js";
import fs from "fs";
import path from "path";
import dotenv from "dotenv";
import { getGuildData, updateGuildData, setConfigValue, ConfigKey } from "./utils/guildData";
import { startScheduler } from "./scheduler";

dotenv.config();

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

// Load command files
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
  // Slash commands
  if (interaction.isChatInputCommand()) {
    const command = commands.get(interaction.commandName);
    if (command) await command.execute(interaction);
  }

  // Select menus
  if (interaction.isStringSelectMenu()) {
    const [action, id] = interaction.values[0].split("_");

    if (interaction.customId === "roster_select") {
      switch (action) {
        case "view": {
          const roster = getGuildData(interaction.guildId!).rosters?.[id];
          await interaction.reply(roster ? `📋 Roster: ${roster.name}` : `❌ Roster not found`);
          break;
        }
        case "edit": {
          const modal = new ModalBuilder()
            .setCustomId(`edit_roster_${id}`)
            .setTitle("Edit Roster");

          const nameInput = new TextInputBuilder()
            .setCustomId("newName")
            .setLabel("New roster name")
            .setStyle(TextInputStyle.Short)
            .setRequired(true);

          const row = new ActionRowBuilder<TextInputBuilder>().addComponents(nameInput);
          modal.addComponents(row);

          await interaction.showModal(modal);
          break;
        }
        case "delete":
          updateGuildData(interaction.guildId!, data => { delete data.rosters![id]; });
          await interaction.reply(`🗑️ Roster ${id} deleted.`);
          break;
      }
    }

    if (interaction.customId === "event_select") {
      switch (action) {
        case "view": {
          const event = getGuildData(interaction.guildId!).events?.[id];
          await interaction.reply(event ? `📅 Event: ${event.title} at <t:${event.dateUnix}:F>` : `❌ Event not found`);
          break;
        }
        case "edit": {
          const modal = new ModalBuilder()
            .setCustomId(`edit_event_${id}`)
            .setTitle("Edit Event");

          const titleInput = new TextInputBuilder()
            .setCustomId("newTitle")
            .setLabel("New event title")
            .setStyle(TextInputStyle.Short)
            .setRequired(true);

          const timeInput = new TextInputBuilder()
            .setCustomId("newTime")
            .setLabel("New time (YYYY-MM-DD HH:mm)")
            .setStyle(TextInputStyle.Short)
            .setRequired(false);

          const row1 = new ActionRowBuilder<TextInputBuilder>().addComponents(titleInput);
          const row2 = new ActionRowBuilder<TextInputBuilder>().addComponents(timeInput);
          modal.addComponents(row1, row2);

          await interaction.showModal(modal);
          break;
        }
        case "delete":
          updateGuildData(interaction.guildId!, data => { delete data.events![id]; });
          await interaction.reply(`🗑️ Event ${id} deleted.`);
          break;
        case "ping": {
          const guildData = getGuildData(interaction.guildId!);
          const event = guildData.events?.[id];
          if (event && event.rosterId) {
            const roster = guildData.rosters?.[event.rosterId];
            if (roster?.roleId) {
              await interaction.reply(`🔔 Pinging <@&${roster.roleId}> ${guildData.config?.pingMinutesBefore ?? 15} minutes before <t:${event.dateUnix}:F>.`);
            } else {
              await interaction.reply("❌ No role assigned to roster.");
            }
          } else {
            await interaction.reply("❌ Event has no roster assigned.");
          }
          break;
        }
      }
    }

    if (interaction.customId === "config_select") {
      const key = action; // e.g. pingMinutesBefore
      const modal = new ModalBuilder()
        .setCustomId(`edit_config_${key}`)
        .setTitle(`Edit Config: ${key}`);

      const valueInput = new TextInputBuilder()
        .setCustomId("newValue")
        .setLabel(`New value for ${key}`)
        .setStyle(TextInputStyle.Short)
        .setRequired(true);

      const row = new ActionRowBuilder<TextInputBuilder>().addComponents(valueInput);
      modal.addComponents(row);

      await interaction.showModal(modal);
    }
  }

  // Modal submissions
  if (interaction.isModalSubmit()) {
    const [action, type, idOrKey] = interaction.customId.split("_");

    if (action === "edit" && type === "config") {
      const key = idOrKey as ConfigKey;
      const newValue = interaction.fields.getTextInputValue("newValue");
      setConfigValue(interaction.guildId!, key, newValue)
      await interaction.reply(`⚙️ Config **${key}** updated to **${newValue}**.`);
    }
  }
});


client.login(process.env.DISCORD_TOKEN);

client.once("ready", () => {
  console.log(`✅ Logged in as ${client.user?.tag}`);
  startScheduler(client);
});
