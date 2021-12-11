"""App entry point."""
from dashboard import create_app

app = create_app()

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=80) # THis fucking disables the copy function FOR SOME REASON
    app.run(host="127.0.0.1", port=80) # t his is fine tho