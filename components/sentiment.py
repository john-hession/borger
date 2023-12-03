from __future__ import annotations

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.engine.recipes.default_recipe import DefaultV1Recipe

from typing import List, Type, Dict, Text, Any, Optional

from rasa.engine.graph import ExecutionContext
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage

from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.constants import TEXT

from rasa.nlu.extractors.extractor import EntityExtractorMixin

from nltk.sentiment.vader import SentimentIntensityAnalyzer


@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.ENTITY_EXTRACTOR, is_trainable=False
)

class SentimentAnalyzer(GraphComponent, EntityExtractorMixin):
   
    """A pre-trained sentiment component"""

    name = "sentiment"
    provides = ["entities"]
    requires = []
    defaults = {}
    language_list = ["en"]

    def __init__(self, component_config: Dict[Text, Any]) -> None:

        self.component_config = component_config

    @classmethod
    def create(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
    ) -> GraphComponent:
        return cls(config)

    def train(self, training_data: TrainingData) -> Resource:
        pass

    def convert_to_rasa(self, entity, value, confidence, text):
        """Convert model output into the Rasa NLU compatible output format."""

        offset_end = len(text) - 1
        entity = {"value": value,
                  "confidence": confidence,
                  "entity": entity,
                  "extractor": "sentiment_extractor",
                  "start": 0,
                  "end": offset_end}

        return entity

    def process(self, messages: List[Message]) -> List[Message]:
        """Retrieve the text message, pass it to the classifier and append the prediction results 
        to the message class."""
        sid = SentimentIntensityAnalyzer()
        for message in messages:
            text = message.get(TEXT)
            res = sid.polarity_scores(text)
            if res['compound'] < -0.25:
                entity = self.convert_to_rasa("user_happy", False, res['compound'], text)
                message.set("entities", [entity], add_to_output=True)
        return messages

    def persist(self, file_name, model_dir):
        """Pass because a pre-trained model is already persisted"""
        pass