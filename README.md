## Description
Brief description of your project.

## Microservices
1. **User Service**: Handles user-related operations.
2. **Discussion Service**: Manages discussions.
3. **Comment Service**: Manages comments.
4. **Interaction Service**: Handles likes on discussions and comments.

## Database Schema
- **User Table**: user_id, name, email, phone_num, password, created_on
- **Discussion Table**: discussion_id, user_id, title_of_post, text_field, image, hashtags, created_on, total_comments, view_count
- **Comment Table**: comment_id, user_id, discussion_id, text, created_on, parent_comment

## API Documentation
- **User Service**:
  - `POST /signup`: Create a new user.
  - `POST /login`: User login.
  - `PUT /user`: Update user details.
  - `DELETE /user`: Delete user.

- **Discussion Service**:
  - `POST /discussion`: Create a discussion.
  - `PUT /discussion`: Update a discussion.
  - `DELETE /discussion`: Delete a discussion.
  - `GET /discussion`: Get discussions by tag or text.

- **Comment Service**:
  - `POST /comment`: Add a comment.
  - `PUT /comment`: Update a comment.
  - `DELETE /comment`: Delete a comment.

- **Interaction Service**:
  - `POST /like/discussion`: Like/unlike a discussion.
  - `POST /like/comment`: Like/unlike a comment.

## Setup Instructions
1. **Clone the repository**:
    git clone

2. **Make migrations**:   
    python manage.py makemigrations  
    python manage.py migrate

3. Run the server:
    python manage.py runserver


