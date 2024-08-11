# ### DRAWS SCRIBBLY TRIANGLES AND LINES ALL OVER THE IMAGE

# import streamlit as st
# from PIL import Image, ImageDraw
# import numpy as np
# import io

# def cubism_filter(image):
#     draw = ImageDraw.Draw(image)
#     width, height = image.size
#     grid_size = 50  # Adjust grid size for detail level

#     for x in range(0, width, grid_size):
#         for y in range(0, height, grid_size):
#             # Draw random shapes
#             points = [(x + np.random.randint(-grid_size, grid_size),
#                        y + np.random.randint(-grid_size, grid_size)) for _ in range(4)]
#             draw.polygon(points, outline="black")

#     return image

# st.title("Cubism Filter Application")

# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# if uploaded_file is not None:
#     # Open the image file
#     image = Image.open(uploaded_file)
    
#     # Apply the Cubism filter
#     filtered_image = cubism_filter(image.copy())
    
#     # Display the original and filtered images
#     st.image(image, caption='Original Image', use_column_width=True)
#     st.image(filtered_image, caption='Cubist Image', use_column_width=True)
    
#     # Save the filtered image to a BytesIO object
#     filtered_image_io = io.BytesIO()
#     filtered_image.save(filtered_image_io, format='PNG')
#     filtered_image_io.seek(0)
    
#     # Provide a download button
#     st.download_button(
#         label="Download Cubist Image",
#         data=filtered_image_io,
#         file_name="cubist_output.png",
#         mime="image/png"
#     )

#### CREATES A FADED MINECRAFT-LIKE GRAPH OF COLORS

# import streamlit as st
# from PIL import Image, ImageDraw, ImageFilter
# import numpy as np
# import io

# def cubism_filter(image):
#     draw = ImageDraw.Draw(image)
#     width, height = image.size
#     grid_size = 50  # Adjust grid size for detail level

#     for x in range(0, width, grid_size):
#         for y in range(0, height, grid_size):
#             # Get average color within the grid
#             average_color = np.mean(np.array(image.crop((x, y, x + grid_size, y + grid_size))), axis=(0, 1))
#             average_color = tuple(int(c) for c in average_color[:3])

#             # Draw polygon with average color
#             points = [(x, y), (x + grid_size, y), (x + grid_size, y + grid_size), (x, y + grid_size)]
#             draw.polygon(points, fill=average_color, outline="black")

#     return image

# st.title("Cubism Filter Application")

# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# if uploaded_file is not None:
#     # Open the image file
#     image = Image.open(uploaded_file)
    
#     # Apply the Cubism filter
#     filtered_image = cubism_filter(image.copy())
    
#     # Display the original and filtered images
#     st.image(image, caption='Original Image', use_column_width=True)
#     st.image(filtered_image, caption='Cubist Image', use_column_width=True)
    
#     # Save the filtered image to a BytesIO object
#     filtered_image_io = io.BytesIO()
#     filtered_image.save(filtered_image_io, format='PNG')
#     filtered_image_io.seek(0)
    
#     # Provide a download button
#     st.download_button(
#         label="Download Cubist Image",
#         data=filtered_image_io,
#         file_name="cubist_output.png",
#         mime="image/png"
#     )


import streamlit as st
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import scipy.spatial
import io

def generate_random_points(width, height, num_points):
    points = np.random.rand(num_points, 2) * [width, height]
    return points

def voronoi(image, points):
    width, height = image.size
    vor = scipy.spatial.Voronoi(points)
    draw = ImageDraw.Draw(image)
    for region in vor.regions:
        if not -1 in region and len(region) > 3:
            polygon = [tuple(vor.vertices[i]) for i in region]
            if all(0 <= x < width and 0 <= y < height for x, y in polygon):
                centroid = tuple(np.mean(polygon, axis=0))
                try:
                    average_color = tuple(np.array(image.getpixel((int(centroid[0]), int(centroid[1])))).astype(int))
                    draw.polygon(polygon, fill=average_color, outline="black")
                except Exception as e:
                    print(f"Error drawing polygon: {e}")
    return image

def cubism_filter(image, num_points):
    width, height = image.size
    points = generate_random_points(width, height, num_points)
    return voronoi(image, points)

st.title("Enhanced Cubism Filter Application")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open the image file
    image = Image.open(uploaded_file)
    
    # Sliders to adjust the display size
    display_width = st.slider("Display Width", min_value=100, max_value=image.width, value=400)
    display_height = st.slider("Display Height", min_value=100, max_value=image.height, value=400)
    
    # Resize the image for display
    display_size = (display_width, display_height)
    resized_image = image.resize(display_size)
    
    # Slider to adjust the number of random points
    num_points = st.slider("Number of points for the Cubism effect", min_value=50, max_value=7000, value=500, step=20)
    
    # Apply the Cubism filter
    filtered_image = cubism_filter(image.copy(), num_points)
    
    # Resize the filtered image for display
    resized_filtered_image = filtered_image.resize(display_size)
    left, right = st.columns(2)
    # Display the original and filtered images
    with left:
        st.image(resized_image, caption='Original Image', use_column_width=True)
    with right:
        st.image(resized_filtered_image, caption='Cubist Image', use_column_width=True)
    
    # Save the filtered image to a BytesIO object
    filtered_image_io = io.BytesIO()
    filtered_image.save(filtered_image_io, format='PNG')
    filtered_image_io.seek(0)
    
    # Provide a download button
    st.download_button(
        label="Download Cubist Image",
        data=filtered_image_io,
        file_name="cubist_output.png",
        mime="image/png"
    )

