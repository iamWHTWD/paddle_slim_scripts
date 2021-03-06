# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"
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
import sys

sys.path.append("../")
import unittest
import paddle
from paddleslim.nas import SANAS, RLNAS
from paddleslim.nas.early_stop import MedianStop
from static_case import StaticCase

steps = 5
epochs = 5


class TestMedianStop(StaticCase):
    def test_median_stop1(self):
        """
        class paddleslim.nas.early_stop.MedianStop(strategy, start_epoch, mode)
        mode='minimize'
        有问题待修复
        :return:
        """
        # config = [('ResNetBlockSpace', {'block_mask': [0]})]
        config = [('ResNetBlockSpace2', {'block_mask': [0]})]
        port = 8773
        rlnas = RLNAS(
            key='lstm',
            configs=config,
            server_addr=("", port),
            is_sync=False,
            is_server=True,
            save_controller=False
        )
        earlystop = MedianStop(rlnas, 2, mode='minimize')
        avg_loss = 1.0
        for step in range(steps):
            status = earlystop.get_status(step, avg_loss, epochs)
            self.assertTrue(status, 'GOOD')

        avg_loss = 0.5
        for step in range(steps):
            status = earlystop.get_status(step, avg_loss, epochs)
            if step < 2:
                self.assertTrue(status, 'GOOD')
            else:
                self.assertTrue(status, 'BAD')


if __name__ == '__main__':
    unittest.main()
