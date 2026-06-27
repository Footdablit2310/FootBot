import { ChatInputCommandInteraction, SlashCommandBuilder } from "discord.js";
import { getGuildData, setGuildData } from "../utils/guildData";
import { ValueIsNullError } from "../utils/nullError";

export const data = new SlashCommandBuilder()
  .setName("croster")
  .setDescription("Create a roster")
  .addStringOption(opt =>
    opt.setName("name").setDescription("Roster name").setRequired(true)
  );

export async function execute(interaction:ChatInputCommandInteraction) {
  const guildId = interaction.guildId;
  const rosterName = interaction.options.getString("name", true);
  if(guildId == null){
    throw new ValueIsNullError()
  }

  const guildData = getGuildData(guildId);
  guildData.rosters![rosterName] = { createdAt: Date.now() };

  setGuildData(guildId, guildData);
  await interaction.reply(`✅ Roster '${rosterName}' created for this guild.`);
}
