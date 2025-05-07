set -e

# python ./api/build_init_sql.py > ./db/init.sql

# Get the value of __version__ from powermemo_server.__init__
version=$(grep -oE '__version__ *= *"[^"]+"' ./api/powermemo_server/__init__.py | awk -F'"' '{print $2}')
echo "Version: $version"
echo "# Synced from backend ${version}" > ../client/powermemo/core/blob.py
cat ./api/powermemo_server/models/blob.py >> ../client/powermemo/core/blob.py