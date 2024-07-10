# 🌟 GiveAid Foundation Web App MVP 🌟

Welcome to the GiveAid Foundation Web App MVP! This platform connects generous donors with individuals and organizations in need, making it easy to contribute to meaningful causes. Below, you'll find an overview of the architecture, APIs, data model, user stories, progress, challenges, and more.

## 🏛️ Architecture Overview

The GiveAid Web App features a robust multi-tier architecture:

### Frontend
- **Technologies**: React, Redux, React Router, Axios, Tailwind CSS

### Backend
- **Technologies**: Django, Django REST framework, MySQL

### Payment Gateway
- **Integration**: Paystack

### Web Server
- **Server**: Nginx, serving Django via Gunicorn

### CI/CD and Deployment
- **Tools**: GitHub Actions, Docker

### Monitoring and Logging
- **Tools**: Prometheus, Grafana, ELK Stack

### Architecture Diagram
*Insert Architecture Diagram Here*

## 📡 APIs and Methods

### API Routes for Web Client

- **api/donation**
  - `GET`: Returns a list of donation causes.
  - `POST`: Accepts donation data and processes payment through Paystack.

- **api/user**
  - `POST`: Register a new user.
  - `GET`: Returns user information based on session ID.

- **api/user/donations**
  - `GET`: Returns a list of past donations for the logged-in user.

### Methods for Other Clients

- **DonationService**
  - `def get_donations(cause_id=None)`: Returns a list of donations optionally filtered by cause.
  - `def create_donations(user_id, amount, cause_id)`: Creates a new donation and processes the payment.

### Third-Party APIs

- **Paystack API**
  - `POST /transaction/initialize`: Initializes a new transaction.
  - `GET /transaction/verify/reference`: Verifies the status of a transaction.

## 🗂️ Data Model

### Data Storage Diagram
*Insert Data Model Diagram Here*

## 🎯 User Stories

1. **Compassionate Global Citizen**: "I want an intuitive platform to easily donate and feel fulfilled through my charitable actions."
2. **Socially Responsible Business Owner**: "I need a seamless platform to channel resources towards meaningful causes, facilitating our CSR initiatives."
3. **New User**: "I want to easily register and log in to manage my donations and track my contributions."
4. **Returning User**: "I want to view my past donations to keep track of my charitable contributions and their impact."

## 🎨 Mockups
*Insert Mockups Here*

### Pages to Visualize

- **Landing Page**: Clear CTAs, featured causes overview.
- **Donation Process**: Form to input donation amount, cause selection dropdown.
- **Checkout Page**: Summary of donation details, payment information input, confirmation button.
- **User Onboarding**: Registration and login forms.
- **My Donations Page**: List of past donations with details (date, amount, cause).

## 🚀 Progress

### Progress Rating
**8/10**

### Progress Assessment
This week has been productive, marked by the completion of the frontend. The integration of React, Redux, React Router, Axios, and Tailwind CSS resulted in a fully functional and responsive UI. However, the backend, including Django and MySQL integration, still needs work.

### Completed Components
- **Frontend**: Fully developed and functional as planned.

### Incomplete Components
- **Backend**: Needs additional work on key functionalities and MySQL integration.

## 🛠️ Challenges

### Technical Challenges
The integration of Django with MySQL posed significant challenges, including compatibility issues and database schema migrations. Docker setup for seamless communication between services required meticulous configuration.

### Non-Technical Challenges
Remote team communication and coordination were challenging due to time zone differences. Miscommunications regarding task assignments and priorities occasionally led to delays.

## TEAM
By: [Patrick A. Noblet](https://github.com/thenoblet/), [Temitayo Daisi-Oso](https://github.com/theAstralProgrammer0) and [Lawson Israel Pascal](https://github.com/lawsonlawson)
