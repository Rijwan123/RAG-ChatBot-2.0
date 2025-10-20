- Create Virtual Environment: python -m venv myenv
- Activate venv : venv/scripts/activate
- pip install -r requirements.txt

-------------------------------------------------------------------------
Note: This error, ConnectionError: [WinError 10061] No connection could be made because the target machine actively refused it, means your FastAPI backend server is not running or is inaccessible. Your Streamlit frontend is trying to connect to the backend at http://127.0.0.1:8000, but there's no server listening on that port.

To fix this, 
you must run the FastAPI backend and Streamlit frontend in two separate terminal windows.

They are two independent applications that need to be started and run concurrently.

1. Start the FastAPI Backend: In one terminal, navigate to your FastAPI server directory and start the server using Uvicorn. The command is likely 'python -m uvicorn main:app --reload'. 
Ensure this terminal remains open and the server is running.

Step and commands :
    1. Go to folder: cd server 
    2. Create Virtual Environment if not created: python -m venv myenv
    3. venv/Scripts/activate
    4. Install all requirements if not done: pip install -r requirements.txt
    5. uvicorn main:app --reload

2. Start the Streamlit Frontend: In a second terminal, navigate to your Streamlit application's directory and run the app with 'streamlit run app.py'.

Once the FastAPI server is active and listening on port 8000, your Streamlit app will be able to connect to it and the error will be resolved.

Step and commands :
  1. cd client
  2. venv/Scripts/activate 
  3. streamlit run app.py