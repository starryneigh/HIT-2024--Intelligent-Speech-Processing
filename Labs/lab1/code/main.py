# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt
from ReadWAVFile import rff, wtf
from dpcm import *

class Main(object):

    def _read_file(self, filename):
        file = rff(filename)
        data = file.getFrameListData()
        self._data = data

    def _dpcm(self, data, q=1, mode='8bit'):
        self._encode_data = dpcm_encode(data, q, mode)
        self._decode_data = dpcm_decode(self._encode_data, q)
        self._snr = calculate_snr(data, self._decode_data)

    def _write_err_file(self, filename):
        wtf(filename, self._encode_data)

    def _write_decode_file(self, filename):
        wtf(filename, self._decode_data)
    
    def _print_snr(self, filename, mode='8bit'):
        string = f'{filename} {mode} snr: {self._snr}'
        print(string)

    def _test_q(self, q_range, mode='8bit', filename='1.wav'):
        q_snr = []
        snr_max = -100
        q_max_idx = 0
        for q in q_range:
            self._dpcm(self._data, q, mode)
            self._print_snr(filename, mode)
            q_snr.append(self._snr)
            if self._snr > snr_max:
                snr_max = self._snr
                q_max_idx = q
        plt.plot(q_range, q_snr)
        # plt.show()
        return q_max_idx
        

    def main(self):
        # 训练量化因子
        # filename_wav = "../corpus/1.wav"
        # self._read_file(filename_wav)
        # x = np.arange(100, 140)
        # q_8bit = self._test_q(x, '8bit')
        # print('8bit q: ', q_8bit)
        # q_4bit = self._test_q(np.arange(1, 40), '4bit')
        # print('4bit q: ', q_4bit)

        # 最终得到的量化因子
        q_8bit = 116
        q_4bit = 1

        # 初始量化因子设为1（也就是不量化）
        # q_8bit = 1
        # q_4bit = 1

        snr_8bit_vec = []
        snr_4bit_vec = []
        for i in range(1, 11):
            filename_wav = f"../corpus/{i}.wav"
            for mode in ['4bit', '8bit']:
                filename_err = f"../out/{i}_{mode}.dpc"
                filename_decode = f"../out/{i}_{mode}.pcm"
                
                self._read_file(filename_wav)
                quantization_factor = q_8bit if mode == '8bit' else q_4bit
                self._dpcm(self._data, quantization_factor, mode)
                
                if mode == '8bit':
                    snr_8bit_vec.append(self._snr)
                elif mode == '4bit':
                    snr_4bit_vec.append(self._snr)
                
                self._print_snr(filename_wav, mode)
                self._write_err_file(filename_err)
                self._write_decode_file(filename_decode)

        snr_8bit_avg = np.mean(snr_8bit_vec)
        print('8bit avg snr: ', snr_8bit_avg)
        snr_4bit_avg = np.mean(snr_4bit_vec)
        print('4bit avg snr: ', snr_4bit_avg)

if __name__ == '__main__':
    Main().main()
