# Reddit User Persona Generator
This project generates a user persona for any Reddit user by analyzing their posts and comments using AI models via OpenRouter.
1. How to Run This Project
Clone or Download the Repository
git clone https://github.com/lakshmipoojithagarikapati09876543/BeyondChats-internship-assignment.git
cd BeyondChats-internship-assignment

Or download and unzip the project.

 2. Install Dependencies
pip install -r requirements.txt

3. Create a `.env` File
Create a file named `.env` in the project root (same folder as `main.py`) with the following content:


REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=your_user_agent_here
REDDIT_USERNAME=your_reddit_username_here
REDDIT_PASSWORD=your_reddit_password_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

> **Note:**
> - Replace the values with your own Reddit and OpenRouter API credentials.
> - **Never share your real keys publicly!**

4. Run the Script

## python main.py <reddit_profile_url>
Example:
python main.py https://www.reddit.com/user/Active-Indication286/


## 📄 Project Structure

- `main.py` — Main script to generate personas.
- `test_reddit.py` — Script to test Reddit API connection.
- `test_env.py` — Script to test environment variable loading.
- `requirements.txt` — Python dependencies.
- `personas/` — Example persona files.


## ⚠️ Security Note
- **Do NOT upload your `.env` file or any real API keys to GitHub.**
- Always keep your credentials private.



## 🙋‍♂️ Need Help?
If you have any issues running the project, please open an issue or contact me through this email.
