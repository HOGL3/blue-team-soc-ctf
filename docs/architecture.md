# Architecture & Design Documentation

## System Architecture

```mermaid
graph TB
    subgraph "Browser"
        UI["Blue Team Portal UI<br/>(Django Templates + Bootstrap)"]
    end

    subgraph "Django Application"
        direction TB
        MW["Middleware<br/>(Security, Session, CSRF, Auth)"]
        
        subgraph "Web Views"
            DASH["Dashboard"]
            INC["Incidents"]
            AST["Assets"]
            RPT["Reports"]
            PROF["Profile"]
            NOTIF["Notifications"]
            LOGS["Activity Logs"]
        end

        subgraph "Secure API (v2)"
            V2["REST API<br/>/api/v2/"]
            SWAGGER["Swagger UI<br/>/api/v2/docs/"]
            RBAC["RBAC Permissions"]
        end

        subgraph "Hidden Legacy API (v1)"
            V1["Legacy API<br/>/api/v1/"]
            BAC["Broken Access Control<br/>/api/v1/admin/"]
        end
    end

    subgraph "Data Layer"
        DB["SQLite Database"]
    end

    UI --> MW --> DASH & INC & AST & RPT & PROF & NOTIF & LOGS
    UI --> MW --> V2
    MW --> V1
    V2 --> RBAC --> DB
    V1 --> DB
    DASH & INC & AST & RPT & PROF & NOTIF & LOGS --> DB
```

## Database Entity Relationship Diagram

```mermaid
erDiagram
    User ||--o| UserProfile : has
    User ||--o{ Notification : receives
    User ||--o{ Incident : creates
    User ||--o{ Incident : assigned_to
    User ||--o{ Asset : owns
    User ||--o{ Report : authors
    User ||--o{ ActivityLog : performs
    User ||--o{ Attachment : uploads

    Incident ||--o{ TimelineEvent : contains
    Incident ||--o{ Attachment : has
    Incident ||--o{ Report : linked_to

    UserProfile {
        string employee_id
        string department
        string designation
        string role
        string security_clearance
        string shift
    }

    Incident {
        string incident_id
        string title
        string category
        string severity
        string status
        string source
    }

    Asset {
        string asset_name
        string hostname
        string asset_type
        string ip_address
        string criticality
        string status
    }

    Report {
        string title
        string report_type
        string report_status
    }

    ActivityLog {
        string action_type
        string target_object
        string description
    }
```

## REST API Architecture

```mermaid
graph LR
    subgraph "Secure API — /api/v2/"
        V2_INC["Incidents<br/>CRUD + Filters"]
        V2_AST["Assets<br/>CRUD + Filters"]
        V2_RPT["Reports<br/>CRUD + Filters"]
        V2_PRF["Profiles<br/>CRUD + /me"]
        V2_NOT["Notifications<br/>Read/Unread"]
        V2_LOG["Activity Logs<br/>Read Only"]
        V2_DSH["Dashboard<br/>Aggregated Stats"]
        V2_SRC["Search<br/>Cross-entity"]
        V2_HLT["Health<br/>Public Status"]
    end

    subgraph "Hidden Legacy API — /api/v1/"
        V1_DSH["Dashboard"]
        V1_INC["Incidents"]
        V1_AST["Assets"]
        V1_RPT["Reports"]
        V1_ADM["Admin ⚠️<br/>Broken Access Control"]
        V1_CFG["Config"]
        V1_BKP["Backups"]
        V1_USR["Users"]
        V1_AUD["Audit Logs"]
        V1_MIG["Migration"]
        V1_SVC["Services"]
        V1_SYS["System"]
        V1_HLT["Health"]
    end
```

## Authentication Flow

```mermaid
sequenceDiagram
    actor Player
    participant Portal as Blue Team Portal
    participant Auth as Django Auth
    participant Session as Session Store

    Player->>Portal: GET /dashboard/
    Portal-->>Player: 302 Redirect → /accounts/login/
    Player->>Portal: POST /accounts/login/ (username, password)
    Portal->>Auth: authenticate(username, password)
    Auth-->>Portal: User object
    Portal->>Session: Create session
    Portal-->>Player: 302 Redirect → /dashboard/
    Player->>Portal: GET /dashboard/ (with session cookie)
    Portal-->>Player: 200 OK — Dashboard HTML
```

## Investigation Workflow

```mermaid
flowchart TD
    A["1. Login to SOC Portal"] --> B["2. Review Dashboard"]
    B --> C["3. Notice 'Infrastructure Upgrade Status' widget<br/>Migration at 85%"]
    C --> D["4. Read Incident Reports<br/>References to 'Legacy VPN Gateway'"]
    D --> E["5. Read Draft RCA<br/>Mentions 'Legacy Portal' and 'compatibility mode'"]
    E --> F["6. Check Activity Logs<br/>'Legacy services restarted'"]
    F --> G["7. Deduce: A legacy system still exists"]
    G --> H["8. Enumerate /api/v1/"]
    H --> I["9. Discover /api/v1/admin/<br/>Broken Access Control"]
    I --> J["10. Retrieve the Flag 🏁"]
```

## CTF Attack Path

```mermaid
flowchart LR
    subgraph "Investigation Phase"
        CLUE1["Incident: Legacy VPN<br/>brute force"]
        CLUE2["Report: Draft RCA<br/>mentions Legacy Portal"]
        CLUE3["Dashboard: Migration<br/>85% complete"]
        CLUE4["Audit Log: Legacy<br/>services restarted"]
    end

    subgraph "Discovery Phase"
        ENUM["Enumerate<br/>/api/v1/"]
        FIND["Discover 13<br/>legacy endpoints"]
    end

    subgraph "Exploitation Phase"
        BAC["Access /api/v1/admin/<br/>as any authenticated user"]
        FLAG["Retrieve<br/>LegacyMasterToken"]
    end

    CLUE1 & CLUE2 & CLUE3 & CLUE4 --> ENUM --> FIND --> BAC --> FLAG
```
