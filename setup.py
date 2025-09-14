#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Telegram Video Yuklab Olish Boti uchun sozlash skripti
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="telegram-video-bot",
    version="1.0.0",
    author="N.Damir",
    author_email="nurmurodov.damir@example.com",
    description="Turli platformalardan videolarni yuklab oladigan Telegram boti",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nurmurodov-Damir/telegram_video_bot",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "telegram-video-bot=src.bot:main",
        ],
    },
)