📝 Bot Development To‑Do List
0. Recreate old stuff
    - /config
    - /croster
    - /cevent
    - /droster
    - /devent
    - /eroster
    - /eevent
1. Add new roster commands
    - /aroster → Add a member to a roster.
        - Parameters: rosterId, userId, position (e.g. Captain, P1, Substitute).
        - Updates data.rosters[rosterId].members[position] = userId.

    - /rroster → Remove a member from a roster.

        - Parameters: rosterId, position.
        - Deletes data.rosters[rosterId].members[position].

2. Restrict command visibility
    - Make all commands except /view ephemeral (user‑only).
    - This means: /croster, /droster, /eroster, /cevent, /devent, /eevent, /levent, /aroster, /rroster, /config → replies are visible only to the user who ran them.
    - /view remains public so everyone can see roster/event details.

3. Update interaction router
    - Add select‑menu options for aroster and rroster so users can manage roster membership via dropdowns.
    - Ensure modal handlers exist for editing roster membership if needed.

4. Scheduler integration
    - Confirm that roster membership changes (aroster/rroster) are reflected in event pings.
    - When an event is linked to a roster, ping all current members (or the roster role) before the event.

5. Testing
    - Dry‑run:
        - Create a roster with /croster.
        - Add members with /aroster.
        - Create an event with /cevent linked to that roster.
        - Set /config pingMinutesBefore to a small value.
        - Watch the scheduler ping the roster role/members at the right time.