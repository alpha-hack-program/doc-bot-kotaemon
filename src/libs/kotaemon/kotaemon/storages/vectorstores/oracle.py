# kotaemon_app/vectorstores/oracle.py

import os
from typing import Any, Optional, cast

from kotaemon.base import DocumentWithEmbedding
from dotenv import load_dotenv

from .base import LlamaIndexVectorStore

class OracleVectorStore(LlamaIndexVectorStore):
    _li_class = None

    # Load variables from the .env file
    load_dotenv()  # Ensure environment variables are loaded

    oracle_username = os.getenv("ORACLE_USERNAME", "")
    oracle_password = os.getenv("ORACLE_PASSWORD", "")
    oracle_dsn = os.getenv("ORACLE_DSN", "")
    oracle_table = os.getenv("ORACLE_TABLE", "")
    oracle_distance_strategy = os.getenv("ORACLE_DISTANCE_STRATEGY", "COSINE")  # Default to COSINE
    print("-------------------------------- Oracle DSN:", oracle_dsn)

    def _get_li_class(self):
        try:
            from llama_index.vector_stores.oracledb import OraLlamaVS
        except ImportError:
            raise ImportError(
                "Please install the required package: "
                "'pip install llama-index-vector-stores-oracledb'"
            )
        return OraLlamaVS

    def __init__(
        self,
        username: str = oracle_username,
        password: str = oracle_password,
        dsn: str = oracle_dsn,
        table_name: str = oracle_table,
        distance_strategy: Optional[str] = None,  # e.g., 'COSINE', 'DOT_PRODUCT', 'EUCLIDEAN_DISTANCE'
        **kwargs: Any,
    ):
        self._username = username
        self._password = password
        self._dsn = dsn
        self._table_name = table_name
        self._distance_strategy = distance_strategy or self.oracle_distance_strategy
        self._kwargs = kwargs
        self._inited = False
        self._client = None  # Will hold the OraLlamaVS instance

    def _lazy_init(self, dim: Optional[int] = None):
        """
        Lazy initialization of the Oracle Vector Store client.
        """
        if not self._inited:
            from llama_index.vector_stores.oracledb import OraLlamaVS, DistanceStrategy

            # Map distance strategy string to the enum
            distance_map = {
                "COSINE": DistanceStrategy.COSINE,
                "DOT_PRODUCT": DistanceStrategy.DOT_PRODUCT,
                "EUCLIDEAN_DISTANCE": DistanceStrategy.EUCLIDEAN_DISTANCE,
            }
            distance = distance_map.get(self._distance_strategy.upper(), DistanceStrategy.COSINE)

            self._client = OraLlamaVS(
                username=self._username,
                password=self._password,
                dsn=self._dsn,
                table_name=self._table_name,
                distance_strategy=distance,
                **self._kwargs,
            )
            self._inited = True

    def add(
        self,
        embeddings: list[list[float]] | list[DocumentWithEmbedding],
        metadatas: Optional[list[dict]] = None,
        ids: Optional[list[str]] = None,
    ):
        """
        Adds embeddings to the Oracle Vector Store.
        """
        try:
            print("-------------------------------- Adding embeddings to Oracle Vector Store...")
            if not self._inited:
                if isinstance(embeddings[0], list):
                    dim = len(embeddings[0])
                else:
                    dim = len(embeddings[0].embedding)
                self._lazy_init(dim)

            return self._client.add(
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids,
            )
            print("-------------------------------- Embeddings added successfully to Oracle Vector Store.")
        except Exception as e:
            print(f"Error adding embeddings: {e}")
            raise

    def query(
        self,
        embedding: list[float],
        top_k: int = 1,
        ids: Optional[list[str]] = None,
        **kwargs,
    ) -> tuple[list[list[float]], list[float], list[str]]:
        """
        Queries the Oracle Vector Store for similar embeddings.
        """
        try:
            print("-------------------------------- Querying embeddings from Oracle Vector Store...")
            if not self._inited:
                self._lazy_init(len(embedding))

            result = self._client.query(
                embedding=embedding,
                top_k=top_k,
                ids=ids,
                **kwargs,
            )

            # Assuming result has attributes: embeddings, distances, ids
            return (result.embeddings, result.distances, result.ids)
        except Exception as e:
            print(f"Error querying embeddings: {e}")
            raise

    def delete(self, ids: list[str], **kwargs):
        """
        Deletes embeddings from the Oracle Vector Store based on IDs.
        """
        try:
            if not self._inited:
                self._lazy_init()

            self._client.delete(ids=ids, **kwargs)
        except Exception as e:
            print(f"Error deleting embeddings: {e}")
            raise

    def drop(self):
        """
        Drops the entire Oracle Vector Store collection/table.
        """
        try:
            if not self._inited:
                self._lazy_init()

            self._client.drop_collection()
        except Exception as e:
            print(f"Error dropping collection: {e}")
            raise

    def count(self) -> int:
        """
        Returns the count of embeddings in the Oracle Vector Store.
        """
        try:
            if not self._inited:
                self._lazy_init()
            return self._client.count()
        except Exception as e:
            print(f"Error counting embeddings: {e}")
            return 0

    def __persist_flow__(self):
        """
        Returns the configuration needed to persist the state.
        """
        return {
            "username": self._username,
            "password": self._password,
            "dsn": self._dsn,
            "table_name": self._table_name,
            "distance_strategy": self._distance_strategy,
            **self._kwargs,
        }
