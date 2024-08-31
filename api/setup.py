from setuptools import setup, find_packages

requirements = """
fastapi==0.112.2
uvicorn==0.30.6
cassandra-driver==3.29.1
"""

setup(
    name='ai_chat_api',
    version='0.0.1',
    author='<NAME>',
    author_email='<EMAIL>',
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.10'
)
