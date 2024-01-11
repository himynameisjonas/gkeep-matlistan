# gkeep-matlistan-sync

This project is designed to synchronize items from [Google Keep](https://keep.google.com/) to [Matlistan](https://www.matlistan.se). The synchronization process retrieves all unchecked items from a specified Google Keep note and adds them to the designated Matlistan list. By default, the synchronization runs every 45 minutes.

## Prerequisites

Make sure you have the following installed before running the project:

-  Docker
-  Docker Compose

## Getting Started

1. Create a docker-compose.yml file and copy the contents of the [docker-compose.yml](https://github.com/himynameisjonas/gkeep-matlistan/blob/main/docker-compose.yml) file into it.

2. Create a file named `.env` in the root directory and provide the necessary environment variables. The required variables are:
    - `MATLISTAN_EMAIL`: The email address associated with your Matlistan account.
    - `MATLISTAN_PASSWORD`: The password for your Matlistan account.
    - `MATLISTAN_LIST_ID`: The ID of the Matlistan list where the items will be added.
    - `GOOGLE_EMAIL`: The email address associated with your Google account.
    - `GOOGLE_PASSWORD`: The password for your Google account.
    - `KEEP_LIST_ID`: The ID of the Google Keep note where the items will be retrieved from.

3. Run the Docker container using Docker Compose:

   ```
   docker-compose up -d
   ```

   This will build the Docker image and start the synchronization process.

4. The synchronization process will run once immediately and then continue to run every 45 minutes.

## Customization

-  To change the synchronization interval, set the `SYNC_INTERVAL` environment variable to the desired number of minutes. The default value is `45`.

## Persistence

-  The state of the Google Keep notes and the authentication token are stored in the `/data` directory within the container. This directory is mapped to the `./data` directory on the host machine.
