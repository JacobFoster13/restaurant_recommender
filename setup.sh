mkdir -p ~/.streamlit/
echo "[theme]
base = \"dark\"
primaryColor = \"#4bd0ff\"
backgroundColor = \"#233041\"

[server]
headless = true
enableCORS = false
port = $PORT" > .streamlit/config.toml
