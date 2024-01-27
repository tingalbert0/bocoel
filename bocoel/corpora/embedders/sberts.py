import typing
from collections.abc import Sequence

from torch import Tensor

from bocoel.corpora.embedders.interfaces import Embedder


class SbertEmbedder(Embedder):
    """
    Sentence-BERT embedder. Uses the sentence_transformers library.
    """

    def __init__(
        self,
        model_name: str = "all-mpnet-base-v2",
        device: str = "cpu",
        batch_size: int = 64,
    ) -> None:
        # Optional dependency.
        from sentence_transformers import SentenceTransformer

        self._sbert = SentenceTransformer(model_name, device=device)

        self._batch_size = batch_size

    @property
    def batch(self) -> int:
        return self._batch_size

    @property
    def dims(self) -> int:
        d = self._sbert.get_sentence_embedding_dimension()
        assert isinstance(d, int)
        return d

    def _encode(self, texts: Sequence[str]) -> Tensor:
        texts = list(texts)

        return typing.cast(
            Tensor,
            self._sbert.encode(texts, batch_size=len(texts), convert_to_tensor=True),
        )
