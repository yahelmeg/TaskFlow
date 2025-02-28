# TaskFlow

TaskFlow is a task management API system that enables users to collaborate by creating, assigning, and tracking tasks across multiple boards.

## Features

- **User Authentication**: Secure login and session management with JWT tokens.
- **Boards**: Users can create and manage multiple boards for organizing tasks of different purposes.
- **Tasks**: Create, update, and track the progress of tasks.
- **Roles**: Dynamic board-specific roles and static user roles encoded in tokens for role based access control.
- **RESTful API**: Well-structured API endpoints for integration.

## Endpoints

### User
- `GET /user` - Get all users  
- `GET /user/{user_id}` - Get a specific user  
- `DELETE /user/{user_id}` - Delete a user  
- `PATCH /user/{user_id}` - Update a user  

### Authentication
- `POST /register` - Register a new user  
- `POST /login` - Authenticate and login and create access and refresh tokens  
- `POST /logout` - Log out the current user  
- `POST /refresh` - Refresh access token using the refresh token

### Board
- `POST /board` - Create a new board  
- `GET /board/{board_id}/users` - Get users of a board  
- `PATCH /board/{board_id}` - Update board details  
- `DELETE /board/{board_id}` - Delete a board  
- `GET /board` - Get all boards  
- `POST /board/{board_id}/invite?user_id={user_id}` - Invite user to board

### Me
- `GET /me/boards` - Get all the active user's boards
- `GET /me/user` - Get the active user's info
- `GET /me/past-invitations` - Get the active user's invitations that were accepted/declined
- `GET /me/pending-invitations` - Get the active user's pending invitations

### Invitations
- `POST /invitation/{invitation_id}/accept` - Accept an invitation 
- `POST /invitation/{invitation_id}/decline` - Decline an invitation 



