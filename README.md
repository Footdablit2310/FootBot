<!DOCTYPE html>

<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
<body>
  <h1>Discord Roster & Event Bot</h1>
  <p>A Discord bot for managing <strong>rosters</strong>, <strong>events</strong>, and <strong>permissions</strong> with a JSON‑backed config system. Built with <code>discord.py</code>.</p>
  <h2>Invite Link</h2>
    <strong>https://discord.com/oauth2/authorize?client_id=1520285404878737458</strong>
  <h2>✨ Features</h2>
  <ul>
    <li><strong>Roster Management</strong>
      <ul>
        <li>Create rosters with names and linked roles.</li>
        <li>Add/remove members with <code>/aroster</code> and <code>/rroster</code>.</li>
        <li>Automatically assign/remove Discord roles when members join/leave.</li>
        <li>View rosters with <code>/view-roster</code>.</li>
      </ul>
    </li>
    <li><strong>Event Management</strong>
      <ul>
        <li>Create events with <code>/cevent</code> (title, UNIX time, roster link).</li>
        <li>Scheduler loop sends reminders <code>pingMinutesBefore</code> minutes before start.</li>
        <li>Reminders mention roster roles if linked.</li>
        <li>View events with <code>/view-event</code> (with pagination).</li>
      </ul>
    </li>
    <li><strong>Permissions System</strong>
      <ul>
        <li><code>/apermissions</code> → add role/member IDs to the guild’s permissions config.</li>
        <li><code>/rpermissions</code> → remove role/member IDs from the config.</li>
        <li>Commands validate against stored permissions before running.</li>
        <li>Supports global <code>permissions.all</code> key for universal access.</li>
      </ul>
    </li>
    <li><strong>Config System</strong>
      <ul>
        <li>Per‑guild JSON storage.</li>
        <li>Keys:
          <ul>
            <li><code>pingMinutesBefore</code> → minutes before event reminder.</li>
            <li><code>eventChannelId</code> → channel ID for reminders.</li>
            <li><code>permissions</code> → role/member IDs allowed to run commands.</li>
          </ul>
        </li>
        <li>Separate sections for <code>rosters</code> and <code>events</code>.</li>
      </ul>
    </li>
  </ul>

<h2>📜 Commands</h2>
  <table border="1" cellpadding="6" cellspacing="0">
    <thead>
      <tr>
        <th>Command</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>/aroster</td><td>Add a member to a roster</td></tr>
      <tr><td>/rroster</td><td>Remove a member from a roster</td></tr>
      <tr><td>/view-roster</td><td>Dropdown to view roster details (with pagination)</td></tr>
      <tr><td>/cevent</td><td>Create an event (title, time, roster link)</td></tr>
      <tr><td>/view-event</td><td>Dropdown to view event details (with pagination)</td></tr>
      <tr><td>/apermissions_roster</td><td>Add role/member permissions</td></tr>
      <tr><td>/rpermissions_roster</td><td>Remove role/member permissions</td></tr>
    </tbody>
  </table>

<h2>🚀 Invite the Bot</h2>
  <p>To add the bot to your server, use this OAuth2 link:</p>
  <pre>
https://discord.com/oauth2/authorize?client_id=1520285404878737458
  </pre>

<h2>⚙️ Setup</h2>
  <ol>
    <li>Clone the repo.</li>
    <li>Install dependencies:
      <pre>pip install -U discord.py</pre>
    </li>
    <li>Create a <code>.env</code> file with your bot token:
      <pre>DISCORD_TOKEN=your_token_here</pre>
    </li>
    <li>Run the bot:
      <pre>python bot.py</pre>
    </li>
  </ol>

<h2>📂 Data Structure</h2>
  <pre>{
  "guild_id": {
    "config": {
      "pingMinutesBefore": 15,
      "eventChannelId": "1234567890",
      "permissions": {
        "roles": ["1111111111"],
        "members": ["2222222222"],
        "all": ["3333333333"]
      }
    },
    "rosters": {
      "roster_id": {
        "name": "Team A",
        "roleId": "4444444444",
        "members": { "Leader": "5555555555" },
        "createdBy": "6666666666"
      }
    },
    "events": {
      "event_id": {
        "title": "Scrim",
        "dateUnix": 1756400000,
        "rosterId": "roster_id",
        "createdBy": "7777777777",
        "pinged": false,
        "linkedDiscordEventId": null
      }
    }
  }
}</pre>

<h2>🔑 Permissions Required</h2>
  <ul>
    <li><strong>Manage Roles</strong> → to assign roster roles.</li>
    <li><strong>Send Messages</strong> → to post reminders.</li>
    <li><strong>Read Messages/View Channels</strong> → to access channels.</li>
    <li><strong>Use Application Commands</strong> → for slash commands.</li>
  </ul>
</body>
</html>
