# Assignment 2

## Intro

You can find stackholder request in another attached file.

## Suggeted API endpoints

- POST /habits — Create habit
- GET /habits — List all habits
- GET /habits/{id} — Get single habit
- PUT /habits/{id} — Update habit
- DELETE /habits/{id} — Delete habit
- POST /habits/{id}/subhabits — Add sub-habit
- POST /habits/{id}/logs — Record progress
- GET /habits/{id}/logs — List logs
- GET /habits/{id}/stats — Get statistics

## Linting/formatting

- Format and lint your code using `ruff`
- Check your static types with `mypy`

You can find configuration for these tools in playground project developed during sessions.
Alternatively you can adopt pyproject.toml form [this](https://github.com/MadViper/nand2tetris-starter-py/blob/main/pyproject.toml) project.

## Grading

We will not grade solutions:
  - without decomposition
  - with needlessly long methods or classes
  - with code duplications
In all these cases you will automatically get 0% so, we sincerely ask you to 
not make a mess of your code and not put us in an awkward position.

- 20%: It is tested!
- 20%: It is easy to change.
- 20%: It demonstrates an understanding of design patterns.
- 20%: It demonstrates an understanding of Restful API and S.O.L.I.D principles.
- 20%: Linting/formatting.

## Disclaimer

We reserve the right to resolve ambiguous requirements (if any) as we see fit just like a real-life stakeholder would. So, do not assume anything, ask for clarifications.


📄 Project Brief: Smart Habit Tracker API

Client: HealthyMe Startup
Project Type: RESTful backend service
Delivery Time: 3 weeks
Individual project

🧭 Background

Our company, HealthyMe, is developing a digital platform that helps people build better daily habits.
We already have a mobile team working on the app interface — now we need a backend service that stores user habits, tracks progress, and provides helpful statistics.

Your job is to design and implement the core API and data layer for the Smart Habit Tracker.

We want the system to be simple to start with, but flexible enough to grow in the future.
New types of habits, new kinds of statistics, and new ways to organize data should be possible later without rewriting everything.

🎯 Goals

The goal is to deliver a working backend that allows:

Managing user habits

Organizing habits into groups or routines

Recording progress over time

Retrieving summaries or streak information

We’ll use your API as the foundation for our upcoming mobile and web clients.

🧩 Core Features
1. Manage Habits

Users should be able to:

Create new habits (like “Drink 8 glasses of water” or “Meditate for 10 minutes”)

View all their habits

Update or delete them when needed

Each habit has:

A name

A short description

A category (e.g., Health, Learning, Productivity)

A type (some habits are yes/no; others measure numbers like pages read or minutes exercised)

A goal or target value (optional)

The date it was created

2. Organize Habits

Many users follow routines that consist of multiple smaller habits.
For example, “Morning Routine” could include “Stretch”, “Meditate”, and “Drink water”.

The system should support this kind of hierarchical structure where habits can contain sub-habits.

3. Track Progress

Every day, users record their progress:

For yes/no habits: whether they did it or not

For measurable habits: how much they did

We should be able to look up a user’s progress for any habit and see how they’re doing over time.

4. Show Statistics

Users love to see how far they’ve come.
We need a simple way to calculate and display:

Total completions or progress

Current streaks (e.g., “5 days in a row!”)

Average performance over time

The system should allow adding new types of summaries or insights later on.

5. Support Different Habit Types

Right now, we only need:

Boolean habits (done / not done)

Numeric habits (count or quantity)

But we plan to introduce others in the future (like time-based or mood-based habits), so your design should make this easy to extend.

🧠 Expectations

We value clarity, organization, and testability.

You should:

Keep the design clean and modular (avoid hard-coding logic that’s hard to change later)

Make sure the system is reliable — it should not break if new features are added

Ensure that everything important is covered by automated tests

Provide a clear starting point for integration with our app team

We don’t expect a fancy interface — just a working API and a well-structured project.