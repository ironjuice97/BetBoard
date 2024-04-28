import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()  # Ensure this is before accessing environment variables

app, main_blueprint = create_app()

if __name__ == "__main__":
    app.run(debug=True)

