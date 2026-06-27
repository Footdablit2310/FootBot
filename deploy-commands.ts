import { REST, Routes, SlashCommandBuilder } from "discord.js";
import dotenv from "dotenv";

dotenv.config();

const commands = [
  new SlashCommandBuilder()
    .setName("croster")
    .setDescription("Create a roster")
    .addStringOption(opt =>
      opt.setName("name")
        .setDescription("Name of the roster")
        .setRequired(true)
    ),

  new SlashCommandBuilder()
    .setName("droster")
    .setDescription("Delete a roster")
    .addStringOption(opt =>
      opt.setName("id")
        .setDescription("Roster ID to delete")
        .setRequired(true)
    ),

  new SlashCommandBuilder()
    .setName("eroster")
    .setDescription("Edit a roster")
    .addStringOption(opt =>
      opt.setName("id")
        .setDescription("Roster ID to edit")
        .setRequired(true)
    )
    .addStringOption(opt =>
      opt.setName("name")
        .setDescription("New name for the roster")
        .setRequired(true)
    ),

  new SlashCommandBuilder()
    .setName("config")
    .setDescription("Update bot config")
    .addStringOption(opt =>
      opt.setName("key")
        .setDescription("Config key")
        .setRequired(true)
    )
    .addStringOption(opt =>
      opt.setName("value")
        .setDescription("Config value")
        .setRequired(true)
    ),

  new SlashCommandBuilder()
    .setName("cevent")
    .setDescription("Create an event")
    .addStringOption(opt =>
      opt.setName("title")
        .setDescription("Title of the event")
        .setRequired(true)
    ),

  new SlashCommandBuilder()
    .setName("devent")
    .setDescription("Delete an event")
    .addStringOption(opt =>
      opt.setName("id")
        .setDescription("Event ID to delete")
        .setRequired(true)
    ),

  new SlashCommandBuilder()
    .setName("eevent")
    .setDescription("Edit an event")
    .addStringOption(opt =>
      opt.setName("id")
        .setDescription("Event ID to edit")
        .setRequired(true)
    )
    .addStringOption(opt =>
      opt.setName("title")
        .setDescription("New title for the event")
        .setRequired(true)
    ),

  new SlashCommandBuilder()
    .setName("levent")
    .setDescription("Link a Discord event")
    .addStringOption(opt =>
      opt.setName("id")
        .setDescription("Event ID in FootBot")
        .setRequired(true)
    )
    .addStringOption(opt =>
      opt.setName("discordeventid")
        .setDescription("Discord event ID to link")
        .setRequired(true)
    ),

  new SlashCommandBuilder()
    .setName("view")
    .setDescription("View roster or event")
].map(cmd => cmd.toJSON());

const rest = new REST({ version: "10" }).setToken(process.env.DISCORD_TOKEN!);

async function main() {
  try {
    console.log("Registering commands...");
    await rest.put(
      Routes.applicationGuildCommands(process.env.CLIENT_ID!, process.env.GUILD_ID!),
      { body: commands }
    );
    console.log("✅ Commands registered.");
  } catch (err) {
    console.error(err);
  }
}

main();
