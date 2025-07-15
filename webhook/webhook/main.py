import uvicorn

host="mule-r5xs.onrender.com"

if __name__ == "__main__":
    uvicorn.run("webhook:app", host=host, port=8081, reload=True)