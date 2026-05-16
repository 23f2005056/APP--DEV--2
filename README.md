# Influencer Engagement & Sponsorship Coordination Platform - V2

## Overview
The Influencer Engagement & Sponsorship Coordination Platform - V2 is a full-stack web application developed using Flask APIs and Vue.js frontend. The platform connects Sponsors and Influencers for managing sponsorship campaigns, ad requests, and collaborations efficiently. It also includes caching, asynchronous batch jobs, role-based access control, and automated reporting features.

---

## Features

### Admin
- Monitor users, campaigns, and ad requests
- Approve sponsor registrations
- Flag inappropriate users or campaigns
- View platform analytics and statistics
- Manage overall platform activities

### Sponsors
- Create, update, and delete campaigns
- Search influencers based on niche and reach
- Send and manage ad requests
- Export campaign details as CSV
- Track campaign performance

### Influencers
- View public campaigns
- Accept or reject ad requests
- Negotiate sponsorship payments
- Update profile information
- Receive daily reminders for pending requests

---

## Tech Stack

### Backend
- Python
- Flask
- Flask REST APIs
- SQLite
- Redis
- Celery

### Frontend
- Vue.js
- Bootstrap
- HTML5
- CSS3
- JavaScript

### Additional Tools
- JWT Authentication / Flask Security
- ChartJS
- Async Background Jobs

---

## Project Structure

```bash
project-root/
│
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── api/
│   ├── tasks/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── views/
│   └── router/
│
├── static/
├── templates/
├── redis/
└── README.md
