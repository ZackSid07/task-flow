# taskflow-Abdullah_Al_Galib

# Task-Flow

## Project Overview
Task-Flow is a single-page, mobile-responsive Task Manager application. It allows users to quickly add, edit, toggle, and delete tasks dynamically, providing a seamless user experience.

## Tech Stack
* **Backend:** FastAPI
* **Database:** SQLite
* **Frontend:** React initialized with Vite

## Prerequisites
* **Python 3.x**
* **Node.js**

## Backend Setup
1. Navigate to the backend folder:
   ```bash
   cd task-flow/backend
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on the provided example:
   ```bash
   cp .env.example .env
   ```
4. Initialize the SQLite database:
   ```bash
   python src/models/setup_db.py
   ```
5. Run the FastAPI development server:
   ```bash
   uvicorn app:app --reload
   ```

## Frontend Setup
1. Navigate to the frontend folder:
   ```bash
   cd task-flow/frontend
   ```
2. Install the frontend dependencies:
   ```bash
   npm install
   ```
3. Run the Vite development server:
   ```bash
   npm run dev
   ```

## AI Acknowledgement
*An AI coding assistant was used to help structure the boilerplate and guide the development process, as per the assignment rules.*
