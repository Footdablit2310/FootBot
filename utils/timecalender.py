"""TC FILE"""
import datetime
from typing import Callable, Any

import discord
import pytz


# pylint: disable=W0221, W0718
class TimeModal(discord.ui.Modal, title="Select Time"):
    """TM"""

    hour: str = discord.ui.TextInput(label="Hour (0-23)").value
    minute: str = discord.ui.TextInput(label="Minute (0-59)").value

    def __init__(
        self, year: int, month: int, day: int, callback: Callable[[int], None]
    ) -> None:
        super().__init__()
        self.year: int = year
        self.month: int = month
        self.day: int = day
        self._callback: Callable[[int], None] = callback

    async def on_submit(self, interaction: discord.Interaction) -> None:
        try:
            h: int = int(self.hour)
            m: int = int(self.minute)
            await interaction.response.send_message(
                "🌍 Select your timezone:",
                view=TimezoneView(
                    self.year, self.month, self.day, h, m, self._callback
                ),
            )
        except Exception:
            await interaction.response.send_message("❌ Invalid hour/minute input.")


class TimezoneSelect(discord.ui.Select[Any]):
    """TZS"""
    def __init__(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        callback: Callable[[int], None],
    ) -> None:
        options: list[discord.SelectOption] = [
            discord.SelectOption(label="UTC", value="UTC"),
            discord.SelectOption(label="Asia/Kolkata", value="Asia/Kolkata"),
            discord.SelectOption(label="America/New_York", value="America/New_York"),
            discord.SelectOption(label="Europe/London", value="Europe/London"),
        ]
        super().__init__(placeholder="Select your timezone...", options=options)
        self.year, self.month, self.day = year, month, day
        self.hour, self.minute = hour, minute
        self._callback: Callable[[int], None] = callback

    async def callback(self, interaction: discord.Interaction) -> None:
        tz: pytz.BaseTzInfo = pytz.timezone(self.values[0])
        dt_local: datetime.datetime = tz.localize(
            datetime.datetime(self.year, self.month, self.day, self.hour, self.minute)
        )
        dt_utc: datetime.datetime = dt_local.astimezone(datetime.timezone.utc)
        unix_ts: int = int(dt_utc.timestamp())

        # Return UNIX stamp to caller
        self._callback(unix_ts)

        await interaction.response.edit_message(
            content=f"✅ Got UNIX timestamp: {unix_ts} (<t:{unix_ts}:F>)", view=None
        )


class TimezoneView(discord.ui.View):
    """TZV"""
    def __init__(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        callback: Callable[[int], None],
    ) -> None:
        super().__init__(timeout=60)
        self.add_item(TimezoneSelect(year, month, day, hour, minute, callback))


class CalendarView(discord.ui.View):
    """CalV"""
    def __init__(self, year: int, month: int, callback: Callable[[int], None]) -> None:
        super().__init__(timeout=60)
        self.year: int = year
        self.month: int = month
        self._callback: Callable[[int], None] = callback
        self.build_calendar()

    def build_calendar(self) -> None:
        """BCal"""
        self.clear_items()
        self.add_item(
            discord.ui.Button(
                label="◀", style=discord.ButtonStyle.secondary, custom_id="prev"
            )
        )
        self.add_item(
            discord.ui.Button(
                label="▶", style=discord.ButtonStyle.secondary, custom_id="next"
            )
        )
        days_in_month: int = (
            datetime.date(self.year, (self.month % 12) + 1, 1)
            - datetime.timedelta(days=1)
        ).day
        for day in range(1, days_in_month + 1):
            self.add_item(
                discord.ui.Button(
                    label=str(day),
                    style=discord.ButtonStyle.primary,
                    custom_id=f"day_{day}",
                )
            )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        cid: str = interaction.data["custom_id"]  # type: ignore[index]
        if not isinstance(cid, str):
            raise ValueError("Invalid type")
        elif cid == "prev":
            self.month -= 1
            if self.month < 1:
                self.month = 12
                self.year -= 1
            self.build_calendar()
            await interaction.response.edit_message(view=self)
        elif cid == "next":
            self.month += 1
            if self.month > 12:
                self.month = 1
                self.year += 1
            self.build_calendar()
            await interaction.response.edit_message(view=self)
        elif cid.startswith("day_"):
            day: int = int(cid.split("_")[1])
            await interaction.response.send_modal(
                TimeModal(self.year, self.month, day, self._callback)
            )
        return True


# pylint: enable=W0221, W0718
