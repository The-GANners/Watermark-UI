import numpy as np
import pywt
import os
from PIL import Image
from scipy.fftpack import dct, idct
from scipy.ndimage import gaussian_filter
from skimage.metrics import peak_signal_noise_ratio as PSNR
import pathlib

# --- CONFIGURATION ---
IMAGE_HOST = r'D:\WatermarkGAN\Unwatermarked_256x256_512x512.png'
IMAGE_WATERMARK = r'D:\WatermarkGAN\Watermark-UI\DWT_DCT_Watermarking\qr.jpg'
HOST_SIZE = 2048
WATERMARK_SIZE =128
MODEL = 'haar'
LEVEL = 1

# --- PATHS ---
os.makedirs('./pictures', exist_ok=True)
os.makedirs('./dataset', exist_ok=True)
os.makedirs('./result', exist_ok=True)
os.makedirs('./attacks', exist_ok=True)

def convert_image(image_name, size):
    # Open as RGB, resize, and save as RGB
    img = Image.open(image_name).convert('RGB').resize((size, size), Image.Resampling.LANCZOS)
    base_name = os.path.basename(image_name)
    img.save(os.path.join('./dataset', base_name))
    image_array = np.array(img, dtype=np.float64)  # shape: (size, size, 3)
    return image_array

def process_coefficients(imArray, model, level):
    # Process each channel separately for RGB
    if imArray.ndim == 3:
        coeffs = [pywt.wavedec2(imArray[..., c], wavelet=model, level=level) for c in range(3)]
        return coeffs
    else:
        return [pywt.wavedec2(imArray, wavelet=model, level=level)]

def apply_dct(image_array):
    # Apply DCT to each channel if RGB
    if image_array.ndim == 3:
        size = image_array.shape[0]
        all_subdct = np.empty_like(image_array)
        for c in range(3):
            for i in range(0, size, 8):
                for j in range(0, size, 8):
                    subpixels = image_array[i:i+8, j:j+8, c]
                    subdct = dct(dct(subpixels.T, norm="ortho").T, norm="ortho")
                    all_subdct[i:i+8, j:j+8, c] = subdct
        return all_subdct
    else:
        size = len(image_array)
        all_subdct = np.empty((size, size))
        for i in range(0, size, 8):
            for j in range(0, size, 8):
                subpixels = image_array[i:i+8, j:j+8]
                subdct = dct(dct(subpixels.T, norm="ortho").T, norm="ortho")
                all_subdct[i:i+8, j:j+8] = subdct
        return all_subdct

def inverse_dct(all_subdct):
    # Inverse DCT for each channel if RGB
    if all_subdct.ndim == 3:
        size = all_subdct.shape[0]
        all_subidct = np.empty_like(all_subdct)
        for c in range(3):
            for i in range(0, size, 8):
                for j in range(0, size, 8):
                    subidct = idct(idct(all_subdct[i:i+8, j:j+8, c].T, norm="ortho").T, norm="ortho")
                    all_subidct[i:i+8, j:j+8, c] = subidct
        return all_subidct
    else:
        size = len(all_subdct)
        all_subidct = np.empty((size, size))
        for i in range(0, size, 8):
            for j in range(0, size, 8):
                subidct = idct(idct(all_subdct[i:i+8, j:j+8].T, norm="ortho").T, norm="ortho")
                all_subidct[i:i+8, j:j+8] = subidct
        return all_subidct

def embed_watermark(watermark_array, orig_image):
    # Embed watermark in each channel if RGB
    if orig_image.ndim == 3 and watermark_array.ndim == 3:
        watermark_flat = watermark_array.reshape(-1, 3)
        ind = 0
        size = orig_image.shape[0]
        for x in range(0, size, 8):
            for y in range(0, size, 8):
                if ind < watermark_flat.shape[0]:
                    for c in range(3):
                        orig_image[x+5][y+5][c] = watermark_flat[ind][c]
                    ind += 1
        return orig_image
    else:
        watermark_flat = watermark_array.ravel()
        ind = 0
        size = len(orig_image)
        for x in range(0, size, 8):
            for y in range(0, size, 8):
                if ind < len(watermark_flat):
                    orig_image[x+5][y+5] = watermark_flat[ind]
                    ind += 1
        return orig_image

def get_watermark(dct_watermarked_coeff, watermark_size):
    # Extract watermark from each channel if RGB
    if dct_watermarked_coeff.ndim == 3:
        subwatermarks = []
        size = dct_watermarked_coeff.shape[0]
        for x in range(0, size, 8):
            for y in range(0, size, 8):
                coeff_slice = dct_watermarked_coeff[x:x+8, y:y+8, :]
                subwatermarks.append([coeff_slice[5][5][c] for c in range(3)])
        watermark = np.array(subwatermarks).reshape(watermark_size, watermark_size, 3)
        return watermark
    else:
        subwatermarks = []
        size = len(dct_watermarked_coeff)
        for x in range(0, size, 8):
            for y in range(0, size, 8):
                coeff_slice = dct_watermarked_coeff[x:x+8, y:y+8]
                subwatermarks.append(coeff_slice[5][5])
        watermark = np.array(subwatermarks).reshape(watermark_size, watermark_size)
        return watermark

def print_image_from_array(image_array, name):
    # Save as RGB if 3 channels
    if image_array.ndim == 3:
        image_array_copy = image_array.clip(0, 255).astype("uint8")
        img = Image.fromarray(image_array_copy, mode='RGB')
    else:
        image_array_copy = image_array.clip(0, 255).astype("uint8")
        img = Image.fromarray(image_array_copy)
    img.save('./result/' + name)

def recover_watermark(image_array, model=MODEL, level=LEVEL):
    # Recover watermark for each channel if RGB
    if image_array.ndim == 3:
        coeffs_watermarked_image = [pywt.wavedec2(image_array[..., c], wavelet=model, level=level) for c in range(3)]
        dct_watermarked_coeff = np.stack([apply_dct(coeffs_watermarked_image[c][0]) for c in range(3)], axis=-1)
        watermark_array = get_watermark(dct_watermarked_coeff, WATERMARK_SIZE)
        return watermark_array
    else:
        coeffs_watermarked_image = process_coefficients(image_array, model, level=level)
        dct_watermarked_coeff = apply_dct(coeffs_watermarked_image[0])
        watermark_array = get_watermark(dct_watermarked_coeff, WATERMARK_SIZE)
        return watermark_array

def w2d_embed(host_image_path, watermark_image_path):
    image_array = convert_image(host_image_path, HOST_SIZE)
    watermark_array = convert_image(watermark_image_path, WATERMARK_SIZE)
    coeffs_image = process_coefficients(image_array, MODEL, level=LEVEL)
    if image_array.ndim == 3:
        dct_array = np.stack([apply_dct(coeffs_image[c][0]) for c in range(3)], axis=-1)
        dct_array = embed_watermark(watermark_array, dct_array)
        for c in range(3):
            coeffs_image[c][0] = inverse_dct(dct_array[..., c])
        image_array_H = np.stack([pywt.waverec2(coeffs_image[c], MODEL) for c in range(3)], axis=-1)
    else:
        dct_array = apply_dct(coeffs_image[0])
        dct_array = embed_watermark(watermark_array, dct_array)
        coeffs_image[0] = inverse_dct(dct_array)
        image_array_H = pywt.waverec2(coeffs_image, MODEL)
    print_image_from_array(image_array_H, 'image_with_watermark.jpg')
    return image_array, image_array_H, watermark_array

def attack_jpeg_compression(image_array, quality):
    # Save as RGB if 3 channels
    if image_array.ndim == 3:
        img = Image.fromarray(np.uint8(image_array.clip(0, 255)), mode='RGB')
    else:
        img = Image.fromarray(np.uint8(image_array.clip(0, 255)))
    attack_path = f'./attacks/jpeg_q{quality}.jpg'
    img.save(attack_path, 'jpeg', quality=quality)
    attacked_img = Image.open(attack_path)
    if image_array.ndim == 3:
        attacked_img = attacked_img.convert('RGB')
        return np.array(attacked_img, dtype=np.float64)
    else:
        attacked_img = attacked_img.convert('L')
        return np.array(attacked_img.getdata()).reshape(image_array.shape)
    
def attack_gaussian_noise(image_array, sigma):
    # Add noise to each channel if RGB
    if image_array.ndim == 3:
        normalized_array = image_array / 255.0
        noise = np.random.normal(0, sigma, image_array.shape)
        attacked_array = normalized_array + noise
        attacked_array = np.clip(attacked_array, 0, 1) * 255.0
        Image.fromarray(np.uint8(attacked_array.clip(0, 255)), mode='RGB').save(f'./attacks/noise_s{sigma:.2f}.jpg')
        return attacked_array
    else:
        normalized_array = image_array / 255.0
        noise = np.random.normal(0, sigma, image_array.shape)
        attacked_array = normalized_array + noise
        attacked_array = np.clip(attacked_array, 0, 1) * 255.0
        Image.fromarray(np.uint8(attacked_array.clip(0, 255))).save(f'./attacks/noise_s{sigma:.2f}.jpg')
        return attacked_array

def attack_gaussian_blur(image_array, sigma):
    # Blur each channel if RGB
    if image_array.ndim == 3:
        attacked_array = np.stack([gaussian_filter(image_array[..., c], sigma=sigma) for c in range(3)], axis=-1)
        Image.fromarray(np.uint8(attacked_array.clip(0, 255)), mode='RGB').save(f'./attacks/blur_s{sigma:.1f}.jpg')
        return attacked_array
    else:
        attacked_array = gaussian_filter(image_array, sigma=sigma)
        Image.fromarray(np.uint8(attacked_array.clip(0, 255))).save(f'./attacks/blur_s{sigma:.1f}.jpg')
        return attacked_array

def measure_psnr(original_host, watermarked_host):
    return PSNR(original_host, watermarked_host, data_range=255)

def measure_ncc(original_wm, recovered_wm):
    W = original_wm.flatten()
    W_prime = recovered_wm.flatten()
    ncc_value = np.corrcoef(W, W_prime)[0, 1]
    return ncc_value

def evaluate_watermarking_scheme():
    print("--- WATERMARKING EVALUATION STARTING ---")
    try:
        original_host_arr, wm_host_arr, original_wm_arr = w2d_embed(IMAGE_HOST, IMAGE_WATERMARK)
    except FileNotFoundError as e:
        print(f"\nFATAL ERROR: {e}")
        print(f"Please ensure '{IMAGE_HOST}' and '{IMAGE_WATERMARK}' are in the current directory.")
        return

    print("\n" + "="*50)
    print("                 IMPERCEPTIBILITY TEST")
    print("="*50)
    psnr_score = measure_psnr(original_host_arr, wm_host_arr)
    print(f"| PSNR (Original vs. Watermarked): {psnr_score:.2f} dB")
    if psnr_score >= 40:
        print("| Conclusion: EXCELLENT imperceptibility (watermark is highly invisible).")
    elif psnr_score >= 30:
        print("| Conclusion: GOOD imperceptibility (watermark is barely noticeable).")
    else:
        print("| Conclusion: POOR imperceptibility (watermark is likely visible).")

    print("\n" + "="*50)
    print("                 ROBUSTNESS TEST (NCC)")
    print("="*50)
    test_results = {}
    recovered_wm_baseline = recover_watermark(wm_host_arr)
    ncc_baseline = measure_ncc(original_wm_arr, recovered_wm_baseline)
    test_results['Baseline'] = ncc_baseline
    print(f"| {'Baseline (No Attack):':<30} | NCC: {ncc_baseline:.4f} | (Should be close to 1.0)")
    print("-" * 50)

    attacks_to_run = {
        'JPEG Q=60': ('jpeg', 60),
        'JPEG Q=30': ('jpeg', 30),
        'Noise S=0.10': ('noise', 0.10),
        'Noise S=0.20': ('noise', 0.20),
        'Blur S=1.0': ('blur', 1.0),
        'Blur S=2.0': ('blur', 2.0),
    }

    for name, (attack_type, strength) in attacks_to_run.items():
        if attack_type == 'jpeg':
            attacked_img_arr = attack_jpeg_compression(wm_host_arr, strength)
        elif attack_type == 'noise':
            attacked_img_arr = attack_gaussian_noise(wm_host_arr, strength)
        elif attack_type == 'blur':
            attacked_img_arr = attack_gaussian_blur(wm_host_arr, strength)
        recovered_wm = recover_watermark(attacked_img_arr)
        ncc_score = measure_ncc(original_wm_arr, recovered_wm)
        test_results[name] = ncc_score
        print(f"| {name:<30} | NCC: {ncc_score:.4f} |")

    average_ncc = np.mean([ncc for name, ncc in test_results.items() if name != 'Baseline'])
    print("-" * 50)
    print(f"| {'Average NCC (Attack):':<30} | NCC: {average_ncc:.4f} |")
    if average_ncc >= 0.8:
        print("| Conclusion: HIGHLY ROBUST (watermark survives most common attacks).")
    elif average_ncc >= 0.6:
        print("| Conclusion: MODERATELY ROBUST (watermark survives light attacks).")
    else:
        print("| Conclusion: POOR ROBUSTNESS (watermark is easily destroyed).")
    print("\n--- EVALUATION COMPLETE ---")

if __name__ == "__main__":
    evaluate_watermarking_scheme()
