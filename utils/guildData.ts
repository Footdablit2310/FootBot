import fs from "fs";
import path from "path";

const DATA_FILE = path.join(__dirname, "../data.json");

interface GuildData {
  config?: Record<string, any>;
  rosters?: Record<string, any>;
  events?: Record<string, any>;
}

function loadData(): Record<string, GuildData> {
  if (!fs.existsSync(DATA_FILE)) return {};
  return JSON.parse(fs.readFileSync(DATA_FILE, "utf8"));
}

function saveData(data: Record<string, GuildData>) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

export function getGuildData(guildId: string): GuildData {
  const data = loadData();
  if (!data[guildId]) {
    data[guildId] = { config: {}, rosters: {}, events: {} };
    saveData(data);
  }
  return data[guildId];
}

export function setGuildData(guildId: string, newData: GuildData) {
  const data = loadData();
  data[guildId] = newData;
  saveData(data);
}
