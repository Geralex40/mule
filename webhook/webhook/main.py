import uvicorn
import os

host="localhost"
port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    uvicorn.run("webhook:app", host=host, port=port, reload=True)