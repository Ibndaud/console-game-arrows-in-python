"""Общие настройки тестов: headless-режим pygame до импортов игрового кода."""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame  # noqa: E402

pygame.init()