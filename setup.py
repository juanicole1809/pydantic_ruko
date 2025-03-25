from setuptools import setup, find_packages

setup(
    name="mi_agente_ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic-ai",
        "httpx",
        "pydantic",
        "python-dotenv",
        "streamlit",
    ],
) 