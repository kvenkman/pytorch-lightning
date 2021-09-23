# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Union

from pytorch_lightning.utilities import GradClipAlgorithmType
from pytorch_lightning.utilities.exceptions import MisconfigurationException


class TrainingTricksConnector:
    def __init__(self, trainer):
        self.trainer = trainer

    def on_trainer_init(
        self,
        gradient_clip_val: float,
        gradient_clip_algorithm: str,
        track_grad_norm: Union[int, float, str],
        terminate_on_nan: bool,
    ):

        self.trainer.terminate_on_nan = terminate_on_nan

        # gradient clipping
        if gradient_clip_algorithm not in list(GradClipAlgorithmType):
            raise MisconfigurationException(f"gradient_clip_algorithm should be in {list(GradClipAlgorithmType)}")
        self.trainer.gradient_clip_val = gradient_clip_val
        self.trainer.gradient_clip_algorithm = GradClipAlgorithmType(gradient_clip_algorithm)

        # gradient norm tracking
        if not isinstance(track_grad_norm, (int, float)) and track_grad_norm != "inf":
            raise MisconfigurationException("track_grad_norm can be an int, a float or 'inf' (infinity norm).")
        self.trainer.track_grad_norm = float(track_grad_norm)
