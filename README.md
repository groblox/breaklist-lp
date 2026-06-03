# Breaklist — Morning Report Generator for Thermal Printers

![Breaklist hero image](./docs/images/2.jpg)

Breaklist is a toolkit that generates personalized morning reports, designed for thermal printers. The compact summary provides you with all your to-dos, reminders, weather forecast, and the hottest Hacker News highlights — fitting snugly on a dainty, receipt-like paper.

## Features

- **Task list** — Plain-text task management via web UI or direct file editing
- **Reminders** — Crontab-style scheduled reminders (day-of-month, month, day-of-week)
- **Weather forecast** — 18-hour hourly forecast via [Tomorrow.io](https://docs.tomorrow.io/reference/welcome) with temperature, "RealFeel," and weather icons
- **Hacker News digest** — Top 8 article summaries from [hacker-news-digest](https://github.com/polyrabbit/hacker-news-digest)
- **Web app** — SvelteKit-based interface for managing tasks with dark/light mode
- **Dual calendar** — Displays both Persian (Jalali) and Gregorian dates
- **Cross-platform** — Builds for macOS, Linux, and Windows (amd64, arm64, arm, 386)

<details>
<summary>📱 Web App Screenshots</summary>
  <img alt="Task list view" src="https://github.com/alibahmanyar/breaklist/blob/main/docs/images/m1.png" style="width:33%"/>
  <img alt="Add task view" src="https://github.com/alibahmanyar/breaklist/blob/main/docs/images/m2.png" style="width:33%"/>
  <img alt="Dark mode view" src="https://github.com/alibahmanyar/breaklist/blob/main/docs/images/m3.png" style="width:33%"/>
</details>

<details>
<summary>🧾 Complete Report Example</summary>
  <img alt="Full thermal printer report" src="https://github.com/alibahmanyar/breaklist/blob/main/docs/images/1.jpg"/>
</details>

## Architecture

Breaklist consists of three independent components that share data through plain-text `.list` files:

```
┌──────────────────┐      ┌───────────────────────┐      ┌──────────────────┐
│   Frontend       │─────▶│   Backend (Go/Fiber)  │◀────▶│   .list files    │
│   SvelteKit SPA  │      │   Port :3030          │      │   tasks.list     │
│   Static build   │      │   REST API + static   │      │   reminders.list │
└──────────────────┘      └───────────────────────┘      └────────┬─────────┘
                                                                  │
                          ┌───────────────────────┐               │
                          │  Report Generator     │───────────────┘
                          │  Go CLI               │──▶ Tomorrow.io API
                          │  Outputs PDF via       │──▶ Hacker News Digest
                          │  wkhtmltopdf           │──▶ breaklist.pdf
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
- **[Tomorrow.io API key](https://docs.tomorrow.io/reference/welcome)** — Required for weather forecast data
- **[Go 1.21+](https://go.dev/dl/)** — Required if building from source
- **[Node.js & npm](https://nodejs.org/)** — Required if building the frontend from source

### Installation

#### Option 1: Download a Release

Download the latest pre-built binaries from the [GitHub Releases](https://github.com/alibahmanyar/breaklist/releases/latest) page.

#### Option 2: Build from Source

```sh
git clone git@github.com:alibahmanyar/breaklist.git
cd breaklist
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

| Variable | Required By | Description | Example |
|----------|------------|-------------|---------|
| `TOMORROW_API_KEY` | reportGenerator | Tomorrow.io API key for weather data | `abc123def456` |
| `LOCATION` | reportGenerator | Location for weather forecast (city name or coordinates) | `London` |
| `TIMEZONE` | reportGenerator | IANA timezone identifier | `Europe/London` |
| `TASKS_LIST_PATH` | both | Path to the tasks file | `./tasks.list` |
| `REMINDERS_LIST_PATH` | both | Path to the reminders file | `./reminders.list` |

> **Important:** Both the backend and report generator must point to the **same** `.list` files for task/reminder data to stay in sync.

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

### Data Files

#### `tasks.list`

Plain-text file with one task per line. Lines starting with `#` are treated as comments and ignored.

```
Buy groceries
Finish project report
Call dentist
```

#### `reminders.list`

Crontab-style format using 3 fields (day-of-month, month, day-of-week) separated by spaces, followed by a `|` delimiter and the reminder text.

```
#.---------- day of month (1 - 31)
#|  .------- month (1 - 12) OR jan,feb,mar,apr ...
#|  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
#|  |  |

* * *|Take vitamins (Every day)
*/2 * *|Water the plants (Every other day)
* * 6,0|Weekend review (Saturdays and Sundays)
1 * *|Pay rent (1st of every month)
* 1,7 *|Seasonal check-in (January and July)
```

**Supported cron syntax:**

| Pattern | Meaning | Example |
|---------|---------|---------|
| `*` | Every value | `* * *` = every day |
| `N` | Specific value | `15 * *` = 15th of month |
| `N,M` | Multiple values | `1,15 * *` = 1st and 15th |
| `*/N` | Every N-th value | `*/3 * *` = every 3rd day |
| `*/N,M` | Mixed | `*/2,5 * *` = every 2nd day + 5th |

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

### Project Structure

```
breaklist/
├── backend/                # Go web server (Fiber)
│   ├── main.go             # API handlers and server setup
│   ├── go.mod              # Go module definition
│   └── .env.example        # Environment variable template
├── frontend/
│   └── breaklist/          # SvelteKit application
│       ├── src/
│       │   ├── routes/
│       │   │   ├── +page.svelte   # Main app UI (single page)
│       │   │   └── +layout.ts     # Static prerender config
│       │   ├── app.html           # HTML shell
│       │   └── app.d.ts           # TypeScript declarations
│       ├── package.json
│       └── svelte.config.js
├── reportGenerator/        # PDF report generator CLI
│   ├── main.go             # Report orchestration + cron matching
│   ├── weatherReport.go    # Tomorrow.io API integration
│   ├── getHNArticles.go    # Hacker News scraper (Colly)
│   ├── template.html       # Go HTML template for the report
│   ├── main_test.go        # Unit tests (cron matching)
│   ├── weathercodes/       # 152 weather icon PNGs
│   ├── go.mod              # Go module definition
│   └── .env.example        # Environment variable template
├── weatherIcons/           # Icon preprocessing utility
│   ├── threshold.py        # Adaptive thresholding for B&W
│   ├── raw/                # Original weather icons
│   └── thresholded/        # Processed icons
├── docs/                   # Documentation and images
│   └── images/             # Screenshots and photos
├── go.work                 # Go workspace (multi-module)
├── makefile                # Build system
├── .goreleaser.yaml        # Cross-platform release config
└── .gitignore
```

## License

See the repository for license information.
