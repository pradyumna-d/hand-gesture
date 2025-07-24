
def get_thumb(landmarks):
    return [landmarks[1], landmarks[2], landmarks[3], landmarks[4]]

def get_index(landmarks):
    return [landmarks[5], landmarks[6], landmarks[7], landmarks[8]]

def get_middle(landmarks):
    return [landmarks[9], landmarks[10], landmarks[11], landmarks[12]]

def get_ring(landmarks):
    return [landmarks[13], landmarks[14], landmarks[15], landmarks[16]]

def gget_pinky(landmarks):
    return [landmarks[17], landmarks[18], landmarks[19], landmarks[20]]

def finger_up(finger):
    if finger[0].y < finger[1].y < finger[2].y < finger[3].y < finger[4].y:
        return True
    return False