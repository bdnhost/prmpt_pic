#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="ai_prompt_generator",
    version="0.1.0",
    author="bdnhost",
    author_email="example@example.com",
    description="A tool for creating structured prompts for AI image generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bdnhost/prmpt_pic",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ai-prompt=ai_prompt_generator:main",
            "simple-prompt=simple_prompt_generator:main",
            "cli-prompt=cli_prompt_generator:main",
        ],
    },
)
