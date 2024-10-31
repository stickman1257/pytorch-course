import os
import glob

from typing import Callable, Optional, Sequence, Tuple

import numpy as np
from PIL import Image
import pandas as pd

import torch
from torch import Tensor
from torch.utils.data import Dataset
from torchvision import transforms


class ImagenetDataset(Dataset):
    def __init__(self, image_dir: os.PathLike, class_name: str, transform: Optional[Sequence[Callable]]) -> None:
        super().__init__()
        self.image_dir = image_dir
        self.class_name = class_name
        self.transform = transform

    def __len__(self) -> int:
        return len(self.image_dir)
    
    def __getitem__(self, index: int) -> Tuple:
        image_id = self.image_dir[index]
        target = self.class_name[index].split("-")[0]

        image = Image.open(os.path.join(image_id)).convert('RGB')
        # image = np.array(image, dtype=np.float32)
        if self.transform:
            image = self.transform(image)

        target = torch.tensor(int(target))
                
        return image, target


def get_transform(state: str, image_size: int):
    if state == 'train':
        transform = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
        ])
    else:
        transform = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
        ])
    
    return transform