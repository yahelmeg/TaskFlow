# TaskFlow

TaskFlow is a task management API system that enables users to collaborate by creating, assigning, and tracking tasks across multiple boards.

## Features

- **User Authentication**: Secure login and session management with JWT tokens.
- **Boards**: Users can create and manage multiple boards for organizing tasks of different purposes.
- **Tasks**: Create, update, and track the progress of tasks.
- **Roles**: Dynamic board-specific roles and static user roles encoded in tokens for role based access control.
- **RESTful API**: Well-structured API endpoints for integration.

## Endpoints

### Users
- `GET /users` - Get all users  
- `GET /users/{user_id}` - Get a specific user  
- `DELETE /users/{user_id}` - Delete a user  
- `PATCH /users/{user_id}` - Update a user  

### Authentication
- `POST /register` - Register a new user  
- `POST /login` - Authenticate and login and create access and refresh tokens  
- `POST /logout` - Log out the current user  
- `POST /refresh` - Refresh access token using the refresh token

### Boards
- `POST /boards` - Create a new board  
- `GET /boards/{board_id}/users` - Get users of a board  
- `PATCH /boards/{board_id}` - Update board details  
- `DELETE /boards/{board_id}` - Delete a board  
- `GET /boards` - Get all boards  


