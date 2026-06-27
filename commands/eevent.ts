import { SlashCommandBuilder, ChatInputCommandInteraction } from "discord.js";
import { updateGuildData } from "../utils/guildData";

export const data = new SlashCommandBuilder()
  .setName("eevent")
  .setDescription("Edit an event")
  .addStringOption(opt =>
    opt.setName("id").setDescription("Event ID").setRequired(true)
  )
  .addStringOption(opt =>
    opt.setName("title").setDescription("New title").setRequired(false)
  )
  .addStringOption(opt =>
    opt.setName("time").setDescription("New time (YYYY-MM-DD HH:mm)").setRequired(false)
  );

export async function execute(interaction: ChatInputCommandInteraction) {
  const id = interaction.options.getString("id", true);
  const newTitle = interaction.options.getString("title");
  const newTime = interaction.options.getString("time");

  updateGuildData(interaction.guildId!, data => {
    const event = data.events![id];
    if (event) {
      if (newTitle) event.title = newTitle;
      if (newTime) event.dateUnix = Math.floor(new Date(newTime).getTime() / 1000);
    }
  });

  await interaction.reply(`✏️ Event **${id}** updated.`);
}
