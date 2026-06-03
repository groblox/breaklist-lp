# API Reference

The Breaklist backend provides a REST API for managing tasks and reminders. The server runs on port **3030** by default.

## Base URL

```
http://localhost:3030/api
```

## Authentication

None. The API is designed for local/personal use and does not require authentication.

## Response Format

All API responses follow this envelope format:

```json
{
  "message": "success",
  "data": ["item1", "item2", "..."]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `message` | `string` | Status message (always `"success"` on 200) |
| `data` | `string[]` | Array of items (may be omitted on write operations) |

## Request Format

POST and DELETE requests accept this body format:

```json
{
  "data": ["item1", "item2"]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `data` | `string[]` | Array of items to add or delete |

> **Note:** Unknown fields in the request body will cause a decode error (strict JSON parsing with `DisallowUnknownFields`).

---

## Endpoints

### Tasks

#### `GET /api/task`

Retrieve all current tasks.

**Request:**
```http
GET /api/task HTTP/1.1
Host: localhost:3030
```

**Response:**
```json
{
  "message": "success",
  "data": [
    "Buy groceries",
    "Finish project report",
    "Call dentist"
  ]
}
```

**Behavior:**
- Reads from the file at `TASKS_LIST_PATH`
- Filters out empty lines and lines starting with `#` (comments)
- Returns an empty array if the file is empty or contains only comments

---

#### `POST /api/task`

Add one or more new tasks.

**Request:**
```http
POST /api/task HTTP/1.1
Host: localhost:3030
Content-Type: application/json

{
  "data": ["New task 1", "New task 2"]
}
```

**Response:**
```json
{
  "message": "success"
}
```

**Behavior:**
- Appends tasks to the file at `TASKS_LIST_PATH`
- **Deduplicates**: tasks that already exist in the file are silently skipped
- Each new task is written on its own line, prefixed with `\n`

---

#### `DELETE /api/task`

Delete one or more tasks.

**Request:**
```http
DELETE /api/task HTTP/1.1
Host: localhost:3030
Content-Type: application/json

{
  "data": ["Buy groceries"]
}
```

**Response:**
```json
{
  "message": "success"
}
```

**Behavior:**
- Reads all lines from the tasks file
- Rewrites the entire file, excluding lines that match any item in `data`
- Matching is **exact string comparison** (case-sensitive)

---

### Reminders

#### `GET /api/reminder`

Retrieve all current reminders.

**Request:**
```http
GET /api/reminder HTTP/1.1
Host: localhost:3030
```

**Response:**
```json
{
  "message": "success",
  "data": [
    "* * *|Take vitamins",
    "*/2 * *|Water plants",
    "* * 6,0|Weekend review"
  ]
}
```

**Behavior:**
- Reads from the file at `REMINDERS_LIST_PATH`
- Returns the **raw cron expression** and reminder text (pipe-delimited)
- Filters out empty lines and comments

---

#### `POST /api/reminder`

Add one or more new reminders.

**Request:**
```http
POST /api/reminder HTTP/1.1
Host: localhost:3030
Content-Type: application/json

{
  "data": ["1 * *|Pay rent"]
}
```

**Response:**
```json
{
  "message": "success"
}
```

**Behavior:**
- Appends reminders to `REMINDERS_LIST_PATH`
- Deduplicates against existing reminders (full string match including cron expression)

---

#### `DELETE /api/reminder`

Delete one or more reminders.

**Request:**
```http
DELETE /api/reminder HTTP/1.1
Host: localhost:3030
Content-Type: application/json

{
  "data": ["* * *|Take vitamins"]
}
```

**Response:**
```json
{
  "message": "success"
}
```

**Behavior:**
- Rewrites the reminders file, excluding matched lines
- Must match the **full string** including cron expression and pipe delimiter

---

### Static Files

#### `GET /`

Serves the built SvelteKit frontend from the `./static/` directory.

```http
GET / HTTP/1.1
Host: localhost:3030
```

All requests that don't match an `/api/*` route fall through to the static file server.

---

## Middleware

| Middleware | Purpose |
|------------|---------|
| **Helmet** | Sets security-related HTTP headers (CSP, X-Frame-Options, etc.) |
| **CORS** | Allows cross-origin requests (needed for SvelteKit dev server on different port) |

## Error Handling

- File read errors are returned as Go errors (500 Internal Server Error)
- JSON decode errors are returned from the handler
- File system errors during writes are logged via `log.Error()` but may still return a success response

## Configuration

Environment variables (loaded from `.env` via godotenv):

| Variable | Default | Description |
|----------|---------|-------------|
| `TASKS_LIST_PATH` | `./tasks.list` | Path to the tasks file |
| `REMINDERS_LIST_PATH` | `./reminders.list` | Path to the reminders file |

On startup, the server automatically creates the parent directories and files if they don't exist.
