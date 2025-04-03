import streamlit as st
import os
import io
import base64
from PIL import Image
from google import genai
from google.genai import types

# Set page configuration
st.set_page_config(
    page_title="Gemini Image Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme styling
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .block-container {
        padding: 2rem 1rem;
    }
    .css-1v3fvcr {
        background-color: transparent;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3rem;
        font-weight: 500;
        background-color: #FF4B4B;
        color: white;
    }
    .stButton>button:hover {
        background-color: #FF3B3B;
        color: white;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
        background-color: #262730;
        color: #FAFAFA;
    }
    .css-1cpxqw2 {
        border-radius: 20px;
        padding: 1.5rem;
        background-color: #1E1E2E;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        margin-bottom: 1rem;
    }
    h1, h2, h3 {
        color: #FAFAFA;
    }
    .result-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 400px;
        background-color: #262730;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1rem;
        margin-top: 1rem;
    }
    .loader {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
    }
    .stTextArea textarea {
        background-color: #262730;
        color: #FAFAFA;
    }
    .stSelectbox>div>div {
        background-color: #262730;
        color: #FAFAFA;
    }
    .stExpanderHeader {
        background-color: #262730;
        color: #FAFAFA;
    }
    [data-testid="stSidebar"] {
        background-color: #1E1E2E;
    }
    .stRadio label, .stCheckbox label {
        color: #FAFAFA;
    }
    .stSlider > div > div {
        background-color: #333342;
    }
    .stFileUploader {
        background-color: #262730;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.title("🎨 Gemini Image Studio")
st.markdown("Create and transform images using Google's Gemini 2.0 model")

# API Key input in the app
if 'api_key_set' not in st.session_state:
    st.session_state.api_key_set = False

if not st.session_state.api_key_set:
    st.info("To get started, enter your Google API key with access to Gemini models.")
    api_key = st.text_input("Enter your Google API Key:", type="password")
    if st.button("Save API Key"):
        if api_key:
            try:
                # Just initialize the client - it doesn't validate the API key immediately
                # We'll store it and test it when actually using it
                st.session_state.api_key = api_key
                st.session_state.api_key_set = True
                st.success("API key saved! You can now use the app.")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error saving API key: {str(e)}")
        else:
            st.error("Please enter an API key.")
else:
    # Show option to reset API key
    if st.sidebar.button("Reset API Key"):
        st.session_state.api_key_set = False
        st.session_state.pop('api_key', None)
        st.experimental_rerun()

    # Initialize the Gemini client with the saved API key
    client = genai.Client(api_key=st.session_state.api_key)
    
    # Sidebar for navigation
    st.sidebar.title("Options")
    app_mode = st.sidebar.selectbox(
        "Choose Mode",
        ["Image Generation", "Image Transformation"]
    )

    # Sidebar info
    with st.sidebar.expander("About", expanded=False):
        st.markdown("""
        This app uses Google's Gemini 2.0 Flash model for image generation and transformation. You can:
        
        * Generate images from text descriptions
        * Transform existing images with text prompts
        """)
    
    # Define standard generation config
    def get_generation_config(temperature=1.0):
        return types.GenerateContentConfig(
            temperature=temperature,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_modalities=["image", "text"],
            safety_settings=[
                types.SafetySetting(
                    category="HARM_CATEGORY_CIVIC_INTEGRITY",
                    threshold="OFF",
                ),
            ],
            response_mime_type="text/plain",
        )

    # Helper function to save temporary files
    def save_temp_file(data, file_name="temp.jpg"):
        with open(file_name, "wb") as f:
            f.write(data)
        return file_name

    # Helper function to generate an image from text
    def generate_image(prompt, style=None, temperature=1.0):
        try:
            # Format the prompt
            full_prompt = prompt
            if style:
                full_prompt = f"{prompt}, in the style of {style}"
            
            # Set up the model and content
            model = "gemini-2.0-flash-exp"
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=full_prompt),
                    ],
                )
            ]
            
            # Generate the content with the config
            generate_content_config = get_generation_config(temperature)
            
            # Process the response to extract the image
            image_data = None
            response_text = ""
            
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
                    continue
                
                if chunk.candidates[0].content.parts[0].inline_data:
                    image_data = chunk.candidates[0].content.parts[0].inline_data.data
                else:
                    # Collect any text response
                    text_chunk = chunk.text
                    if text_chunk:
                        response_text += text_chunk
            
            return image_data, response_text
            
        except Exception as e:
            st.error(f"Error generating image: {str(e)}")
            return None, str(e)

    # Helper function to transform an image
    def transform_image(image_data, prompt, temperature=1.0):
        try:
            # Save the image temporarily to upload it
            temp_path = "temp_upload.jpg"
            with open(temp_path, "wb") as f:
                f.write(image_data)
            
            # Upload the file to the Gemini API
            file = client.files.upload(file=temp_path)
            
            # Set up the model and content
            model = "gemini-2.0-flash-exp-image-generation"
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_uri(
                            file_uri=file.uri,
                            mime_type=file.mime_type,
                        ),
                        types.Part.from_text(text=f"Transform this image: {prompt}"),
                    ],
                )
            ]
            
            # Generate the content with the config
            generate_content_config = get_generation_config(temperature)
            
            # Process the response to extract the image
            transformed_image_data = None
            response_text = ""
            
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
                    continue
                
                if chunk.candidates[0].content.parts[0].inline_data:
                    transformed_image_data = chunk.candidates[0].content.parts[0].inline_data.data
                else:
                    # Collect any text response
                    text_chunk = chunk.text
                    if text_chunk:
                        response_text += text_chunk
            
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return transformed_image_data, response_text
            
        except Exception as e:
            st.error(f"Error transforming image: {str(e)}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return None, str(e)

    # Helper function to display an image
    def display_image(image_data, caption=None):
        if image_data:
            # Create a PIL Image from bytes
            image = Image.open(io.BytesIO(image_data))
            st.image(image, caption=caption, use_column_width=True)
            
            # Add download button
            st.download_button(
                label="Download Image",
                data=image_data,
                file_name="gemini_image.jpg",
                mime="image/jpeg"
            )
            return True
        else:
            st.warning("No image was generated. Please try a different prompt.")
            return False

    # Image Generation Section
    if app_mode == "Image Generation":
        st.header("Generate Images from Text")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            prompt = st.text_area("Describe the image you want to create:", 
                                 height=100, 
                                 placeholder="A serene lake surrounded by autumn trees with mountains in the background, golden hour lighting")
            
        with col2:
            style = st.selectbox(
                "Choose a style (optional)",
                [None, "Photorealistic", "Digital Art", "Oil Painting", "Watercolor", 
                 "Sketch", "Cartoon", "Anime", "3D Rendering", "Pixel Art"]
            )
            
            temperature = st.slider(
                "Creativity level:",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Higher values produce more creative results"
            )
        
        # Advanced options collapsible
        with st.expander("Advanced Options", expanded=False):
            neg_prompt = st.text_area(
                "Negative prompt (what to avoid):", 
                height=50,
                placeholder="blurry, distorted faces, extra limbs"
            )
        
        # Generate button with loading animation
        if st.button("🚀 Generate Image"):
            if prompt:
                with st.spinner("Creating your masterpiece..."):
                    # Adjust prompt with negative prompt if provided
                    full_prompt = prompt
                    if neg_prompt:
                        full_prompt = f"{prompt}. Avoid: {neg_prompt}"
                    
                    # Generate image
                    image_data, response_text = generate_image(full_prompt, style, temperature)
                    
                    # Display result
                    if image_data:
                        st.markdown("### Your Generated Image")
                        with st.container():
                            display_image(image_data)
                            
                        # Display any text response from the model
                        if response_text:
                            with st.expander("Model's comments", expanded=False):
                                st.write(response_text)
                    else:
                        st.error("Failed to generate image. Please try a different prompt or check your API key.")
            else:
                st.warning("Please enter a prompt to generate an image.")
        
        # Example prompts section
        with st.expander("Example Prompts", expanded=False):
            example_prompts = [
                "A futuristic city with flying cars and glowing neon signs, twilight",
                "A cozy coffee shop interior with wooden elements, books, and plants, warm lighting",
                "An underwater scene with colorful coral reefs and tropical fish",
                "A fantasy landscape with floating islands and waterfalls flowing between them",
                "A cyberpunk portrait of a person with neon lights and advanced technology"
            ]
            
            for i, ex_prompt in enumerate(example_prompts):
                if st.button(f"Try Example {i+1}", key=f"ex_{i}"):
                    st.session_state.example_prompt = ex_prompt
                    st.experimental_rerun()
                    
            if "example_prompt" in st.session_state:
                st.text_area("Example prompt:", st.session_state.example_prompt, height=80)
                if st.button("Use This Example"):
                    prompt = st.session_state.example_prompt
                    # Generate image using the example prompt
                    with st.spinner("Creating your masterpiece..."):
                        image_data, response_text = generate_image(prompt, style, temperature)
                        if image_data:
                            st.markdown("### Your Generated Image")
                            with st.container():
                                display_image(image_data)

    # Image Transformation Section
    else:
        st.header("Transform Existing Images")
        
        # Upload image
        uploaded_file = st.file_uploader("Upload an image to transform", type=["png", "jpg", "jpeg"])
        
        if uploaded_file is not None:
            # Get the image data
            image_bytes = uploaded_file.getvalue()
            
            # Display the uploaded image
            image = Image.open(io.BytesIO(image_bytes))
            st.markdown("### Original Image")
            st.image(image, width=400)
            
            # Get transformation prompt
            transform_prompt = st.text_area(
                "Describe how you want to transform the image:", 
                height=100,
                placeholder="Convert to watercolor style with autumn colors"
            )
            
            # Add transformation options
            with st.expander("Transformation Options", expanded=False):
                preserve_option = st.slider(
                    "How much to preserve the original image (approximate):",
                    0, 100, 50,
                    help="Higher values try to keep more elements from the original image"
                )
                
                transform_type = st.radio(
                    "Transformation type:",
                    ["Style Transfer", "Content Modification", "Background Change"],
                    index=0
                )
                
                temperature = st.slider(
                    "Creativity level:",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.7,
                    step=0.1,
                    help="Higher values produce more creative results"
                )
                
                # Adjust the prompt based on options
                if transform_type == "Style Transfer" and transform_prompt:
                    full_transform_prompt = f"Apply this style to the image: {transform_prompt}. Preserve approximately {preserve_option}% of the original content."
                elif transform_type == "Content Modification" and transform_prompt:
                    full_transform_prompt = f"Modify the content of this image: {transform_prompt}. Preserve approximately {preserve_option}% of the original content."
                elif transform_type == "Background Change" and transform_prompt:
                    full_transform_prompt = f"Change the background to: {transform_prompt}. Keep the main subject intact."
                else:
                    full_transform_prompt = transform_prompt
                    
            # Transform button
            if st.button("🔄 Transform Image"):
                if transform_prompt:
                    with st.spinner("Transforming your image..."):
                        transformed_image_data, response_text = transform_image(image_bytes, full_transform_prompt, temperature)
                        
                        # Display result
                        if transformed_image_data:
                            st.markdown("### Transformed Image")
                            with st.container():
                                display_image(transformed_image_data)
                                
                            # Display any text response from the model
                            if response_text:
                                with st.expander("Model's comments", expanded=False):
                                    st.write(response_text)
                        else:
                            st.error("Failed to transform image. Please try a different prompt or check your API key.")
                else:
                    st.warning("Please enter a transformation prompt.")
                    
            # Example transformations
            with st.expander("Example Transformations", expanded=False):
                example_transforms = [
                    "Convert to pixel art style",
                    "Make it look like an oil painting",
                    "Change to night time with moonlight",
                    "Add a cyberpunk aesthetic with neon lights",
                    "Transform into a sketch with pencil shading"
                ]
                
                for i, ex_transform in enumerate(example_transforms):
                    if st.button(f"Try Example {i+1}", key=f"ex_transform_{i}"):
                        st.session_state.example_transform = ex_transform
                        st.experimental_rerun()
                        
                if "example_transform" in st.session_state:
                    st.text_area("Example transformation:", st.session_state.example_transform, height=80)
                    if st.button("Use This Example"):
                        transform_prompt = st.session_state.example_transform
                        with st.spinner("Transforming your image..."):
                            transformed_image_data, response_text = transform_image(image_bytes, transform_prompt, temperature)
                            if transformed_image_data:
                                st.markdown("### Transformed Image")
                                with st.container():
                                    display_image(transformed_image_data)
        else:
            st.info("Please upload an image to get started with transformations.")

    # Footer
    st.markdown("---")
    st.markdown("Built with Streamlit and Google's Gemini 2.0 Flash model")