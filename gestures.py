import hand_utils

def get_gesture(landmarks):
    """
        Determine hand gesture based on finger landmarks.

        Args:
            landmarks: List of hand landmarks from MediaPipe.

        Returns:
            str: Detected gesture name or "Unknown Gesture" if no match.
        """
    if not landmarks:
        return "No Hand"
    thumb = hand_utils.get_thumb(landmarks)
    index_finger = hand_utils.get_index(landmarks)
    middle_finger = hand_utils.get_middle(landmarks)
    ring_finger = hand_utils.get_ring(landmarks)
    pinky_finger = hand_utils.get_pinky(landmarks)

    # OK: Thumb, middle, ring, pinky up; index down
    if (hand_utils.is_up(thumb) and
            hand_utils.is_up(middle_finger) and
            hand_utils.is_up(ring_finger) and
            hand_utils.is_up(pinky_finger) and
            not hand_utils.is_up(index_finger)):
        return "OK"

    # Rock 'n' Roll: Index & pinky up, middle and ring down
    elif (hand_utils.is_up(index_finger) and
          not hand_utils.is_up(middle_finger) and
          not hand_utils.is_up(ring_finger) and
          hand_utils.is_up(pinky_finger)):
        return "Rock 'n' Roll"

    elif (hand_utils.is_up(middle_finger) and
        not hand_utils.is_up(index_finger) and
        not hand_utils.is_up(ring_finger) and
        not hand_utils.is_up(pinky_finger)):
        return "Fuck You!"

    return "Unknown Gesture"
