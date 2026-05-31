from ultralytics import YOLO
import cv2

model = YOLO("runs/classify/train-3/weights/best.pt")

cap = cv2.VideoCapture(0)

danger_classes = ["texting_phone", "talking_phone"]

while True:
    ret, frame = cap.read()

    results = model(frame)

    probs = results[0].probs.data.tolist()
    names = results[0].names

    max_index = probs.index(max(probs))

    label = names[max_index]
    confidence = probs[max_index]

    color = (0, 255, 0)

    if label in danger_classes and confidence > 0.5:
        color = (0, 0, 255)

        cv2.putText(
            frame,
            "WARNING: DISTRACTED DRIVING",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

    cv2.putText(
        frame,
        f"{label} ({confidence:.2f})",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2
    )

    cv2.imshow("AI Driver Monitoring System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()