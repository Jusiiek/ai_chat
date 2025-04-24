# 🧠 AI Chat API

#### A conversational AI backend powered by a neural network, built with FastAPI and PyTorch.

#### To start the project, follow the description

[📦 API](./api/) – FastAPI routes and logic  
[💻 WEB](./web/) – Frontend client

-----------

## About

The project uses the FastAPI framework for building the API and a React client powered by TypeScript for the frontend.

---------------

#### The model is based on simple yet effective natural language processing (NLP) techniques to understand the user's intent.

🔤 Tokenization

The input sentence is split into individual words (tokens) using NLTK's tokenizer.

-----

🌱 Stemming

Each word is reduced to its root form using a stemming algorithm (e.g., PorterStemmer), allowing the model to generalize over word variations.

-----

🧺 Bag of Words (BoW)

Tokens are converted into a binary vector representing the presence (1.0) or absence (0.0) of known words from a predefined vocabulary (all_words). This vector serves as input to the neural network.

-----

🧠 Model Architecture

The model is a simple Multi-layer Perceptron (MLP) classifier:

Activator: ReLU activation

Output: intent classes with Softmax activation

The model assigns each sentence to an intent defined in the Intent.json file.

