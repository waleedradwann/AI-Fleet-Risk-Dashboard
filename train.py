from ultralytics import YOLO

model = YOLO("/Users/waleedradwann/Desktop/AI Fleet Dashboard/yolov8n-cls.pt")
model.train(
    data="/Users/waleedradwann/Desktop/AI Fleet Dashboard/Revitsone-5classes",
    epochs=1,
    imgsz=224
)