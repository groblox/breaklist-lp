# Breaklist — Morning Report Generator for Thermal Printers

![Breaklist hero image](./docs/images/2.jpg)

Breaklist is a toolkit that generates personalized morning reports designed for thermal printers. The compact summary provides you with all your to-dos, reminders, weather forecast, Google Calendar items, and NYT headlines — fitting snugly on a receipt-like paper strip.

## Features

- **Task List & Reminders** — Plain-text task management via SvelteKit web UI, local files, or auto-synced/backed up via Dropbox.
- **Google Calendar** — Displays upcoming calendar events (supporting timed, multi-day, and all-day items) from a specific calendar (e.g. `HeineCal`).
- **Weather Forecast** — Detailed forecast from [Tomorrow.io](https://docs.tomorrow.io/reference/welcome) with temperature, "RealFeel," and B&W optimized weather icons.
- **Personal Weather Station Stats** — Integrates with local weather stations via the [Aeris Weather API](https://www.aerisweather.com/) (e.g. temperature, humidity, wind speed, and rain metrics).
- **New York Times Digest** — Scrapes and displays the latest top headlines.
- **Far Side Comic** — Renders a daily random B&W Far Side cartoon from a local scraped library.
- **Web App** — SvelteKit-based interface for managing tasks with dark/light mode toggle.
- **Cross-Platform** — Builds for macOS, Linux, and Windows (amd64, arm64, arm, 386).

<details>
<summary>📱 Web App Screenshots</summary>
  <img alt="Task list view" src="https://github.com/groblox/breaklist-lp/blob/main/docs/images/m1.png" style="width:33%"/>
  <img alt="Add task view" src="https://github.com/groblox/breaklist-lp/blob/main/docs/images/m2.png" style="width:33%"/>
  <img alt="Dark mode view" src="https://github.com/groblox/breaklist-lp/blob/main/docs/images/m3.png" style="width:33%"/>
</details>

<details>
<summary>🧾 Complete Report Example</summary>
  <img alt="Full thermal printer report" src="https://github.com/groblox/breaklist-lp/blob/main/docs/images/1.jpg"/>
</details>

## Architecture

Breaklist consists of three independent components that share data through plain-text `.list` files (optionally synced with Dropbox):

```
┌──────────────────┐      ┌───────────────────────┐      ┌──────────────────┐
│   Frontend       │─────▶│   Backend (Go/Fiber)  │◀────▶│   .list files    │
│   SvelteKit SPA  │      │   Port :3030          │      │   tasks.list     │
│   Static build   │      │   REST API + static   │      │   reminders.list │
└──────────────────┘      └───────────────────────┘      └────────┬─────────┘
                                                                  │
                          ┌───────────────────────┐               │
                          │  Report Generator     │───────────────┘ (or via Dropbox)
                          │  Go CLI               │──▶ Tomorrow.io API
                          │  Outputs PDF via      │──▶ Aeris Weather API
                          │  wkhtmltopdf          │──▶ Google Calendar API
                          │  grayscale mode       │──▶ breaklist.pdf
                          └───────────────────────┘
```

| Component | Language | Purpose |
|-----------|----------|---------|
| **backend** | Go (Fiber) | REST API for tasks/reminders CRUD, serves the frontend |
| **frontend** | SvelteKit + TypeScript | Web UI for managing tasks (builds to static files) |
| **reportGenerator** | Go | CLI that assembles data and generates the PDF report |

> For detailed architecture documentation, see [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md).
> For the API reference, see [`docs/API.md`](./docs/API.md).

## Getting Started

### Prerequisites

- **[wkhtmltopdf](https://wkhtmltopdf.org/downloads.html)** — Required by the report generator to convert HTML to PDF
- **[Tomorrow.io API Key](https://docs.tomorrow.io/reference/welcome)** — Required for weather forecast data
- **[Go 1.21+](https://go.dev/dl/)** — Required if building from source
- **[Node.js & npm](https://nodejs.org/)** — Required if building the frontend from source

### Installation

#### Build from Source

```sh
git clone https://github.com/groblox/breaklist-lp.git
cd breaklist-lp
make setup    # Install frontend npm dependencies
make          # Build all components
```

The compiled binaries and assets will be placed in the `build/` directory:

```
build/
├── webserver           # Backend server binary
├── reportGenerator     # Report generator binary
├── static/             # Built frontend assets
├── template.html       # Report HTML template
├── weathercodes/       # Weather icon PNGs
└── .env.example        # Example configuration
```

### Configuration

Duplicate `.env.example` and rename it to `.env`, then populate the variables:

| Variable | Component | Description | Example |
|----------|------------|-------------|---------|
| `TOMORROW_API_KEY` | reportGenerator | Tomorrow.io API key for weather data | `abc123def456` |
| `LOCATION` | reportGenerator | Location coordinates for forecast | `33.4054,-86.8114` |
| `TIMEZONE` | reportGenerator | IANA timezone identifier | `America/Chicago` |
| `TASKS_LIST_PATH` | both | Path to local tasks file (fallback) | `./tasks.list` |
| `REMINDERS_LIST_PATH` | both | Path to local reminders file | `./reminders.list` |
| `GOOGLE_CLIENT_ID` | reportGenerator | Google OAuth 2.0 Client ID | `82441593318-...apps.googleusercontent.com` |
| `GOOGLE_CLIENT_SECRET` | reportGenerator | Google OAuth 2.0 Client Secret | `GOCSPX-...` |
| `GOOGLE_CALENDAR_ID` | reportGenerator | Specific Google Calendar Name or ID | `HeineCal` |
| `GOOGLE_REFRESH_TOKEN` | reportGenerator | Authenticated Google Refresh Token | *(Set via CLI auth)* |
| `DROPBOX_APP_KEY` | both | Dropbox App Key for backup | `vmj3ivdahewiqzu` |
| `DROPBOX_REFRESH_TOKEN` | both | Authenticated Dropbox Refresh Token | *(Set via CLI auth)* |
| `DROPBOX_FILE_PATH` | both | Path to list in Dropbox | `/breaklist/tasks.list` |

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

#### Web Server (Task Management)

```sh
./webserver
```

The web app will be available at [http://localhost:3030](http://localhost:3030). Use it to add, view, and delete tasks.

#### Report Generator (PDF Output)

```sh
./reportGenerator
```

Generates `breaklist.pdf` in the current directory, ready to print on a thermal printer.

> **Tip:** Schedule the report generator with cron (Linux/macOS) or Task Scheduler (Windows) to generate your report every morning automatically.

## Development

For detailed development setup and contribution guidelines, see [`docs/DEVELOPMENT.md`](./docs/DEVELOPMENT.md).

### Quick Start (Development)

```sh
# Terminal 1: Run the backend with hot-reload
cd backend
go run .

# Terminal 2: Run the frontend dev server  
cd frontend/breaklist
npm run dev
```

## License

See the repository for license information.
