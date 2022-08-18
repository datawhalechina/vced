from typing import Optional, Tuple, Dict

import torch
from docarray import DocumentArray
from jina import Executor, requests
from jina.logging.logger import JinaLogger
from transformers import CLIPFeatureExtractor, CLIPModel
import numpy as np
import clip
from PIL import Image
import time

class CLIPImageEncoder(Executor):
    """Encode image into embeddings using the CLIP model."""

    def __init__(
        self,
        pretrained_model_name_or_path: str = 'ViT-B/32',
        device: str = 'cpu',
        batch_size: int = 32,
        traversal_paths: str = '@r',
        *args,
        **kwargs,
    ):
        """
        :param pretrained_model_name_or_path: Can be either:
            - A string, the model id of a pretrained CLIP model hosted
                inside a model repo on huggingface.co, e.g., 'openai/clip-vit-base-patch32'
            - A path to a directory containing model weights saved, e.g.,
                ./my_model_directory/
        :param base_feature_extractor: Base feature extractor for images.
            Defaults to ``pretrained_model_name_or_path`` if None
        :param use_default_preprocessing: Whether to use the `base_feature_extractor` on
            images (tensors) before encoding them. If you disable this, you must ensure
            that the images you pass in have the correct format, see the ``encode``
            method for details.
        :param device: Pytorch device to put the model on, e.g. 'cpu', 'cuda', 'cuda:1'
        :param traversal_paths: Default traversal paths for encoding, used if
            the traversal path is not passed as a parameter with the request.
        :param batch_size: Default batch size for encoding, used if the
            batch size is not passed as a parameter with the request.
        """
        super().__init__(*args, **kwargs)
        self.batch_size = batch_size
        self.traversal_paths = traversal_paths
        self.pretrained_model_name_or_path = pretrained_model_name_or_path

        self.logger = JinaLogger(self.__class__.__name__)

        self.device = device

        model, preprocessor = clip.load(self.pretrained_model_name_or_path, device=device)
        
        self.preprocessor = preprocessor
        self.model = model
        # self.model.to(self.device).eval()

    @requests
    def encode(self, docs: DocumentArray, parameters: dict, **kwargs):
        t1 = time.time()
        print('clip_image encode', t1)
        document_batches_generator =  DocumentArray(
            filter(
                lambda x: x is not None,
                docs[parameters.get('traversal_paths', self.traversal_paths)],
            )
        ).batch(batch_size=parameters.get('batch_size', self.batch_size))
        with torch.inference_mode():
            for batch_docs in document_batches_generator:
                print('in for')
                for d in batch_docs:
                    print('in clip image d.uri', d.uri, len(d.chunks))
                    # tensor = self._generate_input_features(tensors_batch)
                    tensors_batch = []
                    for c in d.chunks:
                        if (c.modality == 'image'):
                            image_embedding = self.model.encode_image(self.preprocessor(Image.fromarray(c.tensor)).unsqueeze(0).to(self.device))
                            # tensors_batch.append(image_embedding)
                            tensors_batch.append(np.array(image_embedding).astype('float32'))
                    embedding = tensors_batch
                    # print(np.asarray(Image.open(d.uri)).shape)
                    # image = self.preprocessor(Image.fromarray(np.asarray(Image.open(d.uri)))).unsqueeze(0).to(self.device)
                    # embedding = self.model.encode_image(image)
                    # print(embedding)
                    # embedding = np.array(embedding).astype('float32')
                    # print(embedding)
                    d.embedding = embedding
        t2 = time.time()
        print('clip_image encode end', t2 - t1, t2)
        