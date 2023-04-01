import torch
from data import transforms as T


def updated_DClayer(Irec, masked_kspace, inv_mask, mean, std):
    # mean = mean.unsqueeze(1).unsqueeze(2).unsqueeze(3)
    # std = std.unsqueeze(1).unsqueeze(2).unsqueeze(3)

    network_output = (Irec * std + mean)
    network_output_ks = T.fft2c_new(network_output)

    fwd_output = (network_output_ks * inv_mask) + masked_kspace

    fwd_output = T.ifft2c_new(fwd_output)
    fwd_output = T.complex_abs(fwd_output)
    # int_output = T.ifft2c_new(mult)
    # int_output = T.complex_abs(int_output)

    outUDC = T.normalize(fwd_output, mean, std, eps=1e-11)

    return outUDC


def updated_DClayer_last(Irec, masked_kspace, inv_mask, mean, std):
    mean = mean.unsqueeze(1).unsqueeze(2).unsqueeze(3)
    std = std.unsqueeze(1).unsqueeze(2).unsqueeze(3)

    network_output = (Irec * std + mean)
    network_output_ks = T.fft2c_new(network_output)

    mult = (network_output_ks * inv_mask)

    fwd_output = torch.add(mult, masked_kspace)

    fwd_output = T.ifft2c_new(fwd_output)
    fwd_output = T.complex_abs(fwd_output).unsqueeze(3)
    outUDC = T.normalize(fwd_output, mean, std, eps=1e-11)
    return outUDC

def updated_DClayer_esc(Irec, masked_kspace, inv_mask, mean, std):
    # mean = mean.unsqueeze(1).unsqueeze(2)
    # std = std.unsqueeze(1).unsqueeze(2)
    network_output = Irec * std + mean
    network_output = torch.stack((network_output, torch.zeros(network_output.shape).cuda()), axis=-1)
    network_output_ks = T.fft2c_new(network_output)

    fwd_output = (network_output_ks * inv_mask) + masked_kspace
    fwd_output = T.ifft2c_new(fwd_output)
    fwd_output = T.complex_abs(fwd_output).type(torch.FloatTensor)
    # int_output = T.ifft2c_new(mult)
    # int_output = T.complex_abs(int_output)

    outUDC = T.normalize(fwd_output.cuda(), mean.cuda(), std.cuda(), eps=1e-11)
    # int_output_n = T.normalize(int_output, mean, std, eps=1e-11)

    return outUDC

