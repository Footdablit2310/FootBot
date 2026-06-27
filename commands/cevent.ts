import {
  SlashCommandBuilder,
  ChatInputCommandInteraction,
  ActionRowBuilder,
  StringSelectMenuBuilder
} from "discord.js";
import crypto from "crypto";
import { updateGuildData } from "../utils/guildData";

export const data = new SlashCommandBuilder()
  .setName("cevent")
  .setDescription("Create an event")
  .addStringOption(opt =>
    opt.setName("title").setDescription("Event title").setRequired(true)
  )
  .addStringOption(opt =>
    opt.setName("time").setDescription("YYYY-MM-DD HH:mm").setRequired(true)
  )
  .addStringOption(opt =>
    opt.setName("assignrosterparam").setDescription("Roster ID").setRequired(false)
  );

export async function execute(interaction: ChatInputCommandInteraction) {
  const title = interaction.options.getString("title", true);
  const timeString = interaction.options.getString("time", true);
  const rosterId = interaction.options.getString("assignrosterparam") ?? undefined;

  const dateUnix = Math.floor(new Date(timeString).getTime() / 1000);
  const eventId = crypto.randomUUID();

  updateGuildData(interaction.guildId!, data => {
    data.events![eventId] = {
      id: eventId,
      title,
      dateUnix,
      rosterId,
      createdBy: interaction.user.id
    };
  });

  const menu = new StringSelectMenuBuilder()
    .setCustomId("event_select")
    .setPlaceholder("Choose next action")
    .addOptions([
      { label: "View Event", value: `view_${eventId}` },
      { label: "Edit Event", value: `edit_${eventId}` },
      { label: "Delete Event", value: `delete_${eventId}` },
      { label: "Ping Roster", value: `ping_${eventId}` }
    ]);

  const row = new ActionRowBuilder<StringSelectMenuBuilder>().addComponents(menu);

  await interaction.reply({
    content: `📅 Event **${title}** scheduled for <t:${dateUnix}:F>${rosterId ? ` (Roster: ${rosterId})` : ""}`,
    components: [row]
  });
}
