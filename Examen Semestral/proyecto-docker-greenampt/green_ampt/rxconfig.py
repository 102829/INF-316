import os
import reflex as rx

config = rx.Config(
    app_name="green_ampt",
    api_url=os.environ.get("API_URL", "http://localhost:3000"),
    backend_port=3000,
    frontend_port=3000,
)
