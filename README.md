# Breaklist — Morning Report Generator for Thermal Printers

![Breaklist hero image](./docs/images/2.jpg)

Breaklist is a toolkit that generates personalized morning reports designed for thermal printers. The compact summary provides you with all your to-dos, reminders, weather forecast, Google Calendar items, and NYT headlines — fitting snugly on a receipt-like paper strip.

## Features

- **Task List & Reminders** — Plain-text task management via local files, or auto-synced/backed up via Dropbox.
- **Google Calendar** — Displays upcoming calendar events (supporting timed, multi-day, and all-day items) from a specific calendar (e.g. `HeineCal`).
- **Weather Forecast** — Detailed forecast from [Tomorrow.io](https://docs.tomorrow.io/reference/welcome) with temperature, "RealFeel," and B&W optimized weather icons.
- **Personal Weather Station Stats** — Integrates with local weather stations via the [Aeris Weather API](https://www.aerisweather.com/) (e.g. temperature, humidity, wind speed, and rain metrics).
- **New York Times Digest** — Scrapes and displays the latest top headlines.
- **Far Side Comic** — Renders a daily random B&W Far Side cartoon from a local scraped library.
- **Cross-Platform** — Builds for macOS, Linux, and Windows (amd64, arm64, arm, 386).

<details>
<summary>🧾 Complete Report Example</summary>
  <img alt="Full thermal printer report" src="https://github.com/groblox/breaklist-lp/blob/main/docs/images/1.jpg"/>
</details>

## Architecture

Breaklist processes local plain-text `.list` files (optionally synced with Dropbox) and external APIs to build a printable PDF report:

```
┌──────────────────┐
│   .list files    │◀──────────────┐
│   tasks.list     │               │
│   reminders.list │               │
└────────┬─────────┘               │
         │                         │
         ▼                         │
┌──────────────────┐               │
│ Report Generator │───────────────┘ (or via Dropbox)
│ Go CLI           │──▶ Tomorrow.io API
│ Outputs PDF via  │──▶ Aeris Weather API
│ wkhtmltopdf      │──▶ Google Calendar API
│ grayscale mode   │──▶ breaklist.pdf
└──────────────────┘
```

The core codebase is located under the `reportGenerator` directory, supported by a shared utilities package under `shared`.

> For detailed architecture documentation, see [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md).

## Getting Started

### Prerequisites

- **[wkhtmltopdf](https://wkhtmltopdf.org/downloads.html)** — Required by the report generator to convert HTML to PDF
- **[Tomorrow.io API Key](https://docs.tomorrow.io/reference/welcome)** — Required for weather forecast data
- **[Go 1.21+](https://go.dev/dl/)** — Required if building from source

### Installation

#### Build from Source

```sh
git clone https://github.com/groblox/breaklist-lp.git
cd breaklist-lp
make          # Build the reportGenerator CLI
```

The compiled binaries and assets will be placed in the `build/` directory:

```
build/
├── reportGenerator     # Report generator binary
├── template.html       # Report HTML template
├── weathercodes/       # Weather icon PNGs
└── .env.example        # Example configuration
```

### Configuration

Duplicate `.env.example` and rename it to `.env`, then populate the variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `TOMORROW_API_KEY` | Tomorrow.io API key for weather data | `abc123def456` |
| `LOCATION` | Location coordinates for forecast | `33.4054,-86.8114` |
| `TIMEZONE` | IANA timezone identifier | `America/Chicago` |
| `TASKS_LIST_PATH` | Path to local tasks file (fallback) | `./tasks.list` |
| `REMINDERS_LIST_PATH` | Path to local reminders file | `./reminders.list` |
| `GOOGLE_CLIENT_ID` | Google OAuth 2.0 Client ID | `82441593318-...apps.googleusercontent.com` |
| `GOOGLE_CLIENT_SECRET` | Google OAuth 2.0 Client Secret | `GOCSPX-...` |
| `GOOGLE_CALENDAR_ID` | Specific Google Calendar Name or ID | `HeineCal` |
| `GOOGLE_REFRESH_TOKEN` | Authenticated Google Refresh Token | *(Set via CLI auth)* |
| `DROPBOX_APP_KEY` | Dropbox App Key for backup | `vmj3ivdahewiqzu` |
| `DROPBOX_REFRESH_TOKEN` | Authenticated Dropbox Refresh Token | *(Set via CLI auth)* |
| `DROPBOX_FILE_PATH` | Path to list in Dropbox | `/breaklist/tasks.list` |

### Setting Up Authentication

To authorize Google Calendar or Dropbox, run the CLI authorization flows:

#### Google Calendar Authorization
```sh
# Run the reportGenerator with the auth-google flag:
./reportGenerator --auth-google
```
This will open your web browser, prompt you to sign in with Google, and automatically save the required refresh token to your `.env` file.

#### Dropbox Integration
```sh
# Run the reportGenerator with the auth flag:
./reportGenerator --auth
```
This will open your web browser, prompt you to link your Dropbox account, and save the refresh token to your `.env` file for automatic task-list backups/syncing.

### Usage

#### Report Generator (PDF Output)

```sh
./reportGenerator
```

Generates `breaklist.pdf` in the current directory, ready to print on a thermal printer.

> **Tip:** Schedule the report generator with cron (Linux/macOS) or Task Scheduler (Windows) to generate your report every morning automatically.

## Development

### Project Structure

```
breaklist-lp/
├── reportGenerator/        # PDF report generator CLI
│   ├── main.go             # Report orchestration + cron matching
│   ├── weatherReport.go    # Tomorrow.io API integration
│   ├── getHNArticles.go    # Hacker News scraper (unused)
│   ├── getNYTArticles.go   # NY Times scraper (upstract)
│   ├── template.html       # Go HTML template for the report
│   ├── main_test.go        # Unit tests (cron matching)
│   ├── weathercodes/       # Weather icon PNGs
│   ├── go.mod              # Go module definition
│   └── .env.example        # Environment variable template
├── shared/                 # Shared Dropbox and utility helper functions
├── weatherIcons/           # Icon preprocessing utility
├── docs/                   # Documentation and images
├── go.work                 # Go workspace (multi-module)
├── makefile                # Build system
├── .goreleaser.yaml        # Cross-platform release config
└── .gitignore
```

## License

See the repository for license information.
