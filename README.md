# Gemini-Image-Generator
 
*Create and transform images with the power of Google's Gemini 2.0 models.*

**Gemini Image Generator** is an interactive web application built with Streamlit that leverages Google's Gemini 2.0 Flash model for advanced image generation and transformation. Whether you're crafting original images from text prompts or reimagining existing visuals with creative modifications, this tool provides a seamless interface to explore the multimodal capabilities of Gemini 2.0.

---

## Features

- **Image Generation**: Generate high-quality images from text descriptions using Gemini 2.0 Flash Experimental.
- **Image Transformation**: Modify uploaded images with text-based instructions, such as style transfers or content edits.
- **Customizable Options**: Adjust creativity levels, apply artistic styles, and fine-tune outputs with negative prompts.
- **User-Friendly Interface**: Built with Streamlit for an intuitive dark-themed experience.
- **Downloadable Results**: Save generated or transformed images directly from the app.

---

## Gemini 2.0 Capabilities

This project utilizes the **Gemini 2.0 Flash Experimental** model (`gemini-2.0-flash-exp`) for image generation and transformation tasks. Below are the key capabilities of this model as implemented in the project:

### Model Overview
- **Model Name**: `gemini-2.0-flash-exp`
- **Purpose**: A fast, multimodal AI model optimized for generating and editing images alongside text outputs.
- **Key Features**:
  - **Native Image Generation**: Creates images directly from text prompts with support for styles like photorealistic, digital art, and more.
  - **Multimodal Understanding**: Processes text and image inputs for transformations, maintaining context across interactions.
  - **High Performance**: Offers rapid inference speeds, making it ideal for real-time applications.
  - **Enhanced Reasoning**: Leverages world knowledge to produce contextually accurate and detailed imagery.

### Algorithms in Gemini 2.0 Flash
While the exact internal workings of Gemini 2.0 are proprietary, the model employs advanced generative AI techniques:
- **Diffusion-Based Generation**: Likely uses a diffusion process to iteratively refine noise into coherent images based on text prompts.
- **Transformer Architecture**: Combines transformer layers for text understanding with vision models for image synthesis.
- **Multimodal Fusion**: Integrates text and image data through a unified latent space, enabling seamless generation and editing workflows.
- **Safety Mechanisms**: Incorporates safety filters to manage content generation, configurable via API settings.

### Image Workflow (Gemini Perspective)
1. **Input Processing**:
   - Text prompts are tokenized and encoded into a latent representation.
   - For transformations, uploaded images are preprocessed and embedded alongside text instructions.
2. **Latent Space Mapping**:
   - The model maps inputs into a shared multimodal latent space, aligning text descriptions with visual features.
3. **Generation/Transformation**:
   - For generation, the model samples from the latent space to produce an image.
   - For transformation, it modifies the latent representation of the input image based on the prompt, preserving specified elements.
4. **Output Rendering**:
   - The resulting latent representation is decoded into a high-resolution image, streamed back as inline data.
5. **Iterative Refinement**:
   - The model may perform internal iterations to enhance quality, guided by parameters like temperature and top-k sampling.

---

## Prerequisites

To run this project locally, ensure you have the following:

- **Python**: Version 3.8 or higher
- **Google API Key**: Access to Gemini 2.0 models via Google AI Studio or Vertex AI (see [Setup](#setup) below)
- **Git**: For cloning the repository
- **A modern web browser**: For interacting with the Streamlit app

---

## Setup

Follow these steps to get Gemini Image Studio running on your local system:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/gemini-image-studio.git
cd gemini-image-studio
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
Install the required Python packages listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```
*Note*: If `requirements.txt` is not yet created, install these core dependencies:
```bash
pip install streamlit google-generativeai pillow
```

### 4. Obtain a Google API Key
- Visit [Google AI Studio](https://ai.google.dev/) and sign in with your Google account.
- Navigate to the API section and click **"Get API Key"**.
- Create a new API key and copy it securely.
- The app will prompt you to enter this key on first launch, or you can set it as an environment variable:
  ```bash
  export GEMINI_API_KEY="your-api-key-here"  # On Windows: set GEMINI_API_KEY=your-api-key-here
  ```

### 5. Run the Application
Launch the Streamlit app:
```bash
streamlit run app.py
```
- Open your browser and go to `http://localhost:8501` to access the app.

---

## Usage

1. **Enter API Key**: On first launch, input your Google API key in the provided text field and save it.
2. **Choose Mode**:
   - **Image Generation**: Enter a text prompt (e.g., "A futuristic city at sunset") and optionally select a style.
   - **Image Transformation**: Upload an image and describe how to modify it (e.g., "Convert to watercolor style").
3. **Customize**: Adjust creativity levels or add negative prompts for finer control.
4. **Generate/Transform**: Click the respective button to process your request.
5. **Download**: Save your generated or transformed image using the download button.

---

## Project Structure

```
gemini-image-studio/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore file
```

---

## Troubleshooting

- **API Key Errors**: Ensure your key has access to Gemini 2.0 models and is correctly entered.
- **Image Not Generated**: Check your prompt for clarity or adjust the creativity slider; some prompts may be filtered by safety settings.
- **Streamlit Issues**: Verify all dependencies are installed and Python is up-to-date.
- **Connection Problems**: Confirm your internet connection, as the app relies on Google's API.

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Google Gemini Team**: For developing the powerful Gemini 2.0 Flash model.
- **Streamlit Community**: For providing an excellent framework for building interactive apps.

---

*Built with ❤️ by [ShutterStack](https://github.com/ShutterStack)*

