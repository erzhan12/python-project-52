### Hexlet tests and linter status:
[![Actions Status](https://github.com/erzhan12/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/erzhan12/python-project-52/actions)

### SonarQube
[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=erzhan12_python-project-52)](https://sonarcloud.io/summary/new_code?id=erzhan12_python-project-52)

### Application Demo

[View the deployed application](https://python-project-52-joe4.onrender.com)


### Project Description

# Task Manager

A Django-based task management system that allows users to create, track, and manage tasks with statuses and labels.

## Features

- User authentication and authorization
- Task management (create, read, update, delete)
- Status management for tasks
- Label management for task categorization
- Internationalization support (i18n)
- Responsive design

## Tech Stack

- Python 3.11+
- Django 4.2
- PostgreSQL
- Bootstrap 5

## Project Structure

- `task_manager/` - Main application directory
  - `users/` - User management
  - `tasks/` - Task management
  - `statuses/` - Task status management
  - `labels/` - Task label management
  - `templates/` - HTML templates
  - `locale/` - Translation files
  - `fixtures/` - Initial data

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   make install
   ```
3. Start the application:
   ```bash
   make start
   ```

## Development

- Run tests:
  ```bash
  make test
  ```
- Check code style:
  ```bash
  make lint
  ```
