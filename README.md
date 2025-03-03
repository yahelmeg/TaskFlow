# TaskFlow

TaskFlow is a task management API system that enables users to collaborate by creating, assigning, and tracking tasks across multiple boards.

## Features

- **User Authentication**: Secure login and session management with JWT tokens.
- **Boards**: Users can create and manage multiple boards for organizing tasks of different purposes.
- **Tasks**: Create, update, and track the progress of tasks.
- **Roles**: Dynamic board-specific roles and static user roles encoded in tokens for role based access control.
- **RESTful API**: Well-structured API endpoints for integration.

## Roles

### Static Role (User-level)
- **Admin**: Can manage all users, boards, and tasks system-wide

### Dynamic Roles (Board-specific)
- **Owner**: Can manage a specific board and its tasks
- **Contributor**: Can create and manage their own tasks on a board
- **Viewer**: Can only view tasks on a board

## Endpoints


### Authentication
- `POST /register` - Register a new user  
- `POST /login` - Authenticate and login and create access and refresh tokens  
- `POST /logout` - Log out the current user  
- `POST /refresh` - Refresh access token using the refresh token

### Board
- `POST /board` - Create a new board
- `GET /board` - Get all boards
- `GET /board/{board_id}/users` - Get users of a board
- `PATCH /board/{board_id}` - Update board details  
- `DELETE /board/{board_id}` - Delete a board  
- `POST /board/{board_id}/invite/{user_id}` - Invite user to board
- `PATCH /board/{board_id}/role/{user_id}` - Change user's role in board

### List  
- `POST /board/{board_id}/list` - Create a new list in a board  
- `GET /board/{board_id}/list` - Get all lists in a board  
- `GET /list/{list_id}` - Get details of a specific list  
- `PATCH /list/{list_id}` - Update list details  
- `DELETE /list/{list_id}` - Delete a list  

### Invitations
- `POST /invitation/{invitation_id}/accept` - Accept an invitation 
- `POST /invitation/{invitation_id}/decline` - Decline an invitation 

### Me
- `GET /me/boards` - Get all the active user's boards
- `GET /me/user` - Get the active user's info
- `PATCH /me/user` - Update the active user's info
- `GET /me/past-invitations` - Get the active user's invitations that were accepted or declined
- `GET /me/pending-invitations` - Get the active user's pending invitations
- 
### User
- `GET /user` - Get all users
- `GET /user/{user_id}` - Get a specific user
- `DELETE /user/{user_id}` - Delete a user
- `PATCH /user/{user_id}` - Update a user


