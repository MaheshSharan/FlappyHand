#hand_gesture.py
import cv2
import mediapipe as mp

class HandGesture:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.cap = cv2.VideoCapture(0)
        self.index_finger_y = None
        self.index_finger_x = None
        self.thumbs_up = False

    def get_hand_data(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None, None

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                self.draw_pipeline(frame, hand_landmarks, handedness.classification[0].label)

                thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                thumb_ip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_IP]
                index_finger = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

                self.index_finger_y = int(index_finger.y * frame.shape[0])
                self.index_finger_x = int(index_finger.x * frame.shape[1])

                if thumb_tip.y < thumb_ip.y:
                    self.thumbs_up = True
                else:
                    self.thumbs_up = False

        cv2.imshow('Hand Tracking', frame)
        cv2.waitKey(1)

        return self.index_finger_y, self.index_finger_x, self.thumbs_up

    def draw_pipeline(self, frame, hand_landmarks, handedness):
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8)  # Index
        ]

        for connection in connections:
            start = hand_landmarks.landmark[connection[0]]
            end = hand_landmarks.landmark[connection[1]]
            start_point = (int(start.x * frame.shape[1]), int(start.y * frame.shape[0]))
            end_point = (int(end.x * frame.shape[1]), int(end.y * frame.shape[0]))
            cv2.line(frame, start_point, end_point, (255, 105, 180), 2)
            cv2.circle(frame, start_point, 3, (255, 255, 255), -1)
            cv2.circle(frame, end_point, 3, (255, 255, 255), -1)

    def update(self):
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)