# Supabase to MongoDB Replicator

Hey there! This tool helps you keep your MongoDB data in sync with Supabase's PostgreSQL database in real-time. It's like having a bridge that automatically copies changes from MongoDB to Supabase as they happen.

## What It Does (The Output)

Once set up, this replicator creates tables in your Supabase database that mirror your MongoDB collections. Every time something changes in MongoDB—like adding, updating, or deleting a document—it gets reflected in Supabase right away. You'll see structured rows with flattened data, operation details, timestamps, and the original JSON for flexibility.

## The Goal

The main aim is to make MongoDB data accessible in Supabase without manual syncing. This is great if you're building apps that need the power of both databases: MongoDB for flexible schemas and Supabase for relational queries, real-time features, and easy integrations.

## How It Works (In Simple Terms)

Imagine MongoDB as a busy warehouse where documents are constantly being added or changed. This tool sets up watchers (called change streams) on each collection. When a change happens, it grabs the data, flattens any nested structures to fit neatly into PostgreSQL tables, and pushes it to Supabase. It even creates the tables automatically if they don't exist, and keeps them updated as your data evolves. Everything runs in parallel for speed, and it remembers where it left off if there's an interruption.

## Why It Helps Enterprises

For businesses, this means smoother data flows between systems without downtime or manual work. You can use Supabase's tools for analytics, dashboards, or APIs on data that's originally in MongoDB. It's scalable, reliable, and reduces the hassle of data migration—perfect for teams handling large volumes of changing data across different platforms.

## Prerequisites

- Python 3.8 or newer
- A MongoDB setup with change streams turned on
- A Supabase account with a PostgreSQL database

## Installation

1. Grab the project files.
2. Install the needed packages:
   ```
   pip install pymongo python-dotenv psycopg2-binary
   ```

## Configuration

Set up a `.env` file in the project root with these details (replace with your actual values):

```
MONGO_URI=mongodb://localhost:27017
MONGO_DB=your_database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
SUPABASE_REST_URL=https://your-project.supabase.co/rest/v1
SUPABASE_SQL_URL=postgresql://postgres:password@db.your-project.supabase.co:5432/postgres
PG_USER=postgres
PG_PASSWORD=password
PG_HOST=db.your-project.supabase.co
PG_PORT=5432
PG_DATABASE=postgres
LOG_LEVEL=INFO
BATCH_SIZE=1
```

## Usage

Fire it up with:

```
python -m supabase-to-mongo.main
```

It'll kick off watchers for all your MongoDB collections and start syncing changes to Supabase tables automatically.

## Key Features

- Handles multiple collections at once with parallel processing.
- Picks up right where it left off after restarts (thanks to resume tokens).
- Figures out and builds table schemas on the fly.
- Logs everything so you can keep an eye on what's happening.
