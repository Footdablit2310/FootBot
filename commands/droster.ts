import { SlashCommandBuilder, ChatInputCommandInteraction } from "discord.js";
import { updateGuildData } from "../utils/guildData";

export const data = new SlashCommandBuilder()
  .setName("droster")
  .setDescription("Delete a roster")
  .addStringOption(opt =>
    opt.setName("id").setDescription("Roster ID").setRequired(true)
  );

export async function execute(interaction: ChatInputCommandInteraction) {
  const id = interaction.options.getString("id", true);

  updateGuildData(interaction.guildId!, data => {
    delete data.rosters![id];
  });

  await interaction.reply(`🗑️ Roster **${id}** deleted.`);
}
