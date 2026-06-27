import {
  SlashCommandBuilder,
  ChatInputCommandInteraction,
  ActionRowBuilder,
  StringSelectMenuBuilder
} from "discord.js";
import crypto from "crypto";
import { updateGuildData } from "../utils/guildData";

export const data = new SlashCommandBuilder()
  .setName("croster")
  .setDescription("Create a roster")
  .addStringOption(opt =>
    opt.setName("name").setDescription("Roster name").setRequired(true)
  )
  .addRoleOption(opt =>
    opt.setName("assignrole").setDescription("Discord role to assign").setRequired(false)
  );

export async function execute(interaction: ChatInputCommandInteraction) {
  const name = interaction.options.getString("name", true);
  const role = interaction.options.getRole("assignrole");
  const rosterId = crypto.randomUUID();

  updateGuildData(interaction.guildId!, data => {
    data.rosters![rosterId] = {
      id: rosterId,
      name,
      roleId: role?.id,
      createdBy: interaction.user.id
    };
  });

  const menu = new StringSelectMenuBuilder()
    .setCustomId("roster_select")
    .setPlaceholder("Choose next action")
    .addOptions([
      { label: "View Roster", value: `view_${rosterId}` },
      { label: "Edit Roster", value: `edit_${rosterId}` },
      { label: "Delete Roster", value: `delete_${rosterId}` }
    ]);

  const row = new ActionRowBuilder<StringSelectMenuBuilder>().addComponents(menu);

  await interaction.reply({
    content: `📋 Roster **${name}** created${role ? ` with role <@&${role.id}>` : ""}.`,
    components: [row]
  });
}
