#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smbus2
import time

class Lps25hsensor:
    address = 0x5d

    PRESS_OUT_XL = 0x28
    PRESS_OUT_L = 0x29
    PRESS_OUT_H = 0x2A

    def __init__(self, smbus_addr = 1):
        self.bus = smbus2.SMBus(smbus_addr)

    def setup(self):
        """
        lps25hセンサーを初期化する
        """
        try:
            self.bus.write_i2c_block_data(self.address, 0x00, [])
        except OSError as e:
            print(e)

        time.sleep(0.1)

    def read(self):
        """
        lps25hからセンサの値を読み取る
        """
        try:
            self.bus.write_i2c_block_data(self.address, 0x20, [0x90])
        except OSError as e:
            print(e)

        time.sleep(0.05)

        pressure = (
          self.read_i2c_block(self.PRESS_OUT_XL) << 0 |
          self.read_i2c_block(self.PRESS_OUT_L) << 8 |
          self.read_i2c_block(self.PRESS_OUT_H) << 16
        )
        pressure = pressure / 4096

        return {'pressure': pressure}

    def read_i2c_block(self, register):
        """
        ブロックデータを読み込む
        """
        blocks = self.bus.read_i2c_block_data(self.address, register, 1)
        return blocks[0]

        
