# Discord Bot & Dashboard (Educational Project)

**Status**: In Development (Unfinished)  
**Purpose**: Educational project for learning Python (Flask/FastAPI), Discord bots and full-stack development  
**License**: [MIT](LICENSE) © mk0v4c3v1c  
**Open Source**

## About The Project

This project was created as a learning exercise for:
- Understanding Discord API
- Building REST APIs with FastAPI
- Frontend (React) and backend integration
- Docker containerization
- Modern development workflows

## Getting Started

### Prerequisites
- Docker 20.10+
- Python 3.9+
- Node.js 18+

### Installation
```bash
# 1. Clone the repository
git clone https://github.com/mk0v4c3v1c/discord-bot.git

# 2. Set up environment files (copy from .env.example)
cp .env.example .env
cp .env.db.example .env.db

# 3. Start the application
docker-compose up -d --build