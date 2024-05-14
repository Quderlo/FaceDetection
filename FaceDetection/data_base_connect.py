import psycopg2
import secret_settings

try:
    connection = psycopg2.connect(
        host=secret_settings.HOST_DB,
        port=secret_settings.PORT_DB,
        database=secret_settings.NAME_DB,
        user=secret_settings.USER_DB,
        password=secret_settings.PASSWORD_DB,
    )
except psycopg2.Error as ex:
    print(f"Error: {ex}. While connecting to Database or Database not exist.")

except Exception as e:
    print(f"Error: {e}. Unexpected error in Database connect.")

# docker compose -f docker-compose.yml up -d
