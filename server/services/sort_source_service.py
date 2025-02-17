# from typing import List
# from sentence_transformers import SentenceTransformer
# import numpy as np
# import heapq


# class SortSourceService:
#     def __init__(self):
#         self.embedding_model = SentenceTransformer("all-miniLM-L6-v2")

#     def sort_sources(self, query: str, search_results: List[dict]):
#         try:
#             relevant_docs = []
#             query_embedding = self.embedding_model.encode(query)

#             for res in search_results:
#                 res_embedding = self.embedding_model.encode(res["content"])

#                 similarity = float(
#                     np.dot(query_embedding, res_embedding)
#                     / (np.linalg.norm(query_embedding) * np.linalg.norm(res_embedding))
#                 )

#                 res["relevance_score"] = similarity

#                 if similarity > 0.3:
#                     relevant_docs.append(res)

#                 # print(relevant_docs)

#             return sorted(
#                 relevant_docs, key=lambda x: x.get("relevance_score"), reverse=True
#             )
#         except Exception as e:
#             print(e)


from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import numpy as np
from logging import getLogger

logger = getLogger(__name__)


class SortSourceService:
    def __init__(self):
        self.embedding_model = SentenceTransformer("all-miniLM-L6-v2")

    def calculate_similarity(
        self, query_embedding: np.ndarray, content_embedding: np.ndarray
    ) -> float:
        try:
            return float(
                np.dot(query_embedding, content_embedding)
                / (np.linalg.norm(query_embedding) * np.linalg.norm(content_embedding))
            )
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0

    def sort_sources(
        self, query: str, search_results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        try:
            if not search_results:
                logger.warning("Empty search results provided")
                return []

            if not isinstance(search_results, list):
                logger.error(
                    f"search_results must be a list, got {type(search_results)}"
                )
                return []

            relevant_docs = []
            query_embedding = self.embedding_model.encode(query)

            for idx, res in enumerate(search_results):
                try:
                    # Check if the result is None
                    if res is None:
                        # logger.warning(f"Skipping None result at index {idx}")
                        continue

                    if not isinstance(res, dict):
                        # logger.warning(
                        #     f"Skipping non-dictionary result at index {idx}. Got type: {type(res)}"
                        # )
                        continue

                    if "content" not in res:
                        # logger.warning(
                        #     f"Skipping result at index {idx} - missing 'content' key. Available keys: {list(res.keys())}"
                        # )
                        continue

                    # Check if content is None or empty
                    if not res["content"]:
                        # logger.warning(
                        #     f"Skipping result at index {idx} - empty content"
                        # )
                        continue

                    content_embedding = self.embedding_model.encode(res["content"])
                    similarity = self.calculate_similarity(
                        query_embedding, content_embedding
                    )

                    # Create a new dictionary instead of modifying the original
                    doc = res.copy()
                    doc["relevance_score"] = similarity

                    if similarity > 0.3:
                        relevant_docs.append(doc)

                except Exception as e:
                    # logger.error(f"Error processing search result at index {idx}: {e}")
                    # # Print the problematic result for debugging
                    # logger.error(f"Problematic result: {res}")
                    continue

            # Sort and return a new list
            sorted_docs = sorted(
                relevant_docs, key=lambda x: x.get("relevance_score", 0), reverse=True
            )

            logger.info(
                f"Successfully processed {len(sorted_docs)} relevant documents out of {len(search_results)} total results"
            )
            return sorted_docs

        except Exception as e:
            logger.error(f"Error in sort_sources: {e}")
            return []
