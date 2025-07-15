import uvicorn

host="localhost"
port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    uvicorn.run("webhook:app", host=host, port=port, reload=True)