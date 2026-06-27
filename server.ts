import express from "express";
import { clientId } from "./index";

const app = express();
const PORT = process.env.PORT || 3000;

// Invite link (replace with your bot’s client ID)
const inviteUrl = `https://discord.com/oauth2/authorize?client_id=${clientId}&scope=bot%20applications.commands&permissions=8`;

app.get("/", (_, res) => {
  res.send(`
    <html>
      <head><title>FootBot Invite</title></head>
      <body style="font-family:sans-serif;max-width:600px;margin:auto;">
        <h1>🚀 Invite FootBot</h1>
        <p>Click below to add FootBot to your server:</p>
        <p><a href="${inviteUrl}" target="_blank">Invite FootBot</a></p>
        <hr/>
        <h2>📖 Documentation</h2>
        <ul>
          <li><b>/croster</b> – Create a roster</li>
          <li><b>/droster</b> – Delete a roster</li>
          <li><b>/eroster</b> – Edit a roster</li>
          <li><b>/view</b> – View rosters/events</li>
          <li><b>/cevent</b> – Create an event</li>
          <li><b>/devent</b> – Delete an event</li>
          <li><b>/eevent</b> – Edit an event</li>
          <li><b>/levent</b> – Link to a Discord event</li>
          <li><b>/config</b> – Configure guild settings</li>
        </ul>
        <p>FootBot keeps data per guild, so each server has its own rosters and events.</p>
      </body>
    </html>
  `);
});

app.listen(PORT, () => {
  console.log(`Invite/docs page running on port ${PORT}`);
});
