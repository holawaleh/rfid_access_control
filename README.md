# RFID Access Control System

A comprehensive RFID door lock system with a web-based interface for management, built with Flask and MySQL.

## Features

- **User Management**: Registration, login, and role-based access
- **RFID Card Management**: Add, activate/deactivate, and assign cards to users
- **Door Control**: Manage multiple doors with lock/unlock functionality
- **Access Logging**: Complete audit trail of all access attempts
- **Real-time Dashboard**: Overview of system status and recent activity
- **REST API**: Endpoints for RFID scanner integration

## Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL with SQLAlchemy ORM
- **Frontend**: Bootstrap 5, HTML5, JavaScript
- **Authentication**: Flask-Login with bcrypt password hashing
- **Forms**: Flask-WTF with WTForms validation

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rfid_access_control
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL database**
   - Create a MySQL database
   - Run the SQL script in `database_setup.sql`
   - Or let Flask create tables automatically on first run

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

## Configuration

Edit the `.env` file with your settings:

```env
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=rfid_access_control
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

## API Endpoints

### Access Control API
- `POST /api/access` - Check RFID card access

Request body:
```json
{
    "card_uid": "1234567890",
    "door_id": 1
}
```

Response:
```json
{
    "access_granted": true,
    "message": "Access granted",
    "user": "john_doe"
}
```

## Default Credentials

- **Username**: admin
- **Password**: admin123

## Database Schema

### Users
- User accounts with authentication
- Admin role support

### RFID Cards
- Card UID storage
- User assignment
- Active/inactive status
- Usage tracking

### Access Logs
- Complete audit trail
- Timestamp and location tracking
- Success/failure logging

### Doors
- Multiple door support
- Lock status tracking
- Location information

## Hardware Integration

The system is designed to work with RFID readers that can make HTTP requests. Configure your RFID reader to send POST requests to `/api/access` with the card UID.

Example Arduino/ESP32 code structure:
```cpp
// When RFID card is detected
String cardUID = getCardUID();
HTTPClient http;
http.begin("http://your-server:8080/api/access");
http.addHeader("Content-Type", "application/json");
String payload = "{\"card_uid\":\"" + cardUID + "\",\"door_id\":1}";
int httpResponseCode = http.POST(payload);
// Handle response to control door lock
```

## Security Features

- Password hashing with bcrypt
- Session management with Flask-Login
- CSRF protection with Flask-WTF
- SQL injection prevention with SQLAlchemy ORM
- Input validation and sanitization

## Development

To run in development mode:
```bash
export FLASK_ENV=development
python app.py
```

## Production Deployment

1. Set `FLASK_ENV=production` in your environment
2. Use a production WSGI server like Gunicorn
3. Configure a reverse proxy (nginx)
4. Set up SSL/TLS certificates
5. Use environment variables for sensitive configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details