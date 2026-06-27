import { Client, TextChannel } from "discord.js";
import { GuildData, Event } from "./utils/guildData";
import fs from "fs";
import path from "path";

const DATA_FILE = path.join(__dirname, "../data.json");

function loadAll(): Record<string, GuildData> {
  if (!fs.existsSync(DATA_FILE)) return {};
  return JSON.parse(fs.readFileSync(DATA_FILE, "utf8")) as Record<string, GuildData>;
}

export function startScheduler(client: Client) {
  setInterval(async () => {
    const now = Math.floor(Date.now() / 1000);
    const allGuilds = loadAll();

    for (const [guildId, guildData] of Object.entries(allGuilds)) {
      const pingMinutes = guildData.config.pingMinutesBefore ?? 15;
      const threshold = pingMinutes * 60;

      for (const ev of Object.values(guildData.events)) {
        // ev is typed as Event
        if (!ev.dateUnix) continue;

        if (ev.dateUnix - now <= threshold && !ev.pinged) {
          const guild = client.guilds.cache.get(guildId);
          if (!guild) continue;

          const channelId = guildData.config.eventChannelId;
          const channel = channelId ? guild.channels.cache.get(channelId) as TextChannel : null;

          const roster = ev.rosterId ? guildData.rosters[ev.rosterId] : undefined;
          const roleMention = roster?.roleId ? `<@&${roster.roleId}>` : "";

          if (channel) {
            await channel.send(
              `🔔 Reminder: Event **${ev.title}** starts at <t:${ev.dateUnix}:F>. ${roleMention}`
            );
          }

          ev.pinged = true;
        }
      }
    }
  }, 60 * 1000); // check every minute
}
