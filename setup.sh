mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
[theme]\n\
base="dark"\n\
primaryColor="#4bd0ff"\n\
backgroundColor="#233041"\n\
\n\
" > ~/.streamlit/config.toml