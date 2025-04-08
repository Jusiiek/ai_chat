from setuptools import setup, find_packages

requirements = """
fastapi==0.115.0
uvicorn==0.30.6
cassandra-driver==3.29.1
flake8==7.1.1
PyJWT==2.9.0
pytest==8.3.3
pytest-asyncio==0.25.3
pytest-cov==6.0.0
passlib==1.7.4
bcrypt==4.0.1
python-multipart==0.0.20
click==8.1.8
httpcore==1.0.7
httpx==0.28.1
celery==5.5.0
redis==5.2.1
pytest-mock==3.14.0
"""

setup(
    name='ai_chat_api',
    setup_requires=["setuptools_scm"],
    use_scm_version={
        "write_to": "../version.txt",
        "root": "..",
        "relative_to": __file__,
    },
    version='0.0.1',
    author='<NAME>',
    author_email='<EMAIL>',
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.12',
    # all functions @cli.command()
    entry_points={
        "console_scripts": [
            "ai_chat_api_cli = ai_chat_api.cli:cli",
        ]
    },
)
