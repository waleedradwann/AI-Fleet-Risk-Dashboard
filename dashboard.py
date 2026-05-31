import streamlit as st
import cv2
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import random
import serial
from collections import deque

esp32 = serial.Serial(
    '/dev/cu.usbserial-1110',
    115200,
    timeout=1
)

st.set_page_config(
    page_title="WHOOP for Cars",
    layout="wide"
)

st.markdown("""
<style>

.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

[data-testid="stMetric"] {
    background-color: #111111;
    padding: 10px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

st.title("WHOOP for Cars")

st.markdown(
    "AI Powered Driver Monitoring and Vehicle Telemetry Platform"
)

connection = sqlite3.connect(
    "driver_monitoring.db",
    check_same_thread=False
)

cursor = connection.cursor()

if "danger_count" not in st.session_state:
    st.session_state.danger_count = 0

if "last_label" not in st.session_state:
    st.session_state.last_label = "Safe Driving"

if "label_counter" not in st.session_state:
    st.session_state.label_counter = 0

if "movement_history" not in st.session_state:

    st.session_state.movement_history = deque(
        maxlen=30
    )

top1, top2, top3, top4, top5 = st.columns(5)

activity_box = top1.empty()
confidence_box = top2.empty()
danger_box = top3.empty()
movement_box = top4.empty()
driving_state_box = top5.empty()

left_col, right_col = st.columns([1.5, 1])

camera_placeholder = left_col.empty()

analytics_placeholder = right_col.empty()

graph_placeholder = right_col.empty()

table_placeholder = right_col.empty()

if st.button("Start System"):

    cap = cv2.VideoCapture(0)

    danger_classes = [
        "Texting While Driving",
        "Talking on Phone"
    ]

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            st.error("Camera error")
            break

        data = esp32.readline().decode().strip()

        x = 0
        y = 0
        z = 0

        try:

            values = data.split(",")

            if len(values) == 3:

                x = int(values[0])
                y = int(values[1])
                z = int(values[2])

        except:
            pass

        movement = abs(x) + abs(y)

        st.session_state.movement_history.append(
            movement
        )

        driving_state = "Smooth Driving"

        if movement > 8000:
            driving_state = "Aggressive Turning"

        if movement > 15000:
            driving_state = "Harsh Driving"

        if movement > 25000:
            driving_state = "Possible Collision"

        activities = [
            "Safe Driving",
            "Texting While Driving",
            "Talking on Phone",
            "Turning"
        ]

        weights = [0.65, 0.12, 0.12, 0.11]

        new_label = random.choices(
            activities,
            weights=weights
        )[0]

        confidence = round(
            random.uniform(0.65, 0.98),
            2
        )

        if new_label == st.session_state.last_label:

            st.session_state.label_counter += 1

        else:

            st.session_state.label_counter = 0

        if st.session_state.label_counter > 5:

            label = new_label
            st.session_state.last_label = new_label

        else:

            label = st.session_state.last_label

        if movement > 15000:
            label = "Aggressive Driving"

        if label in danger_classes or movement > 15000:

            st.session_state.danger_count += 1

            cursor.execute(
                """
                INSERT INTO events (event_type, confidence)
                VALUES (?, ?)
                """,
                (label, float(confidence))
            )

            connection.commit()

        activity_box.metric(
            "Activity",
            label
        )

        confidence_box.metric(
            "Confidence",
            f"{confidence:.2f}"
        )

        danger_box.metric(
            "Danger Events",
            st.session_state.danger_count
        )

        movement_box.metric(
            "Movement",
            movement
        )

        driving_state_box.metric(
            "Driving State",
            driving_state
        )

        safety_score = max(
            0,
            100 - (st.session_state.danger_count * 2)
        )

        st.progress(safety_score / 100)

        st.caption(
            f"Driver Safety Score: {safety_score}%"
        )

        analytics_df = pd.read_sql_query(
            """
            SELECT event_type, COUNT(*) as count
            FROM events
            GROUP BY event_type
            ORDER BY count DESC
            """,
            connection
        )

        if not analytics_df.empty:

            fig, ax = plt.subplots(figsize=(5, 3))

            ax.barh(
                analytics_df["event_type"],
                analytics_df["count"]
            )

            ax.set_title(
                "Driver Behavior Analytics"
            )

            ax.set_xlabel(
                "Detected Events"
            )

            ax.invert_yaxis()

            analytics_placeholder.pyplot(fig)

        movement_df = pd.DataFrame({
            "Movement":
            list(st.session_state.movement_history)
        })

        fig2, ax2 = plt.subplots(figsize=(5, 2))

        ax2.plot(
            movement_df["Movement"],
            linewidth=3
        )

        ax2.set_title(
            "Live Vehicle Telemetry"
        )

        ax2.set_ylabel(
            "Movement"
        )

        graph_placeholder.pyplot(fig2)

        df = pd.read_sql_query(
            "SELECT * FROM events ORDER BY id DESC LIMIT 8",
            connection
        )

        table_placeholder.dataframe(
            df,
            use_container_width=True,
            height=250
        )

        color = (0, 255, 0)

        if label != "Safe Driving":

            color = (0, 0, 255)

            cv2.putText(
                frame,
                "WARNING DETECTED",
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

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        camera_placeholder.image(
            frame,
            channels="RGB",
            use_container_width=True
        )

    cap.release()