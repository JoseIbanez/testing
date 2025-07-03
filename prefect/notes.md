




# Start server

tmux new -s prefect-server
./setup/start-server


# Start worker

tmux new -s prefect-worker
./setup/start-worker


# Deploy 
prefect deploy 01_started.py:main