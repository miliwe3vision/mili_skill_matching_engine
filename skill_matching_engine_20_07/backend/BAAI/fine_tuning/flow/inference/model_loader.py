"""
model_loader.py

Loads the fine-tuned BGE model for inference.
"""

from pathlib import Path

from transformers import AutoModel, AutoTokenizer

from fine_tuning.flow.inference.model_loader import ModelLoader

tokenizer, model = ModelLoader.load()

class ModelLoader:

    _model = None
    _tokenizer = None

    @classmethod
    def load(cls):

        if cls._model is not None:
            return cls._tokenizer, cls._model

        # skill_mathing_engine/
        project_root = Path(__file__).resolve().parents[3]

        model_path = (
            project_root
            / "models"
            / "bge_finetuned"
            / "best"
        )

        print(f"Loading model from:\n{model_path}")

        cls._tokenizer = AutoTokenizer.from_pretrained(model_path)

        cls._model = AutoModel.from_pretrained(model_path)

        cls._model.eval()

        print("✓ Model loaded successfully")

        return cls._tokenizer, cls._model