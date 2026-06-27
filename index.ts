import { Client, GatewayIntentBits, Interaction } from "discord.js";
import { routeInteraction } from "./interactionRouter";
import { croster } from "./commands/croster";
import { droster } from "./commands/droster";
import { eroster } from "./commands/eroster";
import { config } from "./commands/config";
import { cevent } from "./commands/cevent";
import { devent } from "./commands/devent";
import { eevent } from "./commands/eevent";
import { levent } from "./commands/levent";
import { execute as viewCommand } from "./commands/view";

import dotenv from "dotenv";
dotenv.config();

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
