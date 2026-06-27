import fs from "fs";
import path from "path";

const DATA_FILE = path.join(__dirname, "../../data.json");

export interface GuildData {
  config: Record<string, any>;
  rosters: Record<string, any>;
  events: Record<string, any>;
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
    all[guildId] = { config: {}, rosters: {}, events: {} };
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
    all[guildId] = { config: {}, rosters: {}, events: {} };
  }
  mutator(all[guildId]);
  saveAll(all);
}
