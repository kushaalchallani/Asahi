# Asahi

<p align="center">

**Small steps. Meaningful connections. A better everyday.**

A mental-wellness and real-life connection platform designed to help people understand how they feel, build positive habits, and take manageable steps towards everyday wellbeing.

</p>

---

## About

Asahi is an open-source mental-wellness application built around a simple idea: understanding how we feel should lead to meaningful actions in everyday life.

Through mood check-ins, personalized missions, and activity insights, Asahi encourages users to reflect on their emotional wellbeing and discover small, achievable ways to engage with the world around them.

Rather than overwhelming users with complicated routines or unrealistic expectations, Asahi focuses on personalized experiences that adapt to how someone feels, their energy levels, and their preferences.

**Asahi isn't about changing your life overnight. It's about making small steps possible.**

## Features

### Mood Check-ins

- Record your current emotional state.
- Add optional personal notes.
- Maintain a history of previous check-ins.
- Track emotional patterns over time.

### Personalized Missions

- Receive personalized real-life activity suggestions.
- Recommendations adapt to mood and energy levels.
- Choose your preferred difficulty.
- Start, complete, or skip missions.
- Provide feedback to improve future recommendations.

### Insights & Analytics

- Visualize check-in activity.
- Explore mood distribution.
- Review emotional trends.
- Understand personal activity patterns.

### History

- Revisit previous check-ins.
- Review personal notes.
- Track completed and skipped missions.
- Explore past activity.

### User Authentication

- Individual user accounts.
- Protected application features.
- User-specific check-ins and mission history.

## Technology Stack

| Component     | Technology |
| ------------- | ---------- |
| Frontend      | React      |
| Language      | TypeScript |
| Build Tool    | Vite       |
| Backend       | Python     |
| API Framework | FastAPI    |
| ORM           | SQLAlchemy |
| Database      | PostgreSQL |
| Migrations    | Alembic    |

## Architecture

Asahi follows a frontend-backend architecture.

```text
                ASAHI
                  |
          React + TypeScript
                  |
              REST API
                  |
             FastAPI
                  |
             SQLAlchemy
                  |
             PostgreSQL
```

The frontend communicates with the backend through REST APIs, while PostgreSQL stores application data.

## Getting Started

Follow these instructions to run Asahi locally.

### Prerequisites

Make sure you have installed:

- Git
- Python
- Node.js and npm
- PostgreSQL

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/<your-repository>.git

cd <your-repository>
```

Replace the repository URL with the actual GitHub repository address.

### 2. Backend Setup

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it:

**Windows:**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your environment variables using `.env.example`.

Make sure PostgreSQL is running and your database is configured.

Run database migrations:

```bash
alembic upgrade head
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Use the actual FastAPI module path if your application entry point differs.

Backend API documentation:

```text
http://localhost:8000/docs
```

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Vite will provide the local development URL in your terminal.

### 4. Environment Configuration

Asahi uses environment variables to configure its backend, database, authentication, and frontend API connection.

Create your local `.env` file from `.env.example`.

Configure the required values according to the variables defined in the project.

**Important:** Never commit real credentials, authentication secrets, database passwords, or private environment files.

## Deployment

Asahi is being prepared for free-tier deployment using the following services.

| Service  | Platform                          | Purpose             |
| -------- | --------------------------------- | ------------------- |
| Frontend | [Vercel](https://vercel.com/)     | React application   |
| Backend  | [Render](https://render.com/)     | FastAPI application |
| Database | [Supabase](https://supabase.com/) | PostgreSQL database |

The deployment configuration will use environment variables to connect the frontend, backend, and database.

Free-tier services may have resource limitations, inactivity policies, and availability restrictions.

## Project Structure

```text
Asahi/
│
├── frontend/
│   └── src/
│       ├── components/
│       ├── ...
│       └── App.tsx
│
├── backend/
│   └── ...
│
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
└── README.md
```

_The structure above illustrates the intended organization. Refer to the repository for the actual current directory structure._

## Open Source

Asahi is being developed as an open-source project.

Contributions, suggestions, bug reports, and improvements are welcome.

If you would like to contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Test your implementation.
5. Submit a pull request.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting contributions.

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community guidelines.

## Privacy & Safety

Asahi is designed to support personal reflection and everyday wellbeing.

- Personal check-ins and notes should remain private.
- Users should only be able to access their own personal data.
- Authentication and authorization protect private application features.
- Sensitive information should never be exposed through logs or public repositories.

Asahi is not a medical application and does not provide medical diagnoses, treatment, or professional mental-health services.

## Roadmap

Some areas of continued development include:

- [ ] Complete application-wide UI/UX refinement.
- [ ] Improve personalized mission recommendations.
- [ ] Expand insights and activity visualizations.
- [ ] Improve responsive layouts.
- [ ] Complete production security and privacy review.
- [ ] Publish the hosted application.
- [ ] Expand contributor documentation.
- [ ] Welcome community contributions.

## License

Asahi is intended to be distributed under the MIT License.

See the [LICENSE](LICENSE) file for details.

---

<p align="center">

**Asahi**

_Small steps can make a meaningful difference._

Built with care.

</p>
