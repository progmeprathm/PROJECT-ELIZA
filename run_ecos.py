import uvicorn

if __name__ == "__main__":
    print("Starting ECOS Kernel...")
    uvicorn.run("ecos.api.main:app", host="0.0.0.0", port=8001, reload=True)
