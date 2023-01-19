import inspect
import os
from typing import Dict, Optional

from jina import DocumentArray, Executor, requests
from jina.logging.logger import JinaLogger
import clip
from torch import Tensor
import torch
import time


class SimpleIndexer(Executor):
    """
    A simple indexer that stores all the Document data together in a DocumentArray,
    and can dump to and load from disk.

    To be used as a unified indexer, combining both indexing and searching
    """

    FILE_NAME = 'index.db'

    def __init__(
        self,
        pretrained_model_name_or_path: str = 'ViT-B/32',
        match_args: Optional[Dict] = None,
        table_name: str = 'simple_indexer_table2',
        traversal_right: str = '@r',
        traversal_left: str = '@r',
        device: str = 'cpu',
        **kwargs,
    ):
        """
        Initializer function for the simple indexer

        To specify storage path, use `workspace` attribute in executor `metas`
        :param match_args: the arguments to `DocumentArray`'s match function
        :param table_name: name of the table to work with for the sqlite backend
        :param traversal_right: the default traversal path for the indexer's
        DocumentArray
        :param traversal_left: the default traversal path for the query
        DocumentArray
        """
        super().__init__(**kwargs)

        self._match_args = match_args or {}
        self._index = DocumentArray(
            storage='sqlite',
            config={
                'connection': os.path.join(self.workspace, SimpleIndexer.FILE_NAME),
                'table_name': table_name,
            },
        )  # with customize config
        self.logger = JinaLogger(self.metas.name)
        self.default_traversal_right = traversal_right
        self.default_traversal_left = traversal_left

        self.pretrained_model_name_or_path = pretrained_model_name_or_path

        self.device = device

        model, preprocessor = clip.load(self.pretrained_model_name_or_path, device="cpu")   # No need to load on cuda
        
        self.preprocessor = preprocessor
        self.model = model

    @property
    def table_name(self) -> str:
        return self._index._table_name

    @requests(on='/index')
    def index(
        self,
        docs: 'DocumentArray',
        **kwargs,
    ):
        """All Documents to the DocumentArray
        :param docs: the docs to add
        """
        t1 = time.time()
        if docs:
            self._index.extend(docs)
        t2 = time.time()
        print(t2 - t1)
        print(t1)
        print(t2)

    @requests(on='/search')
    def search(
        self,
        docs: 'DocumentArray',
        parameters: Optional[Dict] = None,
        **kwargs,
    ):
        """Perform a vector similarity search and retrieve the full Document match

        :param docs: the Documents to search with
        :param parameters: the runtime arguments to `DocumentArray`'s match
        function. They overwrite the original match_args arguments.
        """
        match_args = (
            {**self._match_args, **parameters}
            if parameters is not None
            else self._match_args
        )

        traversal_right = parameters.get(
            'traversal_right', self.default_traversal_right
        )
        traversal_left = parameters.get('traversal_left', self.default_traversal_left)
        match_args = SimpleIndexer._filter_match_params(docs, match_args)
        # print('in indexer',docs[traversal_left].embeddings.shape, self._index[traversal_right])
        texts: DocumentArray = docs[traversal_left]
        stored_docs: DocumentArray = self._index[traversal_right]

        doc_ids = parameters.get("doc_ids")
        t1 = time.time()
        with torch.inference_mode():
            t1_00 = time.time()
            for text in texts:
                result = []
                text_features = text.embedding
                text.embedding = None
                for sd in stored_docs:
                    if doc_ids is not None and sd.uri not in doc_ids:
                        continue
                    images_features = sd.embedding
                    print('images len',len(images_features))
                    t1_0 = time.time()
                    tensor_images_features = [Tensor(image_features) for image_features in images_features]
                    t1_1 = time.time()
                    for i, image_features in enumerate(tensor_images_features):
                        tensor = image_features
                        probs = self.score(tensor, text_features)
                        result.append({
                            "score": probs[0][0],
                            "index": i,
                            "uri": sd.uri,
                            "id": sd.id
                        })
                    t1_2 = time.time()
                    print("tensor cost:", t1_1 - t1_0)
                    print("part score cost:", t1_2 - t1_1)
                    print(t1_0)
                    print(t1_1)
                    print(t1_2)
                t2 = time.time()
                print('score cost:', t2 - t1)
                # print(parameters, type(parameters.get("thod")))
                index_list = self.getMultiRange(result,0.1 if parameters.get("thod") is None else parameters.get('thod'), parameters.get("maxCount"))
                t3 = time.time()
                print('range cost:', t3 - t2)
                print(t1)
                print(t1_00)
                print(t2)
                print(t3)
                # print(index_list)
                docArr = DocumentArray.empty(len(index_list))
                for i, doc in enumerate(docArr):
                    doc.tags["leftIndex"] = index_list[i]["leftIndex"]
                    doc.tags["rightIndex"] = index_list[i]["rightIndex"]
                    # print(index_list[i])
                    doc.tags["maxImageScore"] = float(index_list[i]["maxImage"]["score"])
                    doc.tags["uri"] = index_list[i]["maxImage"]["uri"]
                    doc.tags["maxIndex"] = index_list[i]["maxImage"]["index"]
                # print(docArr)
                text.matches = docArr

    def getMultiRange(self, result: list, thod = 0.1, maxCount: int = 10):
        ignore_range = {}
        index_list = []
        maxCount = int(maxCount)
        for i in range(maxCount):
            maxItem = self.getNextMaxItem(result, ignore_range)
            if maxItem is None:
                break
            # print(maxItem["score"])
            leftIndex, rightIndex, maxImage = self.getRange(maxItem, result, thod, ignore_range)
            index_list.append({
                "leftIndex": leftIndex,
                "rightIndex": rightIndex,
                "maxImage": maxImage
            })
            if maxImage["uri"] in ignore_range:
                ignore_range[maxImage["uri"]] += list(range(leftIndex, rightIndex + 1))
            else:
                ignore_range[maxImage["uri"]] = list(range(leftIndex, rightIndex + 1))
        # print(ignore_range)
        return index_list

    def getNextMaxItem(self, result: list, ignore_range):
        maxItem = None
        for item in result:
            if item["uri"] in ignore_range and item["index"] in ignore_range[item["uri"]]:
                continue
            if maxItem is None:
                maxItem = item
            if item["score"] > maxItem["score"]:
                maxItem = item
        return maxItem
    
    def getRange(self, maxItem, result: list, thod = 0.1, ignore_range = None):
        maxImageScore = maxItem["score"]
        maxImageUri = maxItem["uri"]
        maxIndex = maxItem["index"]
        leftIndex = maxIndex
        rightIndex = maxIndex
        has_ignore_range = ignore_range is not None

        d_result = list(filter(lambda x: x["uri"] == maxImageUri, result))
        for i in range(maxIndex):
            prev_index = maxIndex - 1 - i
            if has_ignore_range and prev_index in ignore_range:
                break
            # print(maxImageScore, thod, maxImageUri, maxIndex)
            if d_result[prev_index]["score"] >= maxImageScore - thod:
                leftIndex = prev_index
            else:
                break

        for i in range(maxIndex+1, len(d_result)):
            if has_ignore_range and i in ignore_range:
                break
            if d_result[i]["score"] >= maxImageScore - thod:
                rightIndex = i
            else:
                break
        if (rightIndex - leftIndex) > 60:
            return self.getRange(maxItem, result, thod/2, ignore_range)
        return leftIndex, max(rightIndex, leftIndex + 10), d_result[maxIndex]

    def score(self, image_features, text_features):

        logit_scale = self.model.logit_scale.exp()
        # normalized features
        image_features = image_features / image_features.norm(dim=1, keepdim=True)
        text_features = text_features / text_features.norm(dim=1, keepdim=True)

        # cosine similarity as logits
        
        logits_per_image = logit_scale * image_features @ text_features.t()
        probs = logits_per_image.softmax(dim=-1).cpu().detach().numpy()

        # print(" img Label probs:", probs)
        return probs

    @staticmethod
    def _filter_match_params(docs, match_args):
        # get only those arguments that exist in .match
        args = set(inspect.getfullargspec(docs.match).args)
        args.discard('self')
        match_args = {k: v for k, v in match_args.items() if k in args}
        return match_args

    @requests(on='/delete')
    def delete(self, parameters: Dict, **kwargs):
        """Delete entries from the index by id

        :param parameters: parameters to the request
        """
        deleted_ids = parameters.get('ids', [])
        if len(deleted_ids) == 0:
            return
        del self._index[deleted_ids]

    @requests(on='/update')
    def update(self, docs: DocumentArray, **kwargs):
        """Update doc with the same id, if not present, append into storage

        :param docs: the documents to update
        """

        for doc in docs:
            try:
                self._index[doc.id] = doc
            except IndexError:
                self.logger.warning(
                    f'cannot update doc {doc.id} as it does not exist in storage'
                )

    @requests(on='/fill_embedding')
    def fill_embedding(self, docs: DocumentArray, **kwargs):
        """retrieve embedding of Documents by id

        :param docs: DocumentArray to search with
        """
        for doc in docs:
            doc.embedding = self._index[doc.id].embedding

    @requests(on='/clear')
    def clear(self, **kwargs):
        """clear the database"""
        self._index.clear()
