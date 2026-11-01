# Press Agency 📰

**Press Agency** is a Django-based web application designed as a news management platform. The project enables redactors (authors) to publish and manage news articles, categorize them by topics, and efficiently search and sort content.

---

## 🚀 Key Features

- **Article Management (Newspapers):** Create, update, delete, and view news articles.
- **Flexible Search System (`?q=`):**
  - Search by keywords in article titles and content.
  - Search by author (redactor) first and last names.
  - Search by article topics (`Topics`).
  - Intelligent date-based search (supports exact year, month, or day inputs, e.g., searching for `2026`).
- **Content Sorting (`?sort=`):**
  - Sort by publication date (newest first / oldest first).
  - Sort alphabetically by title (A–Z / Z–A).
  - Sort by topics on redactor profile pages.
- **Secure Sorting Queries:** Uses an `allowed_sort_fields` whitelist to prevent unauthorized or invalid database queries.
- **Performance Optimization:** Optimized database queries using `select_related` and `prefetch_related` to eliminate N+1 query issues.
- **Smooth UX & Navigation:** Automatic smooth scrolling to the `#search-results` section upon filtering or searching, with instant sorting updates on selector change.
- **Interactive Views:**
  - Home page displaying latest news posts.
  - Topic list and individual topic detail pages.
  - Redactor list and detailed author profile pages.
  - Contact form with email sending functionality.

---

## 🛠 Tech Stack

- **Python 3.10+**
- **Django 4.x / 5.x**
- **Bootstrap 5** (UI styling)
- **SQLite** (Development database)
- **JavaScript** (Smooth scrolling & dynamic form interaction)

---
