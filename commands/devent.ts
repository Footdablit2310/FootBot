import { SlashCommandBuilder, ChatInputCommandInteraction } from "discord.js";
import { updateGuildData } from "../utils/guildData";

export const data = new SlashCommandBuilder()
  .setName("devent")
  .setDescription("Delete an event")
  .addStringOption(opt =>
    opt.setName("id").setDescription("Event ID").setRequired(true)
  );

export async function execute(interaction: ChatInputCommandInteraction) {
  const id = interaction.options.getString("id", true);

  updateGuildData(interaction.guildId!, data => {
    delete data.events![id];
  });

  await interaction.reply(`🗑️ Event **${id}** deleted.`);
}
