"""
embedding_generator.py

Generate embeddings using the fine-tuned BGE model.
"""

import torch
import torch.nn.functional as F

from fine_tuning.flow.inference.model_loader import ModelLoader


class EmbeddingGenerator:

    @staticmethod
    def _mean_pooling(model_output, attention_mask):
        """
        Mean Pooling
        """

        token_embeddings = model_output.last_hidden_state

        input_mask_expanded = (
            attention_mask.unsqueeze(-1)
            .expand(token_embeddings.size())
            .float()
        )

        return torch.sum(
            token_embeddings * input_mask_expanded,
            dim=1
        ) / torch.clamp(
            input_mask_expanded.sum(dim=1),
            min=1e-9
        )

    @staticmethod
    def generate(text: str):

        tokenizer, model = ModelLoader.load()

        encoded_input = tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        )

        with torch.no_grad():

            model_output = model(**encoded_input)

        embedding = EmbeddingGenerator._mean_pooling(
            model_output,
            encoded_input["attention_mask"]
        )

        embedding = F.normalize(
            embedding,
            p=2,
            dim=1
        )

        return embedding.squeeze(0)