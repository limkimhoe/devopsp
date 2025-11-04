from . import app

if __name__ == "__main__":
    # When run directly for development, use Flask's server
    app.run(host="0.0.0.0", debug=app.config.get("DEBUG", False))
