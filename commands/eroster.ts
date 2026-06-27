import { SlashCommandBuilder, ChatInputCommandInteraction } from "discord.js";
import { updateGuildData } from "../utils/guildData";

export const data = new SlashCommandBuilder()
  .setName("eroster")
  .setDescription("Edit a roster")
  .addStringOption(opt =>
    opt.setName("id").setDescription("Roster ID").setRequired(true)
  )
  .addStringOption(opt =>
    opt.setName("name").setDescription("New name").setRequired(false)
  )
  .addRoleOption(opt =>
    opt.setName("assignrole").setDescription("New role").setRequired(false)
  );

export async function execute(interaction: ChatInputCommandInteraction) {
  const id = interaction.options.getString("id", true);
  const newName = interaction.options.getString("name");
  const newRole = interaction.options.getRole("assignrole");

  updateGuildData(interaction.guildId!, data => {
    const roster = data.rosters![id];
    if (roster) {
      if (newName) roster.name = newName;
      if (newRole) roster.roleId = newRole.id;
    }
  });

  await interaction.reply(`✏️ Roster **${id}** updated.`);
}
