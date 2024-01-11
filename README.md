# gkeep-matlistan-sync

This project consists of a Docker Compose setup for synchronizing items from [Google Keep](https://keep.google.com/) to [Matlistan](https://www.matlistan.se). The synchronization will fetch all unchecked items from the specified Google Keep note and add them to the specified Matlistan list. It will run every 45 minutes by default.

## Prerequisites

Make sure you have the following installed before running the project:

-  Docker
-  Docker Compose

## Getting Started

1. Clone the repository to your local machine.

2. Create a file named `.env` in the root directory and provide the necessary environment variables. The required variables are:
    - `MATLISTAN_EMAIL`: The email address associated with your Matlistan account.
    - `MATLISTAN_PASSWORD`: The password for your Matlistan account.
    - `MATLISTAN_LIST_ID`: The ID of the Matlistan list where the items will be added.
    - `GOOGLE_EMAIL`: The email address associated with your Google account.
    - `GOOGLE_PASSWORD`: The password for your Google account.

3. Build and run the Docker containers using Docker Compose:

   ```
   docker-compose up -d
   ```

   This will build the Docker image and start the synchronization process.

4. The synchronization process will run once immediately and then continue to run every 45 minutes.

## Customization

-  To change the synchronization interval, set the `SYNC_INTERVAL` environment variable to the desired number of minutes. The default value is `45`.

## Persistence

-  The state of the Google Keep notes and the authentication token are stored in the `/data` directory within the container. This directory is mapped to the `./data` directory on the host machine.