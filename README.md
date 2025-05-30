# Bitespeed_Task

This project implements the backend API for Bitespeed’s identity reconciliation task using **Flask** and **PostgreSQL**.

## How to Run Locally

1️) **Clone the repo:**  
git clone https://github.com/Sanket-Kedar/Bitespeed_Task.git <br>
cd Bitespeed_Task <br>
2) Install dependencies:  
\`\`\`pip install -r requirements.txt\`\`\` <br>
3) Set up your \`.env\` file:  
\`\`\`DATABASE_URL=postgresql://username:password@localhost:5432/bitespeed\`\`\` <br>
4) Run the app:  
\`\`\`python app.py\`\`\` <br>

---

## API Endpoint

### POST /identify  
**Request:**  
\`\`\`json
{
  "email": "abc@example.com",
  "phoneNumber": "1234567890"
}
\`\`\`

**Response:**  
json
{
  "contact": {
    "primaryContactId": 1,
    "emails": ["abc@example.com", "def@example.com"],
    "phoneNumbers": ["1234567890", "9876543210"],
    "secondaryContactIds": [2, 3]
  }
}


---

## Deployment
Deployed on **Render**:  
\`\`\`
https://identity-reconciliation-task-y5rw.onrender.com
\`\`\`


