# Development Guide

This guide covers how to set up a development environment, build the project, run tests, and create releases.

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| [Go](https://go.dev/dl/) | 1.21+ | Backend and report generator |
| [Node.js](https://nodejs.org/) | 18+ (LTS recommended) | Frontend build |
| [npm](https://www.npmjs.com/) | 9+ | Frontend package management |
| [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) | Latest | PDF generation (report generator) |
| [Make](https://www.gnu.org/software/make/) | Any | Build orchestration |
| [GoReleaser](https://goreleaser.com/) | Latest (optional) | Cross-platform release builds |

## Repository Structure

```
breaklist/
├── backend/                 # Go module: web server
├── frontend/breaklist/      # SvelteKit app (npm project)
├── reportGenerator/         # Go module: PDF report CLI
├── weatherIcons/            # Python utility (one-off processing)
├── docs/                    # Documentation
├── go.work                  # Go workspace linking both Go modules
├── makefile                 # Build targets
└── .goreleaser.yaml         # Release configuration
```

> The project uses a **Go workspace** (`go.work`) to link the `backend` and `reportGenerator` modules. This allows IDEs and tools to resolve cross-module references, but the two modules do not import each other.

---

## Development Setup

### 1. Clone the Repository

```sh
git clone git@github.com:alibahmanyar/breaklist.git
cd breaklist
```

### 2. Install Frontend Dependencies

```sh
make setup
# or manually:
cd frontend/breaklist && npm install
```

### 3. Configure Environment

Both the backend and report generator need a `.env` file. You can set up separate ones or share a single file:

**Backend:**
```sh
cp backend/.env.example backend/.env
# Edit backend/.env — set TASKS_LIST_PATH and REMINDERS_LIST_PATH
```

**Report Generator:**
```sh
cp reportGenerator/.env.example reportGenerator/.env
# Edit reportGenerator/.env — set all 5 variables
```

> **Tip:** For development, point both to the same absolute paths for `.list` files so changes from the web UI are reflected in generated reports.

### 4. Run the Backend (Development)

```sh
cd backend
go run .
```

The server starts on [http://localhost:3030](http://localhost:3030). It serves the API and static files.

### 5. Run the Frontend (Development)

```sh
cd frontend/breaklist
npm run dev
```

The SvelteKit dev server starts (typically on port 5173) with hot module replacement. API calls are directed to `http://localhost:3030/api/` in dev mode.

### 6. Run the Report Generator

```sh
cd reportGenerator
go run .
```

This generates `breaklist.pdf` in the `reportGenerator/` directory.

---

## Building

### Full Build

```sh
make          # or: make all
```

This builds all three components into `build/`:

| Output | Source |
|--------|--------|
| `build/webserver` | `backend/main.go` compiled with `-ldflags '-w -s'` (stripped) |
| `build/reportGenerator` | `reportGenerator/main.go` compiled with `-ldflags '-w -s'` |
| `build/static/` | `frontend/breaklist/` built with `npm run build` |
| `build/template.html` | Copied from `reportGenerator/` |
| `build/weathercodes/` | Copied from `reportGenerator/weathercodes/` |
| `build/.env.example` | Copied from `reportGenerator/` |

### Individual Components

```sh
# Backend only
cd backend && go build -o ../build/webserver .

# Report generator only
cd reportGenerator && go build -o ../build/reportGenerator .

# Frontend only
cd frontend/breaklist && npm run build
```

### Clean Build Artifacts

```sh
make clean    # Removes build/ and dist/
```

---

## Testing

### Report Generator Tests

The report generator has unit tests for the cron matching system:

```sh
cd reportGenerator
go test -v ./...
```

**Test coverage:**
- `TestMatchesCronPart` — 13 test cases covering wildcards, intervals, value lists, and mixed patterns
- `TestMatchCronExpression` — 9 test cases covering full 3-field cron expressions against specific dates

### Frontend Linting & Type Checking

```sh
cd frontend/breaklist

# Type checking
npm run check

# Linting
npm run lint

# Code formatting
npm run format
```

---

## Releases

### Creating a Snapshot Release

```sh
make release
# or: goreleaser release --snapshot --clean
```

This creates cross-platform archives in `dist/` for all supported OS/architecture combinations:

| OS | Architectures | Format |
|----|---------------|--------|
| macOS | amd64, arm64, arm, 386 | `.tar.gz` |
| Linux | amd64, arm64, arm, 386 | `.tar.gz` |
| Windows | amd64, arm64, arm, 386 | `.zip` |

Each archive contains:
- `webserver` (or `webserver.exe`)
- `reportGenerator` (or `reportGenerator.exe`)
- `template.html`
- `weathercodes/` (152 icon PNGs)
- `static/` (built frontend)
- `.env.example`

---

## Weather Icons Processing

The `weatherIcons/` directory contains a Python utility for preprocessing weather icons for thermal printer compatibility.

### When to Use

Run this only when you need to add or update weather icons (e.g., if Tomorrow.io adds new weather codes).

### Process

1. Place raw weather icon images in `weatherIcons/raw/`
2. Run the threshold script:
   ```sh
   cd weatherIcons
   python threshold.py
   ```
3. Processed icons appear in `weatherIcons/thresholded/`
4. Copy the processed icons to `reportGenerator/weathercodes/`, naming them `{weatherCode}0.png`

**Python dependencies:** numpy, opencv-python (cv2), matplotlib

### How It Works

The script applies **adaptive Gaussian thresholding** to convert icons to pure black & white, which renders cleanly on thermal printers that can't handle grayscale gradients.

---

## Key Technical Notes

### Shared `getLines()` Function

Both `backend/main.go` and `reportGenerator/main.go` contain an identical `getLines()` function. This is the data contract between the two components — if you change the file format, both must be updated.

```go
func getLines(filename string) ([]string, error) {
    data, err := os.ReadFile(filename)
    sdata := string(data)
    allLines := strings.Split(sdata, "\n")
    var lines []string
    for _, line := range allLines {
        if !strings.HasPrefix(line, "#") && len(line) > 0 {
            lines = append(lines, line)
        }
    }
    return lines, err
}
```

### Frontend API URL Switching

The SvelteKit frontend detects whether it's in dev or production mode:
- **Dev mode:** API calls go to `http://localhost:3030/api/` (separate Go server)
- **Production:** API calls go to `api/` (relative, served by the same Go server)

### Cross-Platform PDF Generation

The report generator detects the OS at runtime:
- **Windows:** Calls `.\wkhtmltopdf.exe` directly
- **macOS/Linux:** Calls `sh -c "wkhtmltopdf ..."` via shell

### Cron Format Differences

The project uses a **3-field cron** (DOM, Month, DOW) instead of the standard 5-field (Minute, Hour, DOM, Month, DOW). This is intentional — reminders are checked once daily at report generation time, not at specific times.

---

## Troubleshooting

### "wkhtmltopdf not found"

Ensure `wkhtmltopdf` is installed and available in your PATH. On Windows, the report generator expects `wkhtmltopdf.exe` in the current working directory.

### Empty weather forecast

- Verify your `TOMORROW_API_KEY` is valid and has remaining API quota
- Check that `LOCATION` is a valid location string (city name or lat/lon)
- Ensure `TIMEZONE` is a valid IANA timezone (e.g., `America/New_York`, `Europe/London`)

### Tasks not syncing between web app and report

Both the backend and report generator must have identical `TASKS_LIST_PATH` and `REMINDERS_LIST_PATH` values in their respective `.env` files, pointing to the **same files**.

### Hacker News section empty

The scraper depends on `https://hackernews.betacat.io/` being available. If the site is down or has changed its HTML structure, the scraper will return empty results.
