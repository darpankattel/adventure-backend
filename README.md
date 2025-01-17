# Adventure Backend API

## About Adventure
Adventure is a project designed to revolutionize the way campaigns are created and managed. With features like AI-powered background image generation and dynamic canvas editing, Adventure empowers users to create visually stunning campaigns with ease. The frontend leverages Next.js and React Konva, while the backend is built with Django, providing a robust API for managing campaigns, background images, and canvas states.

---

## About This Django Project
This Django project forms the backend API for the Adventure platform. It handles user authentication, campaign management, background image storage, and canvas state saving. The backend integrates seamlessly with the frontend, ensuring a smooth user experience.

---

## Setting Up the Project
Follow the steps below to set up the backend on your local machine:

1. Clone the repository:
   ```bash
   git clone https://github.com/darpankattel/adventure-backend.git
   cd adventure-backend
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply the database migrations:
   ```bash
   python manage.py migrate
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

5. Access the API at `http://127.0.0.1:8000/`.

---

## Authentication
For any authenticated routes, the backend uses cookie-based authentication. The cookie key is `auth_token`, which is automatically set upon login. No additional headers are required if you log in through the provided authentication routes.

---

## API References

### 1. **Account**
All routes are prefixed with `/api/account/`.

#### Endpoints

- **Google Authentication**
  ```http
  POST /api/account/google/
  ```
  **Description**: Authenticate using Google Firebase.
  **Request Body**:
  ```json
  {
    "id_token": "string" // Google Firebase ID token
  }
  ```
  **Response**:
  _(Add response details here)_

- **Logout**
  ```http
  POST /api/account/logout/
  ```
  **Description**: Log out the currently authenticated user.

- **User Profile**
  ```http
  GET /api/account/profile/
  ```
  **Description**: Retrieve the profile of the logged-in user.

- **Hardcoded Login**
  ```http
  POST /api/account/hardcoded-login/
  ```
  **Description**: Development-only endpoint for testing API without Google authentication, the token will be generated for hardcoded username `darpan`.

  **Response**:
  _(Add response details here)_

---

### 2. **Campaign**
All routes are prefixed with `/api/campaign/`.

#### Endpoints

- **List Campaigns**
  ```http
  GET /api/campaign/
  ```
  **Description**: Retrieve all campaigns for the authenticated user.

- **Create Campaign**
  ```http
  POST /api/campaign/
  ```
  **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string"
  }
  ```
  **Response**:
  _(Add response details here)_

- **Retrieve Campaign**
  ```http
  GET /api/campaign/:id/
  ```
  **Description**: Retrieve details of a specific campaign.

- **Update Campaign**
  ```http
  PUT /api/campaign/:id/
  ```
  **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string"
  }
  ```
  **Response**:
  _(Add response details here)_

- **Delete Campaign**
  ```http
  DELETE /api/campaign/:id/
  ```
  **Description**: Delete a specific campaign.

---

### 3. **Canvas**
All routes are prefixed with `/api/canvas/`.

#### Endpoints

- **List Canvas States**
  ```http
  GET /api/canvas/
  ```
  **Description**: Retrieve all canvas states for the authenticated user.

- **Create Canvas State**
  ```http
  POST /api/canvas/
  ```
  **Request Body**:
  ```json
  {
    "campaign": "integer", // Campaign ID
    "data": "object" // JSON representation of the canvas
  }
  ```
  **Response**:
  _(Add response details here)_

- **Retrieve Canvas State**
  ```http
  GET /api/canvas/:id/
  ```
  **Description**: Retrieve a specific canvas state.

- **Update Canvas State**
  ```http
  PUT /api/canvas/:id/
  ```
  **Request Body**:
  ```json
  {
    "data": "object" // JSON representation of the canvas
  }
  ```
  **Response**:
  _(Add response details here)_

- **Delete Canvas State**
  ```http
  DELETE /api/canvas/:id/
  ```
  **Description**: Delete a specific canvas state.

---

### 4. **Backgrounds**
All routes are prefixed with `/api/backgrounds/`.

#### Endpoints

- **List Backgrounds**
  ```http
  GET /api/backgrounds/
  ```
  **Description**: Retrieve all backgrounds for the authenticated user.

- **Create Background**
  ```http
  POST /api/backgrounds/
  ```
  **Request Body**:
  ```json
  {
    "campaign": "integer", // Campaign ID
    "image": "file" // Background image file
  }
  ```
  **Response**:
  _(Add response details here)_

- **Retrieve Background**
  ```http
  GET /api/backgrounds/:id/
  ```
  **Description**: Retrieve details of a specific background.

- **Delete Background**
  ```http
  DELETE /api/backgrounds/:id/
  ```
  **Description**: Delete a specific background.

---

## Notes
- Ensure that the user is authenticated before accessing protected endpoints.
- For canvas state, provide the JSON structure as required by the frontend implementation. A typical JSON structure might look like:

```json
{
    "layers": [
        {
            "type": "image",
            "src": "path/to/image.png",
            "x": 10,
            "y": 20,
            "width": 200,
            "height": 100,
            "zIndex": 1
        },
        {
            "type": "text",
            "text": "Hello World",
            "font": "Arial",
            "size": 24,
            "x": 30,
            "y": 50,
            "color": "#000000",
            "zIndex": 2
        },
        {
            "type": "shape",
            "shapeType": "circle",
            "radius": 50,
            "x": 100,
            "y": 100,
            "color": "#FF0000",
            "zIndex": 3
        }
    ]
}
```

