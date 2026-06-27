import { SlashCommandBuilder, ChatInputCommandInteraction } from "discord.js";
import { updateGuildData } from "../utils/guildData";

export const data = new SlashCommandBuilder()
  .setName("levent")
  .setDescription("Link a Discord event")
  .addStringOption(opt =>
    opt.setName("id").setDescription("FootBot event ID").setRequired(true)
  )
  .addStringOption(opt =>
    opt.setName("discordeventid").setDescription("Discord event ID").setRequired(true)
  );

export async function execute(interaction: ChatInputCommandInteraction) {
  const id = interaction.options.getString("id", true);
  const discordEventId = interaction.options.getString("discordeventid", true);

  updateGuildData(interaction.guildId!, data => {
    const event = data.events![id];
    if (event) {
      event.discordEventId = discordEventId;
    }
  });

  await interaction.reply(`🔗 Linked FootBot event **${id}** to Discord event **${discordEventId}**.`);
}
