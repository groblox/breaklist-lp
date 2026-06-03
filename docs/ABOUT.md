# What is Breaklist?

Breaklist is a personal morning briefing that prints on a thermal receipt printer. Think of it as a tiny, daily newspaper — just for you.

Every morning it generates a small PDF containing:

- 📝 **Your tasks** — pulled directly from your Dropbox JSON file
- 🔔 **Today's reminders** — recurring notes that match today's date
- ☀️ **18-hour weather forecast** — temperature, "feels like," and icons
- 📰 **Top Hacker News stories** — titles, summaries, and vote counts

The PDF is sized for 47mm-wide receipt paper. Print it, tear it off, and carry your day in your pocket.

## How it works

Breaklist is a command-line tool you run (or schedule with cron). It pulls together your tasks from Dropbox, reminders from a local file, weather, and news, then spits out `breaklist.pdf`.

You can easily link your Dropbox account using the built-in CLI link helper:
```bash
./reportGenerator auth
```
This opens your browser, lets you log in, and automatically saves your credentials.

## The stack

| Part | Built with |
|------|-----------|
| CLI Program | Go |
| PDF conversion | [wkhtmltopdf](https://wkhtmltopdf.org/) |
| Weather data | [Tomorrow.io](https://www.tomorrow.io/) API |
| News summaries | [Hacker News Digest](https://github.com/polyrabbit/hacker-news-digest) |

## Who is it for?

Anyone who wants a low-tech, distraction-free way to start their day. No apps to open, no notifications — just a slip of paper with everything you need to know.
