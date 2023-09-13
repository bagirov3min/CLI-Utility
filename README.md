# CLI Utility

Welcome to My CLI Utility Project!

[English](README.md) | [Русский](README-ru.md)

## Description

This application provides user authentication (registration 
and authorization) capabilities through the command-line 
interface (CLI). Users can set their name, email, and password, 
and also have the option to generate a password automatically. 
Upon successful authorization, users gain access to commands for 
adding records to the storage (any text entered through the 
keyboard). When exiting the program (either through a command 
or by closing the window), registration data is saved. However, 
for the next login, users need to authenticate again.

Data Storage: SQLite database.

## Usage

The program can be used to implement services for secure
storage of user-entered texts. This utility uses
user authentication and authorization through the command line
(CLI), and also employs password hashing with
the sha256 algorithm to ensure the security
of password storage.

## Installation

1. Clone the repository: `git clone 
   https://github.com/bagirov3min/CLI-Utility`
2. Navigate to the root directory of your project
3. Run the program by executing the main.py file

## Authors

Name: Emin <br>
Last: Bagirov <br>
GitHub: [@bagirov3min](https://github.com/bagirov3min) <br>
Email: bagirov3min@gmail.com <br>
Telegram: @Emin_pro <br>
