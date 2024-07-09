from ReadWAVFile import rff, wtf
import numpy as np

def linear_predictor(prev_sample):
    # 线性差分预测器：简单地用前一个样本值作为预测值
    return prev_sample

def quantize(error, quantization_factor, mode='8bit'):  # quantization_factor: 量化因子
    # 量化误差，根据量化因子进行量化
    quantized_error = round(error / quantization_factor)
    if mode == '8bit':
        quantized_error = max(-128, min(quantized_error, 127))  # 限制在8位有符号整数范围内
    elif mode == '4bit':
        quantized_error = max(-8, min(quantized_error, 7))
    elif mode == 'none':
        pass
    return quantized_error

def dpcm_encode(samples, quantization_factor, mode='8bit'):
    # 编码算法
    encoded_data = []
    prev_sample = 0 # 将第0个样本值设为0，也就是说第一个预测值为第一个样本值
    for sample in samples:
        prediction = linear_predictor(prev_sample)
        error = sample - prediction
        quantized_error = quantize(error, quantization_factor, mode)
        encoded_data.append(quantized_error)
        prev_sample = sample
    return np.array(encoded_data)

def dpcm_decode(encoded_data, quantization_factor):
    decoded_data = []  # 初始化解码后的数据
    prev_sample = 2**15
    for quantized_error in encoded_data:
        prediction = linear_predictor(prev_sample)
        decoded_sample = prediction + quantized_error * quantization_factor
        decoded_sample = (decoded_sample & 0xFFFF) - 2**15
        decoded_data.append(decoded_sample)
        prev_sample = decoded_sample + 2**15
    return np.array(decoded_data)


def calculate_snr(original_signal, decoded_signal):
    # 计算信号和噪声的均方根值（RMS）
    # print(original_signal)
    # print(decoded_signal)
    signal_rms = np.sqrt(np.mean(original_signal**2))
    noise_rms = np.sqrt(np.mean((original_signal - decoded_signal)**2))
    # 计算信噪比（SNR）
    snr = 10 * np.log10(signal_rms**2 / noise_rms**2)
    return snr


