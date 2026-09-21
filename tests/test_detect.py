from simreach_vision.detect import detect_color_blob, make_blank_frame, paint_rect


def test_detect_missing_on_blank():
    frame = make_blank_frame(64, 48)
    det = detect_color_blob(frame, min_area=5)
    assert det.found is False


def test_detect_red_blob_centroid():
    frame = make_blank_frame(100, 80, fill=(20, 20, 20))
    # 10x10 red square centered near (50, 40)
    paint_rect(frame, 45, 35, 54, 44, (220, 60, 60))
    det = detect_color_blob(frame, lo=(180, 40, 40), hi=(255, 120, 120), min_area=10)
    assert det.found is True
    assert abs(det.u - 49.5) < 0.6
    assert abs(det.v - 39.5) < 0.6
    assert det.area == 100
    assert det.score > 0


def test_make_blank_rejects_zero():
    try:
        make_blank_frame(0, 10)
        assert False, "expected ValueError"
    except ValueError:
        pass
