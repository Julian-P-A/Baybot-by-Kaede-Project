# 🚀 Discord Task Management Bot – MVP

**Author:** Julian Camilo Pinzón Ariza  
**Year:** 2025  
**License:** All rights reserved (see license section)

---

## 1️⃣ Objective

This Discord bot allows teams to manage tasks without leaving Discord, integrating:

- Forum-style channels + threads  
- Google Calendar for due dates  
- Automatic notifications  
- Task states: `pending`, `review`, `changes`, `completed`  

It works efficiently without constant processes, reacting only to:

- Human commands  
- Discord events  
- Google Calendar webhooks  

---

## 2️⃣ MVP Scope

From Discord, the bot allows:

- Creating tasks and assigning responsible users  
- Setting a due date  
- Automatically creating a thread for each task  
- Creating an event in Google Calendar  
- Changing task states  
- Notifying the boss when:  
  - An employee marks a task as delivered  
  - A due date passes without closure  
- Checking today’s tasks  

**Administration:**  

- Server owner = automatic Boss  
- The Boss can promote other users to Manager or Boss  
- Employees register automatically when executing any command  

---

## 3️⃣ User Flow (summary)

### 🧠 Create Task
- The Boss executes `/task create`  
- The bot:  
  - Creates a record in the database  
  - Creates a thread in the configured forum  
  - Posts the initial message in the thread  
  - Creates a Google Calendar event and stores the ID  
  - Assigns responsible users  
  - Sets state to `pending`  

### 🏁 Employee delivers
- In the thread, the employee executes `/task complete`  
- The bot:  
  - Changes state → `review`  
  - Notifies the Boss via DM or private channel  
  - Adds a record in `task_history`  

### 🧑‍💼 Boss reviews
- If approved → `completed`  
- If returned → `changes` and assigns a new date  

### ⏰ Overdue
- Google Calendar webhook alerts  
- The bot checks the state and if still `pending` or `changes` → notifies the Boss  

---

## 4️⃣ Roles and Permissions

| Role      | Permissions                                             |
|----------|---------------------------------------------------------|
| Boss     | All commands                                            |
| Manager  | Review, approve, return, view reports                  |
| Employee | Complete task, add notes, check tasks                  |

**Initial Assignment:**

- Owner → Boss  
- Everyone else → Employee  

**Command to promote:**
```bash
/promote @user role
```

## 6️⃣ Database

### Table `users`
| Field       | Type                           |
|------------|--------------------------------|
| id         | PK                             |
| discord_id | string                         |
| server_id  | string                         |
| name       | string                         |
| role       | enum `boss/manager/employee`  |
| created_at | timestamp                      |

### Table `tasks`
| Field           | Type                                      |
|----------------|------------------------------------------|
| id              | PK                                       |
| server_id       | string                                   |
| title           | string                                   |
| state           | enum `pending/review/changes/completed` |
| responsible     | array of discord_id (json)              |
| due_date        | date                                     |
| thread_id       | string                                   |
| google_event_id | string                                   |
| created_by      | discord_id                               |
| created_at      | timestamp                                |
| updated_at      | timestamp                                |

### Table `task_history`
| Field         | Type                                                           |
|---------------|----------------------------------------------------------------|
| id            | PK                                                             |
| task_id       | FK                                                             |
| action        | enum `created/delivered/approved/returned/overdue/note`       |
| executed_by   | discord_id                                                     |
| date          | timestamp                                                      |
| description   | string (optional)                                              |

---

## 7️⃣ Project Structure (Python)

bot/
├─ baybot.py
├─ moderation.py
├─ config.py
├─ cogs/
│ ├─ tasks.py
│ ├─ configuration.py
│ ├─ moderation.py
│ ├─ fun.py
├─ services/
│ ├─ calendar_service.py
│ ├─ discord_service.py
│ ├─ scheduler_service.py
├─ db/
│ ├─ models.py
│ ├─ database.py
├─ utils/
│ ├─ permissions.py
│ ├─ logger.py
└─ requirements.txt

---