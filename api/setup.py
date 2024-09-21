from setuptools import setup, find_packages

requirements = """
fastapi==0.115.0
uvicorn==0.30.6
cassandra-driver==3.29.1
flake8==7.1.1
PyJWT==2.9.0
passlib==1.7.4
bcrypt==4.2.0
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
