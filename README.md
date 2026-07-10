
<!DOCTYPE html>

<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Discord Roster, Event & Minecraft Bot</title>
</head>
<body>
  <h1>Discord Roster, Event & Minecraft Bot</h1>
  <p>A Discord bot for managing <strong>rosters</strong>, <strong>events</strong>, <strong>leaderboards</strong>, <strong>maps</strong>, <strong>hierarchies</strong>, and <strong>Minecraft integration</strong> with a JSON‑backed config system. Built with <code>discord.py</code>.</p>

<h2>✨ Features</h2>
  <ul>
    <li><strong>Roster Management</strong>
      <ul>
        <li>Create, configure, and delete rosters.</li>
        <li>Add/remove members with <code>/add-to-roster</code> and <code>/remove-from-roster</code>.</li>
        <li>View rosters with <code>/view-roster</code>.</li>
      </ul>
    </li>
    <li><strong>Event Management</strong>
      <ul>
        <li>Create, edit, delete, and link events.</li>
        <li>Scheduler loop sends reminders <code>pingMinutesBefore</code> minutes before start.</li>
        <li>View events with <code>/view-event</code> (with pagination).</li>
      </ul>
    </li>
    <li><strong>Leaderboard & Maps</strong>
      <ul>
        <li>Track scores with <code>/leaderboard</code>.</li>
        <li>Create, view, and delete maps.</li>
        <li>Submit results with <code>/submit</code>.</li>
      </ul>
    </li>
    <li><strong>Hierarchy System</strong>
      <ul>
        <li>Add ranks with <code>/add-rank-to-hierarchy</code>.</li>
        <li>View hierarchy with <code>/view-hierarchy</code>.</li>
        <li>Reset hierarchy with <code>/reset-hierarchy</code>.</li>
      </ul>
    </li>
    <li><strong>Minecraft Integration</strong>
      <ul>
        <li>Per‑guild RCON configuration (<code>/setup-mc</code>, <code>/rcon</code>).</li>
        <li>Link/unlink Minecraft accounts (<code>/link-mc</code>, <code>/unlink_mc</code>).</li>
        <li>Manage permissions (<code>/add_permissions_mc</code>, <code>/remove_permissions_mc</code>, <code>/view-permissions-mc</code>).</li>
        <li>Scheduler loop keeps server whitelist in sync automatically.</li>
      </ul>
    </li>
  </ul>

<h2>📜 Commands</h2>
  <table border="1" cellpadding="6" cellspacing="0">
    <thead>
      <tr><th>Command</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td>/config-roster</td><td>Configure roster settings</td></tr>
      <tr><td>/create-roster</td><td>Create a new roster</td></tr>
      <tr><td>/delete-roster</td><td>Delete a roster</td></tr>
      <tr><td>/add-to-roster</td><td>Add a member to a roster</td></tr>
      <tr><td>/remove-from-roster</td><td>Remove a member from a roster</td></tr>
      <tr><td>/view-roster</td><td>View roster details</td></tr>
      <tr><td>/add-permissions-roster</td><td>Add role/member permissions for roster commands</td></tr>
      <tr><td>/remove-permissions-roster</td><td>Remove role/member permissions for roster commands</td></tr>
      <tr><td>/add-permissions-leaderboard</td><td>Add role/member permissions for leaderboard commands</td></tr>
      <tr><td>/remove_permissions-leaderboard</td><td>Remove role/member permissions for leaderboard commands</td></tr>
      <tr><td>/leaderboard</td><td>View leaderboard standings</td></tr>
      <tr><td>/create-event</td><td>Create an event</td></tr>
      <tr><td>/edit-event</td><td>Edit an event</td></tr>
      <tr><td>/delete-event</td><td>Delete an event</td></tr>
      <tr><td>/link-event</td><td>Link a Discord event</td></tr>
      <tr><td>/view-event</td><td>View event details</td></tr>
      <tr><td>/create-map</td><td>Create a new map</td></tr>
      <tr><td>/view-map</td><td>View map details</td></tr>
      <tr><td>/delete-map</td><td>Delete a map</td></tr>
      <tr><td>/submit</td><td>Submit a score or result</td></tr>
      <tr><td>/add-rank-to-hierarchy</td><td>Add a rank to the hierarchy</td></tr>
      <tr><td>/view-hierarchy</td><td>View the rank hierarchy</td></tr>
      <tr><td>/reset-hierarchy</td><td>Reset the rank hierarchy</td></tr>
      <tr><td>/setup-mc</td><td>Initialize per‑guild Minecraft config</td></tr>
      <tr><td>/rcon</td><td>Guild owner only: view or update RCON config</td></tr>
      <tr><td>/link-mc</td><td>Link a Discord user to Minecraft accounts</td></tr>
      <tr><td>/unlink_mc</td><td>Unlink a Minecraft account</td></tr>
      <tr><td>/add_permissions_mc</td><td>Add user/role permissions for Minecraft commands</td></tr>
      <tr><td>/remove_permissions_mc</td><td>Remove user/role permissions for Minecraft commands</td></tr>
      <tr><td>/view-permissions-mc</td><td>View current Minecraft permissions</td></tr>
    </tbody>
  </table>

<h2>📂 Data Structure</h2>
  <pre><code>{
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
    "rosters": { ... },
    "events": { ... },
    "rcon": {
      "host": "your.falix.host",
      "port": 25575,
      "password": "your_rcon_password"
    },
    "links": {
      "111111111111111111": ["PlayerOne", "PlayerTwo"]
    },
    "permissions_mc": {
      "users": ["111111111111111111"],
      "roles": ["Whitelisted", "Admin"]
    }
  }
}</code></pre>

<h2>🔑 Permissions Required</h2>
  <ul>
    <li><strong>Manage Roles</strong> → to assign roster roles.</li>
    <li><strong>Send Messages</strong> → to post reminders.</li>
    <li><strong>Read Messages/View Channels</strong> → to access channels.</li>
    <li><strong>Use Application Commands</strong> → for slash commands.</li>
  </ul>

<h2>🛠 Usage Flow</h2>
  <ol>
    <li>Guild owner runs <code>/setup-mc</code> to initialize Minecraft config.</li>
    <li>Admins configure rosters with <code>/create-roster</code> and add members.</li>
    <li>Events are scheduled with <code>/create-event</code>, linked to rosters.</li>
    <li>Scheduler loop automatically sends reminders before events.</li>
    <li>Members link their Minecraft accounts with <code>/link-mc</code>.</li>
    <li>Scheduler keeps the server whitelist in sync via RCON.</li>
    <li>Admins and owners manage permissions with <code>/add_permissions_mc</code>, <code>/remove_permissions_mc</code>, and view them with <code>/view-permissions-mc</code>.</li>
    <li>Leaderboards, maps, and hierarchies are maintained with their respective commands.</li>
  </ol>
</body>
</html>
