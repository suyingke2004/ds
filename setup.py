from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="deepseek-client",
    version="0.1.0",
    author="DeepSeek Client Developer",
    author_email="example@example.com",
    description="Python client for accessing DeepSeek API with advanced features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/deepseek-client",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
) 