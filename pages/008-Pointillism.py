import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import io

def generate_random_points(width, height, num_points):
    points = np.random.rand(num_points, 2) * [width, height]
    return points

def pointillism(image, num_points, dot_radius):
    width, height = image.size
    points = generate_random_points(width, height, num_points)
    draw = ImageDraw.Draw(image)

    print(f"Drawing {num_points} points with radius {dot_radius}")

    for i, point in enumerate(points):
        x, y = point
        color = image.getpixel((int(x), int(y)))
        print(f"Point {i}: (x: {x}, y: {y}), Color: {color}")

        # Ensure that coordinates are within the image bounds
        if 0 <= x - dot_radius < width and 0 <= y - dot_radius < height and \
           0 <= x + dot_radius < width and 0 <= y + dot_radius < height:
            try:
                draw.ellipse((x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius), fill=color, outline=color)
                print(f"Drawn ellipse at ({x}, {y}) with color {color}")
            except Exception as e:
                print(f"Error drawing ellipse at ({x}, {y}): {e}")
        else:
            print(f"Skipped drawing ellipse at ({x}, {y}) due to out of bounds")

    return image

st.title("Pointillism Filter Application")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    display_width = st.slider("Display Width", min_value=100, max_value=image.width, value=400)
    display_height = st.slider("Display Height", min_value=100, max_value=image.height, value=400)
    
    display_size = (display_width, display_height)
    resized_image = image.resize(display_size)
    
    num_points = st.slider("Number of points for the Pointillism effect", min_value=100, max_value=5000, value=1000, step=100)
    
    dot_radius = st.slider("Dot Radius", min_value=1, max_value=50, value=15)
    
    filtered_image = pointillism(image.copy(), num_points, dot_radius)
    
    resized_filtered_image = filtered_image.resize(display_size)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(resized_image, caption='Original Image', use_column_width=True)
    
    with col2:
        st.image(resized_filtered_image, caption='Pointillism Image', use_column_width=True)
    
    filtered_image_io = io.BytesIO()
    filtered_image.save(filtered_image_io, format='PNG')
    filtered_image_io.seek(0)
    
    st.download_button(
        label="Download Pointillism Image",
        data=filtered_image_io,
        file_name="pointillism_output.png",
        mime="image/png"
    )
