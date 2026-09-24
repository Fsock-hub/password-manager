# Password Manager

A console-based password manager with master password protection and full data encryption.
All credentials are stored in an encrypted file and can only be accessed with the correct master password.

## Features

- Master password (SHA-256 hashed, 3 attempts)
- Full encryption of all data using cryptography.fernet
- Add, view, search, and delete password entries
- Clean console interface with screen clearing
- Data stored in passwords.enc, master password hash in master.hash

## Installation

1. Clone the repository:
```bash
   git clone https://github.com/Fsock-hub/password-manager.git
   cd password-manager
```
2. Run the program:
```bash
   python password_manager.py
```
## First Launch

You will be asked to create a master password. Remember it – without it, your data will be unrecoverable.

## File Structure

- password_manager.py - Main application code
- passwords.enc - Encrypted password database (created automatically)
- master.hash - SHA-256 hash of the master password (created on first launch)

> Never share your passwords.enc or master.hash files with anyone.

## Dependencies

- Python 3.10 or higher
- cryptography library

## Example

```bash
Password manager 1.0
 0 - Exit
 1 - Add and save entry data
 2 - Show saved entry data
 3 - Search saved entry data
 4 - Delete saved entry data
 ~> 1
 Enter name of site: ~> github.com 
 Enter login: ~> my_login
 Enter password: ~> password123
 Entry data saved...
```
## Author

Fsock-hub
