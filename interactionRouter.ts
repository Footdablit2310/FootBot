import {
  Interaction,
  StringSelectMenuInteraction
} from "discord.js";
import { handleViewType } from "./interactions/viewType";
import { handleViewEvent } from "./interactions/viewEvent";
import { handleViewRoster } from "./interactions/viewRoster";

export async function routeInteraction(interaction: Interaction) {
  if (!interaction.isStringSelectMenu()) return;

  switch (interaction.customId) {
    case "viewType":
      await handleViewType(interaction as StringSelectMenuInteraction);
      break;

    case "viewEvent":
      await handleViewEvent(interaction as StringSelectMenuInteraction);
      break;

    case "viewRoster":
      await handleViewRoster(interaction as StringSelectMenuInteraction);
      break;

    default:
      // Unknown customId — ignore or log
      console.warn(`Unhandled select menu: ${interaction.customId}`);
      break;
  }
}
