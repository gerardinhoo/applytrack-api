import os

ENABLE_TEST_ENDPOINTS = (
    os.getenv("ENABLE_TEST_ENDPOINTS", "false").lower() == "true"
)