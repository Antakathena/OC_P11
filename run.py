import GUDLFTapp
from GUDLFTapp import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)  # change when debug is done
