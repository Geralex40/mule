import uvicorn
import os

hostin="0.0.0.0"
port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    uvicorn.run("webhook:app", host=hostin, port=port, reload=True)