# 🛡️ Watermark-UI: Standalone Batch Image Watermarking Suite

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7%2B-3776AB.svg?logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-FFB300.svg?logo=python)
![DWT-DCT](https://img.shields.io/badge/Invisible%20Watermarking-DWT--DCT-blueviolet)
![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)

</div>

---

## 📖 Overview

**Watermark-UI** is a powerful, user-friendly desktop application for batch watermarking images with both **visible** and **invisible** (DWT-DCT) watermarks.  
It supports image and text watermarks, robust invisible watermarking, real-time previews, and batch processing—all in a simple GUI.

---

## 🏗️ Features

### 👁️‍🗨️ Visible Watermarking

- **Add visible watermarks** (image or text) to multiple images at once.
- **Customizable positioning:** Top-Left, Top-Right, Bottom-Left, Bottom-Right, Center.
- **Adjustable opacity:** 0–100% for subtle or bold watermarks.
- **Auto-resize & scale:** Watermark scales to fit each image, or use original size.
- **Rotation:** Rotate watermark to any angle.
- **Padding:** Fine-tune placement with pixel or percentage padding.
- **Batch processing:** Watermark entire folders in one go.
- **Real-time preview:** See exactly how your watermark will look before applying.
- **Batch download:** Save all watermarked images with one click.

---

### 🕵️‍♂️ Invisible Watermarking (DWT-DCT)

- **Embed robust, imperceptible watermarks** using a hybrid Discrete Wavelet Transform + Discrete Cosine Transform (DWT-DCT) algorithm.
- **Supports both text and image watermarks** for invisible embedding.
- **Binarized and adaptively resized:** Watermark is automatically resized and binarized to match host image capacity.
- **High redundancy embedding:** Ensures watermark survives compression, noise, and blur.
- **Attack simulation:** Test watermark robustness against JPEG compression, noise, and blur.
- **Extraction & verification:** Extract the embedded binary pattern and verify against the original watermark.
- **All metrics displayed:** PSNR (imperceptibility), NCC (robustness), and attack results shown in the UI.
- **Batch invisible watermarking:** Apply invisible watermarks to multiple images at once.

---

## 🖥️ How It Works

### 👁️ Visible Watermarking

- **Description:**  
  Add a visible watermark (image or text) to your images in bulk, with full control over position, opacity, scale, rotation, and padding.
- **Implementation:**  
  - Watermark is composited onto each image using PIL.
  - Supports both image and text watermarks.
  - Batch processing and real-time preview for efficient workflow.

---

### 🕵️ Invisible Watermarking (DWT-DCT)

- **Description:**  
  Embeds a binary watermark (text or image) into the host image using a combination of **Discrete Wavelet Transform (DWT)** and **Discrete Cosine Transform (DCT)**.
- **Implementation:**  
  - Embedding and extraction are performed on the **Y channel** (luminance) in **YCbCr** color space.
  - Watermark is embedded in DCT coefficients of DWT-LL subbands, with adaptive margin and redundancy.
  - Supports watermark extraction (binary pattern) with verification functionality.
  - Robust against common image attacks (JPEG, noise, blur).

---

## 📊 Metrics & Robustness

| Metric                | Purpose                                                      | Formula                                                                                  |
|-----------------------|--------------------------------------------------------------|------------------------------------------------------------------------------------------|
| **Imperceptibility (PSNR)** | High PSNR (e.g., >40 dB) means the watermark is visually imperceptible. | $PSNR = 20 \cdot \log_{10} \left(\frac{255.0}{\sqrt{MSE}}\right)$                        |
| **Robustness (NCC)**        | NCC close to 1.0 means the watermark is perfectly recovered.           | $NCC = mean(sign(original\_wm) \cdot sign(recovered\_wm))$                               |
| **Attack Simulation**       | Robustness is tested against common image attacks: JPEG compression ($Q=85, 70, 50$), Gaussian noise ($\sigma=0.03, 0.06$), Gaussian blur ($\sigma=0.8, 1.2$). | - |

---

## ⚡ Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/The-GANners/Watermark-UI.git
   cd Watermark-UI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python FreeMark.py
   ```

---

## 🛠️ Command-Line Usage for Invisible Watermarking

You can also use the invisible watermarking functionality directly via command line scripts:

### **Embed Invisible Watermark**
```bash
python watermarkdwt.py --input "input_image.png" --output "watermarked.png" --text "Your watermark text"
# or for image watermark:
python watermarkdwt.py --input "input_image.png" --output "watermarked.png" --watermark_image "wm.png"
```

### **Extract & Verify Invisible Watermark**
```bash
python verify_watermark.py --input "watermarked.png" --text "Your watermark text"
# or for image watermark:
python verify_watermark.py --input "watermarked.png" --watermark_image "wm.png"
```

- The extraction script will output the extracted binary pattern and verification results in the console and optionally save the pattern image.

---

## 🧩 Module Structure

| Module                | Description                                      |
|-----------------------|--------------------------------------------------|
| **Visible Watermark** | Batch add visible image/text watermarks          |
| **Invisible Watermark** | Robust DWT-DCT invisible watermarking (text/image) |
| **Robustness Testing** | Simulate attacks and measure watermark survival  |
| **Extraction & Verification** | Extract and verify invisible watermarks   |

---

## 🖼️ Example Workflow

1. **Select images** to watermark (single or batch).
2. **Choose watermark type:** visible or invisible.
3. **Configure watermark:**  
   - For visible: set image/text, position, opacity, scale, rotation, padding.
   - For invisible: set text/image watermark, adjust embedding strength.
4. **Preview** the watermark on your images.
5. **Apply watermark** to all selected images.
6. **Download** all watermarked images in one click.
7. **(Invisible only)**: Extract and verify watermark, view robustness metrics.

---

## 📄 License

This project is released under the **MIT License**.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📧 Contact

For questions and feedback:
* Open an issue on GitHub
* Join our community discussions

---

<div align="center">

### ⭐ If you find this project useful, please consider giving it a star! ⭐

**Made with ❤️ by the GANners Team**

</div>
