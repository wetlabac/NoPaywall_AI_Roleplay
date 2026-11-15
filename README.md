# NoPaywall_AI_Roleplay

**NoPaywall_AI_Roleplay** is a fully local, self-hosted AI roleplay and image generation stack for Windows. It is designed to give you complete control over your AI interactions without relying on paid cloud services. Everything runs on your own hardware, ensuring privacy and zero subscription costs.

This stack combines text generation (Ollama), a powerful web interface (SillyTavern), and local image generation (ComfyUI), all controlled via a Telegram bot for convenience.

## 📸 Screenshots

| Telegram Bot Control | SillyTavern Extension Menu |
| :---: | :---: |
| ![Telegram Bot](screenshots/telegram.png) | ![Menu](screenshots/menu.png) |

| Extension Settings | Tag Editing Modal |
| :---: | :---: |
| ![Settings](screenshots/settings.png) | ![Modal](screenshots/modal.png) |

<<<<<<< HEAD
## 📦 Components & Credits
=======
### 🖼️ Screenshots
*Here is how the extension menu looks in SillyTavern (mobile view):*
<img src="file.webp" width="300" alt="Extension Menu">

### Core Features
*   **🔍 Image Analysis (Import Tags):** Upload any reference image. The script extracts Danbooru tags via ComfyUI (using the DeepGelbooru model) and puts them into an editable field.
*   **🎨 Instant Variation:** Upload an image, and the script will extract tags and **immediately generate** a new image based on them.
*   **💬 Text-to-Image:** Create images purely from a text prompt, no reference needed.
*   **🧠 Automatic LoRA Loading:** The script detects the active character in SillyTavern and automatically finds the matching LoRA file in your ComfyUI `models/loras` folder. No manual selection required.
*   **📱 PC & Mobile Support:** Automatically detects the host IP address (`window.location.hostname`), allowing seamless use from both desktop and mobile browsers on the same local network.
*   **📸 In-Chat Image Insertion:** Uses the Base64 method (adapted from *Image Gen Kazuma*) to save generated images directly into SillyTavern's folder. This guarantees that images display correctly in the chat, even on mobile devices.
>>>>>>> 2a879f474a699d73477a27d5b314391aa89ebb3b

This project stands on the shoulders of giants. Huge thanks to the original authors:

### Core Applications
*   **SillyTavern**: The frontend for interacting with LLMs. [GitHub](https://github.com/SillyTavern/SillyTavern) | [Docs](https://docs.sillytavern.app/). Licensed under **AGPL-3.0**.
*   **ComfyUI**: The node-based GUI for Stable Diffusion. [GitHub](https://github.com/comfyanonymous/ComfyUI) | [Portable Download](https://github.com/comfyanonymous/ComfyUI/releases/latest/download/ComfyUI_windows_portable_nvidia.7z). Licensed under **GPL-3.0**.
*   **Ollama**: The local LLM runner. [Website](https://ollama.com/). Licensed under **MIT**.

### Models Used
*   **Text Generation**: [Ministral-3-8B-Nymphaea-RP](https://huggingface.co/0xA50C1A1/Ministral-3-8B-Nymphaea-RP) by `0xA50C1A1`. Licensed under **Apache-2.0**.
*   **Image Generation (Checkpoint)**: [WAI-NSFW-Illustrious-17](https://tensor.art/models/990778216270553015) by WAI0731. License: **CreativeML OpenRAIL-M** (via base model). The author permits commercial use of generated images but prohibits reselling the model itself.
*   **Tagging Models**: `wd-eva02-large-tagger-v3` (auto-downloaded) and [v2ray/deepgelbooru](https://huggingface.co/v2ray/deepgelbooru) by v2ray. DeepGelbooru is licensed under **MIT**.

<<<<<<< HEAD
### Custom Nodes & Extensions
*   **SillyTavern Image Extension**: Based on [Image-gen-kazuma](https://github.com/Arif-salah/Image-gen-kazuma) by Arif-salah. Licensed under **MIT**. (Heavily modified in this repo to support the dual-tagger workflow and API structure).
*   **ComfyUI Node (WD Tagger)**: [ComfyUI-WD-Timm-Tagger](https://github.com/bedovyy/ComfyUI-WD-Timm-Tagger) by bedovyy. Licensed under **MIT**.
*   **ComfyUI Node (ImgUtils)**: [comfyui-imgutils](https://github.com/xiaden/comfyui-imgutils) by xiaden. Licensed under **MIT**.
=======
1.  **Clone this repository** or download it as a ZIP.
2.  **SillyTavern Extension:** Place the `Ult_generation` folder into your SillyTavern directory:
    `SillyTavern/public/scripts/extensions/third-party/Ult_generation/`
3.  **ComfyUI Requirements:** Ensure you have installed the `comfyui-imgutils` plugin in your ComfyUI `custom_nodes` folder.
4.  **Scripts:** Place `start_all.bat`, `stop_all.bat`, `start_bot.bat`, and `start_bot.vbs` in your root AI folder (e.g., `E:\AI\`).
5.  **Telegram Bot:** Configure your bot token in the `ai_bot.py` script (or use environment variables).
6.  Restart SillyTavern. A **camera icon** (📷) will appear in the message input bar.
>>>>>>> 2a879f474a699d73477a27d5b314391aa89ebb3b

---

## 🚀 Installation Guide

<<<<<<< HEAD
### Prerequisites
*   Windows 10/11
*   NVIDIA GPU (RTX 3070 Ti or better recommended for 8GB VRAM)
*   Node.js (LTS version) for SillyTavern
*   Git (optional, but recommended)
=======
## 🌐 Disabling Auto-Translation (Important!)

If your browser (like Chrome or Yandex) automatically translates the page, it can break the SillyTavern interface and translate technical terms (like "Checkpoint" or "LoRA") into Russian, making it impossible to find the correct settings.

To prevent this:
1.  **In your browser settings**: Go to Settings -> Languages -> Disable "Offer to translate pages".
2.  **On the page**: If a translation bar appears at the top of the page, click "Options" (three dots) and select **"Never translate this site"**.
3.  **SillyTavern settings**: Inside SillyTavern, go to the User Settings (icon of a person) and set the Interface Language to **English** to ensure the extension buttons match the README instructions.

## 🎮 Managing the Stack (Start & Stop Scripts)

To make launching and closing the entire AI stack effortless, this repository includes two custom batch scripts. They are designed to be used either manually or remotely via the Telegram bot.

### 🟢 How `start_all.bat` works
This script is your one-click launcher. When executed, it performs the following steps:
1.  **Launch Ollama:** Starts the Ollama background service if it is not already running.
2.  **Launch ComfyUI:** Opens a new command prompt window and starts ComfyUI. It waits a few seconds to ensure the server initializes properly.
3.  **Launch SillyTavern:** Opens another command prompt window and starts the SillyTavern server.
4.  **Ready to Use:** Once all three windows are open, you can access SillyTavern in your browser and start chatting or generating images.

### 🔴 How `stop_all.bat` works
This script is designed for a safe and complete shutdown. It ensures that heavy AI processes are terminated to free up your GPU and RAM, but **it intentionally leaves your Telegram bot running** so you can still command the PC remotely. 
Here is what it does:
1.  **Stops Ollama:** Forcefully closes `ollama.exe` and `ollama app.exe`.
2.  **Stops SillyTavern:** Uses PowerShell to find the specific process occupying port `8000` and terminates it. It also scans for any remaining `SillyTavern` related processes to ensure a clean shutdown.
3.  **Stops ComfyUI:** Uses PowerShell to find the process occupying port `8188` and terminates it.
4.  **Cleans up Windows:** Closes any leftover command prompt windows with titles like "ComfyUI" or "SillyTavern".
5.  **Preserves the Bot:** It carefully avoids killing the `python.exe` process that runs `ai_bot.py`, keeping your remote control alive.

## 🙏 Credits & Acknowledgments
>>>>>>> 2a879f474a699d73477a27d5b314391aa89ebb3b

### Step 1: Install SillyTavern
1.  Clone the repository into a folder (e.g., `E:\AI\SillyTavern`):
    ```bash
    git clone https://github.com/SillyTavern/SillyTavern -b release
Run Start.bat to install dependencies. The web UI will open at http://127.0.0.1:8000.

Step 2: Install ComfyUI
Download the ComfyUI Windows Portable (NVIDIA).

Extract the archive to your preferred location (e.g., E:\AI\ComfyUI).

Step 3: Install Custom Nodes
Open the ComfyUI Manager (or manually clone into ComfyUI/custom_nodes/):

<<<<<<< HEAD
WD-Timm-Tagger: Clone bedovyy/ComfyUI-WD-Timm-Tagger.
=======
*   **My Custom Code (Extension & Scripts):** Licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
*   **DeepGelbooru:** MIT License.
*   **Image Gen Kazuma:** MIT License.
>>>>>>> 2a879f474a699d73477a27d5b314391aa89ebb3b

ImgUtils: Clone xiaden/comfyui-imgutils.

Install requirements:

bash
python_embeded\python.exe -m pip install -r ComfyUI\custom_nodes\ComfyUI-WD-Timm-Tagger\requirements.txt
python_embeded\python.exe -m pip install -r ComfyUI\custom_nodes\comfyui-imgutils\requirements.txt
Step 4: Download Models
Text Model: Download Ministral-3-8B-Nymphaea-RP (GGUF format, e.g., Q4_K_M) and create a Modelfile for Ollama.

Image Models:

Place WAI-NSFW-Illustrious-17.safetensors in ComfyUI/models/checkpoints/.

LoRA (Important): This extension automatically detects and applies a character LoRA based on the active character name in SillyTavern. To make it work, the LoRA filename (without the .safetensors extension) must match the character's name.

Matching rules: The extension ignores hyphens (-) and underscores (_). It does not ignore extra words like v1, final, etc.

Example: If your character is named "Marin Kitagawa", the LoRA file should be named Marin_Kitagawa.safetensors or Marin-Kitagawa.safetensors. A file named Marin_Kitagawa_v1.safetensors will not be matched automatically.

Place your LoRA files in ComfyUI/models/loras/.

Tagging Models: The WD-Timm-Tagger and ImgUtils nodes will automatically download wd-eva02-large-tagger-v3 and the DeepGelbooru model upon first use.

Step 5: Configure ComfyUI for API Access
Edit ComfyUI/run_nvidia_gpu.bat and add the following flags to the startup command:

bat
--listen --enable-cors-header
This allows SillyTavern to communicate with ComfyUI over the local network.

Step 6: Install the Custom Extension
Inside this repository, locate the folder named Ult_generation.

Copy the entire Ult_generation folder into your SillyTavern installation at:

text
SillyTavern/public/scripts/extensions/third-party/
Reload SillyTavern (F5 in your browser).

Step 7: Import the ComfyUI Workflow
Open ComfyUI in your browser (http://127.0.0.1:8188).

Drag and drop the provided NSFW.json file into the ComfyUI canvas.

Important: The NSFW.json is an API-format export. You must ensure that the ckpt_name (Checkpoint) and lora_name (LoRA) fields in the JSON match the exact filenames on your disk, or simply leave the LoRA field empty if you rely on the extension's auto-detection.

🤖 Telegram Bot (Optional)
The repository includes ai_bot.py, a Python-based Telegram bot for remotely starting and stopping the AI services.

Create a bot_settings.ini file with your bot token and allowed user IDs.

Run ai_bot.py (or use start_bot.vbs for a silent background launch).

📄 License
This project is a personal compilation and is provided for educational purposes. All credit goes to the original authors of the models, nodes, and extensions listed above. Please respect their individual licenses. The author of this repository is not responsible for any misuse of the included tools or models.

*   **Boosty:** [https://boosty.to/wetlabac](https://boosty.to/wetlabac)
*   **Tribute:** [https://web.tribute.tg/e/1Pz](https://web.tribute.tg/e/1Pz)

Your support helps keep the project alive and free for everyone.
