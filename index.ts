import { Client, GatewayIntentBits, Interaction } from "discord.js";
import { routeInteraction } from "./interactionRouter";
import { execute as croster } from "./commands/croster";
import { execute as droster } from "./commands/droster";
import { execute as eroster } from "./commands/eroster";
import { execute as config} from "./commands/config";
import { execute as cevent} from "./commands/cevent";
import { execute as eevent} from "./commands/eevent";
import { execute as devent} from "./commands/devent";
import { execute as levent} from "./commands/levent";
import { execute as viewCommand } from "./commands/view";

import dotenv from "dotenv";
dotenv.config();

export const clientId = process.env.CLIENT_ID!;
export const token = process.env.DISCORD_TOKEN!;
export const guildId = process.env.GUILD_ID!;


const client = new Client({ intents: [GatewayIntentBits.Guilds] });

client.once("ready", () => {
    console.log(`✅ Logged in as ${client.user?.tag}`);
});

client.on("interactionCreate", async (interaction: Interaction) => {
    try {
        if (interaction.isChatInputCommand()) {
            switch (interaction.commandName) {
                case "view": await viewCommand(interaction); break;
                case "croster": await croster(interaction); break;
                case "droster": await droster(interaction); break;
                case "eroster": await eroster(interaction); break;
                case "config": await config(interaction); break;
                case "cevent": await cevent(interaction); break;
                case "devent": await devent(interaction); break;
                case "eevent": await eevent(interaction); break;
                case "levent": await levent(interaction); break;
            }

        } else if (interaction.isStringSelectMenu()) {
            await routeInteraction(interaction);
        }
    } catch (err) {
        console.error("Interaction error:", err);
    }
});

client.login(process.env.DISCORD_TOKEN);
