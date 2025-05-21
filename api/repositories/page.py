from api.models import Page


class PageRepository:
    def get_pages(self, embedding: list[float], top_k: int, min_similarity_score: float) -> list[Page]:
        cursor = Page.objects.aggregate([
            {
                "$vectorSearch": {
                    "index": "page_embedding",
                    "path": "embedding",
                    "queryVector": embedding,
                    "numCandidates": min(top_k * 1000, 10000),
                    "limit": top_k
                }
            },
            {
                "$project": {
                    "title": 1,
                    "url": 1,
                    "similarity_score": {"$meta": "vectorSearchScore"}
                }
            },
            {
                "$match": {
                    "similarity_score": {"$gte": min_similarity_score}
                }
            }
        ])

        return [Page.from_dict(document) for document in cursor]
