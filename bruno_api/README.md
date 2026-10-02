# Bruno API Collection & Automated Test Suite

A modular, role-based [Bruno](https://www.usebruno.com/) collection covering all APIs in the Django REST backend, including system integrity tests, variable chaining, and environment-based secret management.

---

## Architecture & Hierarchy

The collection is organized using a strict hierarchical design:
- **Parent Folders**: Role-specific (`01-Guest`, `02-User`, `03-Admin`)
- **Subfolders**: Feature-specific (`Health`, `OTP`, `Auth`, `Notifications`, `Diagnostics`)
- **Requests**: Modular `.bru` files with built-in Chai `expect` tests and documentation
- **Folder Settings**: Each folder and subfolder utilizes `folder.bru` for role-specific headers and variable scoping.

```
bruno_api/
├── bruno.json                      # Collection manifest
├── README.md                       # Complete guide & documentation
├── environments/                   # Global environment profiles
│   ├── Development.bru             # Local host environment (http://127.0.0.1:8000)
│   ├── Local-Docker.bru            # Docker compose environment (http://localhost:8080)
│   └── Production.bru              # Production environment
├── secrets/                        # Git-ignored secrets repository
│   ├── secrets.example.env         # Committed dummy data template
│   └── development.secrets.env     # Local sensitive variables (git-ignored)
├── 01-Guest/                       # Public & unauthenticated endpoints
│   ├── folder.bru                  # Guest variables (guestIdentifier, guestPassword, etc.)
│   ├── 01-Health/
│   │   ├── folder.bru
│   │   ├── Check System Health.bru
│   │   └── Get Diagnostics Dashboard.bru
│   ├── 02-OTP/
│   │   ├── folder.bru
│   │   ├── Request OTP - Registration.bru
│   │   ├── Request OTP - Password Reset.bru
│   │   ├── Request OTP - Invalid Purpose (Validation Test).bru
│   │   └── Request OTP - Missing Identifier (Validation Test).bru
│   └── 03-Auth/
│       ├── folder.bru
│       ├── Register New User.bru
│       ├── Register - Duplicate Email (Validation Test).bru
│       ├── Register - Invalid OTP (Validation Test).bru
│       ├── Login User.bru
│       ├── Login - Invalid Credentials (Validation Test).bru
│       ├── Refresh JWT Token.bru
│       ├── Verify JWT Token.bru
│       └── Reset Password via OTP.bru
├── 02-User/                        # Authenticated Member endpoints
│   ├── folder.bru                  # Bearer token auth header & user credentials
│   ├── 01-Auth/
│   │   ├── folder.bru
│   │   ├── Get Current User Profile.bru
│   │   ├── Change Password.bru
│   │   ├── Change Password - Wrong Old Password (Validation Test).bru
│   │   └── Logout User.bru
│   ├── 02-Notifications/
│   │   ├── folder.bru
│   │   ├── List Notifications (Paginated).bru
│   │   ├── Get Unread Notification Count.bru
│   │   ├── Mark Single Notification As Read.bru
│   │   ├── Mark All Notifications As Read.bru
│   │   └── Mark Non-Existent Notification As Read (404 Test).bru
│   └── 03-OTP/
│       ├── folder.bru
│       └── Request OTP - Change Email.bru
└── 03-Admin/                       # Privileged / Staff endpoints
    ├── folder.bru                  # Admin Bearer token auth header & admin credentials
    ├── 01-Diagnostics/
    │   ├── folder.bru
    │   ├── Admin Health Status.bru
    │   └── Developer Diagnostic Report.bru
    └── 02-Auth/
        ├── folder.bru
        ├── Admin Login.bru
        └── Verify Admin Profile.bru
```

---

## Environments & Switching

Choose an active environment directly in the Bruno UI (top-right dropdown) or via Bruno CLI:

| Environment | Base URL | API Prefix | Description |
|---|---|---|---|
| **Development** | `http://127.0.0.1:8000` | `/v1` | Standard local Python runtime |
| **Local-Docker** | `http://localhost:8080` | `/v1` | Local containerized Docker compose stack |
| **Production** | `https://api.example.com` | `/v1` | Production deployment URL |

---

## Secrets Management

Secrets are isolated from regular environment files and never committed to Git:
1. `bruno_api/secrets/secrets.example.env` contains dummy data with instructions.
2. Anyone cloning the repository copies this file:
   ```bash
   cp bruno_api/secrets/secrets.example.env bruno_api/secrets/development.secrets.env
   ```
3. Populate your actual local secrets in `development.secrets.env`.
4. Git ignores all `bruno_api/secrets/*.env` files while preserving `secrets.example.env`.

---

## Request Chaining & Dynamic Variables

The collection automatically chains requests to make workflows seamless:
- Calling **`Login User`** automatically saves `accessToken` and `refreshToken` in collection variables.
- Subsequent calls under **`02-User`** automatically inherit `Authorization: Bearer {{accessToken}}` from `02-User/folder.bru`.
- Calling **`List Notifications`** dynamically extracts the first item's ID into `notificationId` for subsequent `Mark Single Notification As Read` tests.
- Calling **`Admin Login`** stores `adminAccessToken` which is automatically inherited by all endpoints under `03-Admin`.

---

## Automated Test Coverage

Every single `.bru` file contains automated Chai `expect` tests:
- **Status codes**: Verifies HTTP 200, 201, 400, 401, 404, 503.
- **Unified Envelope**: Verifies `{ "success": boolean, "message": string, "data": ..., "errors": ... }`.
- **Schema & Data Types**: Verifies properties, array lengths, email regex, and numeric types.
- **Negative & Security Cases**: Verifies invalid credentials, malformed OTPs, duplicate emails, unauthorized access, and expired/blacklisted tokens.

---

## Running with Bruno CLI (`bru`)

You can run the entire collection or specific folders via the command line:

```bash
# Install Bruno CLI globally
npm install -g @usebruno/cli

# Run the entire collection against Development
bru run bruno_api --env Development

# Run only the Guest role folder
bru run bruno_api/01-Guest --env Development

# Run only the User role folder
bru run bruno_api/02-User --env Development
```
