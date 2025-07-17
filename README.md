# [Restaurant Recommender](https://dallas-restaurant-recs-deb42da2fcb0.herokuapp.com/)

## Description
To set up the knowledge base of the application, a Pinecone DB instance is populated using the Google Places Details API using a Jupyter Notebook. Users can then interact with the Python application running on Heroku Cloud to ask for suggestions about Dallas restaurants based on their provided criteria. The users' input is then embedded and compared against the existing embedded queries in the Pinecone DB, retrieving the top three most relevant records. This context is then passed to the OpenAI Chat API to generate a conversational, yet accurate, answer to the users' question. Using a Retrieval Augmented Generation (RAG) architecture allows for the most accurate results to be provided based on current data, while maintaining a conversational interaction.

## Tech Stack & Dependencies
 * Python
 * Streamlit

 * LangChain
 * Pinecone DB
 * MongoDB
 * OpenAI APIs

## Architecture
<img width="1252" height="690" alt="rest_rec_arch" src="https://github.com/user-attachments/assets/38642e12-19b3-44ce-ba41-539b1ac50c9c" />
