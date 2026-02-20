# AI Dataset Alpha Master 🚀

**AI Dataset Alpha Master** is a professional GUI tool designed to streamline the preparation of image datasets for AI training (Stable Diffusion LoRA, Checkpoints, etc.). 

It specifically focuses on creating high-quality **transparent (Alpha channel) images**, which are crucial for training with the `alpha_mask: True` parameter in Kohya_ss, ensuring perfectly clean edges and professional results.

---

## ✨ Features

*   **AI-Powered Background Removal:** Choose between multiple specialized models:
    *   `u2net`: General purpose, excellent for aggressive shadow removal.
    *   `isnet-anime`: Optimized for illustrations and anime-style art.
    *   `birefnet-portrait`: High-resolution portrait specialist.
*   **Interactive Vertical Cropping:** A dedicated slider to crop images from the top (e.g., to create consistent busts or portraits), automatically solving messy feet and ground shadow issues.
*   **Visual Refinement:** Real-time sliders for `Erode` (edge trimming) and `Background Threshold` to fine-tune transparency.
*   **Dataset Navigation:** Scroll through your entire folder with preview navigation to check settings across different images.
*   **Batch Processing:** Process hundreds of images with one click, featuring a progress bar and multithreaded stability (no freezing).
*   **Modern UI:** A clean, Dark Mode interface built with CustomTkinter.

---

## 🛠️ Installation

1.  **Clone the repository** (or download and extract the ZIP):
    ```bash
    git clone https://github.com/SilentLuxRay/Background_Remover.git
    cd YOUR_REPO_NAME
    ```

2.  **Create a Virtual Environment** (Recommended):
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 How to Use

1.  **Run the application:**
    ```bash
    python main.py
    ```
2.  **Load Folder:** Click "Carica Cartella" and select your raw dataset directory.
3.  **Preview & Adjust:**
    *   Switch between AI Models to see which one works best for your images.
    *   Adjust **Erode** to trim dirty edges.
    *   Enable **Ritaglio Altezza** to create perfect "bust" shots for RPG portraits or character LoRAs.
4.  **Navigate:** Use the arrows to verify the effect on different samples.
5.  **Batch Process:** Click **ELABORA TUTTO** to generate your clean dataset in the `Dataset_Output_Pro` subfolder.

---

## 💡 Why use Alpha Masking for Kohya?

When training a LoRA, using images with an Alpha channel and setting `alpha_mask = true` in your configuration allows the AI to focus **only** on the colored pixels of your subject. 

This prevents the model from "learning" background noise, shadows, or artifacts, resulting in a much more flexible and "cut-out" friendly LoRA. This tool automates the tedious task of manually masking hundreds of images.

---

## 📦 Requirements

*   Python 3.10+
*   `customtkinter`
*   `rembg`
*   `pillow`
*   `opencv-python`

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
