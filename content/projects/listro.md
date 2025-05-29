+++
date = '2025-05-29T11:50:58-07:00'
title = 'Listro'
tags = ["project", "in-progress", "v0.0.1"]
+++

## Related Content

- [Source Code](https://github.com/nathantebbs/listro)

## Work in Progress

While key foundational features of Listro have been implemented in `v0.0.1`, the project remains under active development. Features such as persistent state saving are not yet available, and due to limited testing, users may encounter bugs.

## About Listro

When you have a lot to get done, keeping track of tasks can quickly become overwhelming. Since I do most of my work in the terminal using tools like Neovim, I set out to build a terminal user interface (TUI) that fits seamlessly into my existing workflow.

To achieve this, I drew inspiration from other terminal-based tools and prioritized familiarity and efficiency. Core features include:

- **Strong Keyboard Navigation**:
  - `q`, `esc`, or `Ctrl-C` to exit
  - `t` to add a task
  - `l` to add a task list
  - `d` to delete selected tasks

- **File-Based Sessions (Planned)**:
  - JSON/SQLite-based state management, similar to session handling in TMUX
  - Launch from any terminal context into a specified session

- **Cross-Platform Support (Planned)**:
  - Download a platform-specific executable and run from anywhere in the terminal

