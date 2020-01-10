class Colors:
    # 360/60=6
    # 6=x+1
    # x*60+/-30
    def rgb_convert_hsv(r, g, b):
        if r > 255 or g > 255 or b > 255:
            return "Error value > 255"
        max_color = max(r, g, b)
        min_color = min(r, g, b)

        if max_color == min_color:
            h = 0
        elif max_color == r and g >= b:
            h = 60 * (g - b) / (max_color - min_color) + 0
        elif max_color == r and g < b:
            h = 60 * (g - b) / (max_color - min_color) + 360
        elif max_color == g:
            h = 60 * (b - r) / (max_color - min_color) + 120
        elif max_color == b:
            h = 60 * (r - g) / (max_color - min_color) + 240

        if max_color == 0:
            s = 0
        else:
            s = 1 - (min_color / max_color)

        v = max_color / 255
        return h, s, v
