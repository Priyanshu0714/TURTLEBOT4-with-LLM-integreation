import os
import cv2
from ultralytics import YOLO

# Define the model path and name
MODEL_NAME = 'yolov10n.pt'
MODEL_DIR = 'models' # Directory to store the YOLOv8 models

def ensure_model_downloaded():
    """
    Ensures the YOLOv8 model is downloaded.
    The ultralytics library handles the download automatically if the model
    file is not found at the specified path.
    """
    model_path = os.path.join(MODEL_DIR, MODEL_NAME)

    # Create the models directory if it doesn't exist
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
        print(f"Created directory: {MODEL_DIR}")

    if not os.path.exists(model_path):
        print(f"Model '{MODEL_NAME}' not found in '{MODEL_DIR}'. Attempting to download...")
        # Initializing YOLO with the model name will trigger download if not local
        try:
            model = YOLO(MODEL_NAME)
            print(f"Model '{MODEL_NAME}' downloaded successfully to {model.model.yaml['path']}")
            # Move the downloaded model to the specified MODEL_DIR
            # Ultralytics often downloads to a default cache location (~/.cache/ultralytics/models)
            # We'll explicitly load from the model path to ensure it's used from there.
            # For simplicity, we assume YOLO() will eventually use the specified path if it exists.
            # The library manages its own cache. We just need to ensure we try to load it.
        except Exception as e:
            print(f"Error downloading model: {e}")
            print("Please ensure you have an active internet connection and sufficient disk space.")
            exit()
    else:
        print(f"Model '{MODEL_NAME}' already exists in '{MODEL_DIR}'. No download needed.")

    # Load the model from the specified path (or where ultralytics cached it)
    # If it was just downloaded, YOLO(MODEL_NAME) would have cached it.
    # We explicitly load by name, and ultralytics will find it in its cache or download again if necessary
    # (though typically not if already downloaded to cache).
    return YOLO(MODEL_NAME)

def detect_in_image(image_path, model):
    """
    Performs object detection on a static image.

    Args:
        image_path (str): The path to the input image.
        model (YOLO): The loaded YOLOv8 model.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image not found at '{image_path}'")
        return

    print(f"\n--- Running detection on image: {image_path} ---")
    try:
        # Perform detection
        # 'show=True' displays the image with detections in a new window
        # 'save=True' saves the resulting image to 'runs/detect/expX'
        results = model.predict(source=image_path, save=True, show=True)

        # Print results
        for r in results:
            # You can access various attributes like boxes, masks, probs
            # For example, to print the detected classes and confidence scores:
            if r.boxes is not None:
                print(f"Detected {len(r.boxes)} objects.")
                for box in r.boxes:
                    class_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    class_name = model.names[class_id]
                    print(f"  - Class: {class_name}, Confidence: {conf:.2f}")

        print("Detection complete. Results saved in 'runs/detect' directory.")
        cv2.waitKey(0) # Wait indefinitely until a key is pressed
        cv2.destroyAllWindows() # Close all OpenCV windows
    except Exception as e:
        print(f"An error occurred during image detection: {e}")

def detect_in_livestream(model):
    """
    Performs live object detection using the computer's default webcam.

    Args:
        model (YOLO): The loaded YOLOv8 model.
    """
    print("\n--- Starting live stream detection (press 'q' to quit) ---")
    print("If no camera feed appears, ensure your webcam is connected and not in use by another application.")
    try:
        # Perform detection on live stream (source=0 for default webcam)
        # 'show=True' displays the live feed with detections
        # 'conf=0.25' sets a confidence threshold for detections
        # 'stream=True' is important for video sources
        results = model.predict(source=0, show=True, conf=0.25, stream=True)

        # Iterate over frames from the webcam
        # The 'show=True' parameter in model.predict usually handles the display loop.
        # This loop is more for accessing the results programmatically if needed.
        for r in results:
            # You can process results here if you don't just want to show them
            # For example, to count objects:
            if r.boxes is not None:
                # print(f"Objects detected in frame: {len(r.boxes)}")
                pass
            # The 'show=True' argument to model.predict handles the display and 'q' key listener automatically
            # However, sometimes direct control with cv2.imshow is preferred for fine-tuning.
            # If `show=True` doesn't work as expected, you can manually read frames with cv2.VideoCapture
            # and then pass them to model.predict, then cv2.imshow.
            # But for simplicity and ease of use, ultralytics's `show=True` is generally reliable.

        print("Live stream detection stopped.")
    except Exception as e:
        print(f"An error occurred during live stream detection: {e}")
        print("Please check your camera connection and permissions.")

if __name__ == "__main__":
    # Ensure the model is downloaded and loaded
    yolo_model = ensure_model_downloaded()

    print("\n--- YOLOv8 Object Detection ---")
    while True:
        choice = input(
            "\nChoose an option:\n"
            "1. Detect objects in an image\n"
            "2. Detect objects in a live stream (webcam)\n"
            "3. Exit\n"
            "Enter your choice (1/2/3): "
        )

        if choice == '1':
            image_path = input("Enter the path to the image file (e.g., 'path/to/your/image.jpg'): ")
            detect_in_image(image_path, yolo_model)
        elif choice == '2':
            detect_in_livestream(yolo_model)
        elif choice == '3':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


