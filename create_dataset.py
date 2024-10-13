import os
import cv2
import json
import sys

# Set paths
video_dir = "Dataset"
output_dir = "FGC1M_Images"
if os.path.exists(output_dir):
    print(f"The output directory '{output_dir}' already exists. Exiting...")
    sys.exit(1)  # Exit with a non-zero status to indicate an error
os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

with open("categories.json", "r") as f:
    categories_data = json.load(f)

cat_dict = {
    cat["abbreviation"]: cat["name"] for cat in categories_data
}

coco_data = {
    "images": [],
    "annotations": [],
    "categories": []  # To store unique categories
}

# Metadata list to store information about each image
# metadata = []
global_img_id = 0

# Function to extract 100 frames from a video
def extract_frames(video_path, start_image_index):
    global global_img_id
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = max(total_frames // 100, 1)  # Extract 100 frames evenly spaced
    frame_count = 0
    extracted_count = 0

    while cap.isOpened() and extracted_count < 100:
        ret, frame = cap.read()
        if not ret:
            break  # End of video

        if frame_count % interval == 0:  # Save every 'interval'-th frame
            image_id = start_image_index + extracted_count

            img_filename = f"{start_image_index + extracted_count}.jpg"
            img_path = os.path.join(output_dir, img_filename)
            cv2.imwrite(img_path, frame)

            height, width, _ = frame.shape

            coco_data["images"].append({
                "id": global_img_id,  # Unique image ID
                "file_name": img_filename,
                "width": width,
                "height": height,
                "video_path": video_path  # Optional: store video path for reference
            })

            coco_data["images"].append({
                "id": global_img_id+1,  # Unique image ID
                "file_name": img_filename,
                "width": width,
                "height": height,
                "video_path": video_path  # Optional: store video path for reference
            })

            # # Store metadata
            # metadata.append({
            #     "image_id": extracted_count,
            #     "image_path": img_path,
            #     "video_path": video_path
            # })

            bruh_dict = {
                ccdt["name"]: ccdt["id"] for ccdt in coco_data["categories"]
            }

            coco_data["annotations"].append({
                "id": global_img_id,
                "image_id": global_img_id,
                "category_id": bruh_dict[cat_dict[video_path.split("/")[1].split("-")[0]]],  # Category ID for this image
                "bbox": [0, 0, width, height],  # Optional: bbox covering entire image
                "area": width * height,
                "iscrowd": 0,
                "gt_count": int(video_path.split("/")[2].split("-")[0])
            })

            coco_data["annotations"].append({
                "id": global_img_id+1,
                "image_id": global_img_id+1,
                "category_id": bruh_dict[cat_dict[video_path.split("/")[1].split("-")[1]]],  # Category ID for this image
                "bbox": [0, 0, width, height],  # Optional: bbox covering entire image
                "area": width * height,
                "iscrowd": 0,
                "gt_count": int(video_path.split("/")[2].split("-")[1])
            })

            global_img_id += 2

            extracted_count += 1

        frame_count += 1

    cap.release()

video_paths = []
for root, _, files in os.walk(video_dir):
    for file in files:
        if file.endswith(".mp4"):
            video_paths.append(os.path.join(root, file))

# Sort the video paths alphabetically
video_paths.sort()

cat_id = 0

# Process each video in sorted order
current_image_index = 0
for video_path in video_paths:
    cat1, cat2 = video_path.split("/")[1].split("-")
    cat_list = [cat["name"] for cat in coco_data["categories"]]
    if cat_dict[cat1] not in cat_list:
        coco_data["categories"].append({
            "id": cat_id,
            "name": cat_dict[cat1]
        })
        cat_id += 1
    
    if cat_dict[cat2] not in cat_list:
        coco_data["categories"].append({
            "id": cat_id,
            "name": cat_dict[cat2]
        })
        cat_id += 1

    extract_frames(video_path, current_image_index)
    current_image_index += 100


# Save metadata to a JSON file
# with open("metadata.json", "w") as f:
#     json.dump(metadata, f, indent=4)

print("Processing complete. Metadata saved to metadata.json.")

with open("coco_data.json", "w") as f:
    json.dump(coco_data, f, indent=4)

print("Processing complete. Coco saved to coco_data.json.")
