import re
import json
import random
from typing import List
from pathlib import Path

import torch
import torch.nn as nn

from ai_chat_api.ai_model.nltk_utils import (
    tokenize,
    bag_of_words
)


HERE = Path(__file__).resolve().parent
INTENT_DATA = HERE / "Intent.json"
MODEL_DATA = HERE / "model_data.pth"


with open(INTENT_DATA, "r") as f:
    intents = json.load(f)


class ModelConfig:
    def __init__(
        self,
        model_state: dict,
        input_size: int,
        output_size: int,
        hidden_size: int,
        all_words: List[str],
        tags: List[str],
    ):
        self.model_state = model_state
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.all_words = all_words
        self.tags = tags


class NeuralNetModule(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNetModule, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)

        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)

        return out


class ModelInstance:
    def __init__(
        self,
        model_config: ModelConfig,
        model: NeuralNetModule,
    ):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_config = model_config
        self.model = model
        self.model.load_state_dict(model_config.model_state)
        self.model.eval()

    def extract_name(self, text: str) -> str:
        match = re.search(r"(my name is|i am|i'm)\s+([A-Z][a-z]+)", text, re.IGNORECASE)
        if match:
            return match.group(2)
        return "human"

    def generate_response(self, user_input: str):
        sentence = tokenize(user_input)
        X = bag_of_words(sentence, model_config.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self.device)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)
        tag = model_config.tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() >= 0.75:
            for intent in intents["intents"]:
                if tag == intent["intent"].lower():
                    response = random.choice(intent["responses"])
                    if "<NAME>" in response:
                        name = self.extract_name(user_input)
                        response = response.replace("<NAME>", name)
                    return response
        else:
            return "I'm sorry but I don't understand 😔"


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if device == torch.device("cpu"):
    model_data = torch.load(MODEL_DATA, map_location=torch.device('cpu'))
else:
    model_data = torch.load(MODEL_DATA)

model_config = ModelConfig(**model_data)
model = NeuralNetModule(
    model_config.input_size,
    model_config.hidden_size,
    model_config.output_size
).to(device)

model_instance = ModelInstance(model_config, model)
