Now Spinning
Now Spinning is a Django-based social application for vinyl record collectors to share what they are currently listening to. Users can post "spins" with album details, images, and notes, explore other users’ posts, and browse a shared feed. The application integrates with the Discogs API to provide accurate album information and is designed with a clean, responsive Bootstrap interface.
Features
User Profiles – Customizable profile pages with avatar and cover image uploads
Post a Spin – Add a record you are currently listening to, with optional notes and photos
Discogs API Integration – Search for albums and autofill release details
Responsive Feed – View your own spins or see the latest from all users
Image Uploads – Upload album art, personal photos, or setup shots
Timestamp Formatting – Displays 12-hour AM/PM format in Chicago (CST) time zone
Bootstrap Frontend – Mobile-friendly, clean interface
Authentication – Secure user registration and login system
Tech Stack
Backend: Python, Django
Frontend: Bootstrap, JavaScript
Database: SQLite (development), PostgreSQL (production-ready)
API: Discogs API
Hosting: Render
Installation & Setup
Clone the repository
git clone https://github.com/YOUR_USERNAME/now-spinning.git
cd now-spinning
Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
Install dependencies
pip install -r requirements.txt
Set up environment variables
Create a .env file in the project root:
SECRET_KEY=your_django_secret_key
DEBUG=True
DISCOGS_API_TOKEN=your_discogs_api_token
Run migrations
python manage.py migrate
Create a superuser (optional)
python manage.py createsuperuser
Start the development server
python manage.py runserver
Roadmap
Add likes and comments to spins
Friend system with a friends-only feed
Album and genre tagging
Infinite scroll on the main feed
Deplay using Render