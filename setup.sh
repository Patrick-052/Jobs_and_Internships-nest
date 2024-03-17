#!/usr/bin/env bash
# This script is used to setup the virtual environment for the project

# Activate script path
ACTIVATE_SCRIPT="$VIRTUAL_ENV/bin/activate"

# Redis installation
wget http://download.redis.io/releases/redis-7.2.4.tar.gz
tar xzf redis-7.2.4.tar.gz
cd redis-7.2.4
make

# Modify Redis configuration locally
sed -i "s/^port .*/port 6340/g" redis.conf
sed -i "s/bind .*/bind 127.0.0.1/g" redis.conf

# Start the redis server after installation
nohup ./src/redis-server ./redis.conf >/dev/null 2>&1 &

# Modifying activate env script
# Start the redis server automatically when the virtual environment is activated
echo -e "\n# Starting the redis server\nnohup ./redis-7.2.4/src/redis-server ./redis-7.2.4/redis.conf >/dev/null 2>&1 &" >> "$ACTIVATE_SCRIPT"

# Stop the redis server automatically when the virtual environment is deactivated
sed -i '/^deactivate () {/,/^}$/s/^\(\s*\)\(}\)$/\1    pkill -f .\/redis-7.2.4\/src\/redis-server\n\1\2/' "$VIRTUAL_ENV/bin/activate"
sed -i '/^deactivate () {/,/^}$/s/^\(\s*\)\(}\)$/\1    sleep 1\n\1\2/' "$VIRTUAL_ENV/bin/activate"
