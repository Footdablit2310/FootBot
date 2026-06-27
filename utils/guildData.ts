import { ChatInputCommandInteraction } from "discord.js";
import fs from "fs";
import path from "path";

const DATA_FILE = path.join(__dirname, "../../data.json");

export interface Config {
  pingMinutesBefore: number;
  adminRoleId?: string;
  eventChannelId?: string;
}
export type ConfigKey = keyof Config; 
// "pingMinutesBefore" | "adminRoleId" | "eventChannelId"

export interface Roster {
  id: string;
  name: string;
  roleId?: string;
  createdBy: string;
}

export interface Event {
  id: string;
  title: string;
  dateUnix: number;
  rosterId?: string;
  createdBy: string;
  discordEventId?: string;
  pinged?: boolean;
}

export interface GuildData {
  config: Config;
  rosters: Record<string, Roster>;
  events: Record<string, Event>;
}

export function createEmptyGuildData(): GuildData {
  return {
    config: { pingMinutesBefore: 15 },
    rosters: {},
    events: {}
  };
}

function loadAll(): Record<string, GuildData> {
  if (!fs.existsSync(DATA_FILE)) {
    return {};
  }
  const raw = fs.readFileSync(DATA_FILE, "utf8");
  return JSON.parse(raw) as Record<string, GuildData>;
}

function saveAll(data: Record<string, GuildData>) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

/**
 * Get data for a specific guild. Auto‑initializes if missing.
 */
export function getGuildData(guildId: string): GuildData {
  const all = loadAll();
  if (!all[guildId]) {
    all[guildId] = createEmptyGuildData();
    saveAll(all);
  }
  return all[guildId];
}

/**
 * Update data for a specific guild. Merges with existing instead of overwriting.
 */
export function updateGuildData(guildId: string, mutator: (data: GuildData) => void) {
  const all = loadAll();
  if (!all[guildId]) {
    all[guildId] = createEmptyGuildData();
  }
  mutator(all[guildId]);
  saveAll(all);
}

export async function execute(interaction: ChatInputCommandInteraction) {
  const key = interaction.options.getString("key") as ConfigKey | null;
  const value = interaction.options.getString("value");

  if (key && value) {
    updateGuildData(interaction.guildId!, data => {
      if (key === "pingMinutesBefore") {
        data.config.pingMinutesBefore = Number(value);
      } else if (key === "adminRoleId") {
        data.config.adminRoleId = value;
      } else if (key === "eventChannelId") {
        data.config.eventChannelId = value;
      }
    });
    await interaction.reply(`⚙️ Config **${key}** updated to **${value}**.`);
    return;
  }

  // ... embed display logic ...
}

export function setConfigValue(
  guildId: string,
  key: ConfigKey,
  value: string | number
) {
  updateGuildData(guildId, data => {
    if (key === "pingMinutesBefore") {
      data.config.pingMinutesBefore = Number(value);
    } else {
      data.config[key] = value as any;
    }
  });
}

