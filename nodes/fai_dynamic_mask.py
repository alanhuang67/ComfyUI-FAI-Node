import numpy as np
import cv2
import torch

class FAIDynamicMask:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 1}),
                "height": ("INT", {"default": 512, "min": 1}),
                "frame_count": ("INT", {"default": 30, "min": 1}),
                "shape_transition": ([
                    "fade_in", "fade_out",
                    "circle_out", "circle_in",
                    "square_out", "square_in",
                    "diamond_out", "diamond_in",
                    "left_to_right", "right_to_left",
                    "top_to_bottom", "bottom_to_top"
                ],),
                "feather": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0}),
                "ease": (["linear", "ease_in", "ease_out", "ease_in_out"],)
            },
        }

    RETURN_TYPES = ("MASK", "MASK")
    RETURN_NAMES = ("mask", "invert_mask")
    FUNCTION = "generate_mask"
    CATEGORY = "⚛️FAI_Node⚛️"

    def generate_mask(self, width, height, frame_count, shape_transition, feather, ease):
        mask_sequence = []
        invert_mask_sequence = []

        for frame in range(frame_count):
            mask = self.create_mask(frame, frame_count, shape_transition, width, height, feather, ease)
            invert_mask = 1 - mask
            mask_sequence.append(mask)
            invert_mask_sequence.append(invert_mask)

        return (torch.stack(mask_sequence), torch.stack(invert_mask_sequence))

    def create_mask(self, frame, frame_count, shape_transition, width, height, feather, ease):
        mask = np.zeros((height, width), dtype=np.float32)
        t = frame / (frame_count - 1)

        if ease == "linear":
            progress = t
        elif ease == "ease_in":
            progress = t ** 2.0
        elif ease == "ease_out":
            progress = t ** (1 / 2.0)
        elif ease == "ease_in_out":
            progress = (np.sin((t - 0.5) * np.pi) / 2) + 0.5

        if shape_transition == "fade_in":
            mask[:, :] = progress
        elif shape_transition == "fade_out":
            mask[:, :] = 1 - progress
            
        elif shape_transition == "circle_out":
            max_dim = np.sqrt(width ** 2 + height ** 2)
            radius = progress * (max_dim / 2) + 2  # 增加2像素以确保覆盖
            center = (width // 2, height // 2)
            mask = cv2.circle(mask, center, int(radius), 1, -1)

        elif shape_transition == "square_out":
            max_dim = max(width, height)
            side = progress * max_dim + 2  # 增加2像素以确保覆盖
            top_left = (int(width // 2 - side // 2), int(height // 2 - side // 2))
            bottom_right = (int(width // 2 + side // 2), int(height // 2 + side // 2))
            mask = cv2.rectangle(mask, top_left, bottom_right, 1, -1)

        elif shape_transition == "circle_in":
            max_dim = np.sqrt(width ** 2 + height ** 2)
            radius = (1 - progress) * (max_dim / 2)
            center = (width // 2, height // 2)
            mask = cv2.circle(mask, center, int(radius), 1, -1)
            mask = 1 - mask

        elif shape_transition == "square_in":
            max_dim = max(width, height)
            side = (1 - progress) * max_dim
            top_left = (int(width // 2 - side // 2), int(height // 2 - side // 2))
            bottom_right = (int(width // 2 + side // 2), int(height // 2 + side // 2))
            mask = cv2.rectangle(mask, top_left, bottom_right, 1, -1)
            mask = 1 - mask

        elif shape_transition == "diamond_out":
            diag_length = np.sqrt(width ** 2 + height ** 2)
            side = progress * diag_length * np.sqrt(2)  # 将边长乘以√2以确保对角线等于画布对角线
            points = np.array([[
                (width // 2, height // 2 - side // 2),  # Top
                (width // 2 + side // 2, height // 2),  # Right
                (width // 2, height // 2 + side // 2),  # Bottom
                (width // 2 - side // 2, height // 2)   # Left
            ]], dtype=np.int32)
            mask = cv2.fillPoly(mask, points, 1)

        elif shape_transition == "diamond_in":
            diag_length = np.sqrt(width ** 2 + height ** 2)
            side = (1 - progress) * diag_length * np.sqrt(2)  # 将边长乘以√2以确保对角线等于画布对角线
            points = np.array([[
                (width // 2, height // 2 - side // 2),  # Top
                (width // 2 + side // 2, height // 2),  # Right
                (width // 2, height // 2 + side // 2),  # Bottom
                (width // 2 - side // 2, height // 2)   # Left
            ]], dtype=np.int32)
            mask = cv2.fillPoly(mask, points, 1)
            mask = 1 - mask


        elif shape_transition == "left_to_right":
            max_dim = width
            mask = cv2.rectangle(mask, (0, 0), (int(progress * max_dim), height), 1, -1)

        elif shape_transition == "right_to_left":
            max_dim = width
            mask = cv2.rectangle(mask, (int((1 - progress) * max_dim), 0), (width, height), 1, -1)

        elif shape_transition == "top_to_bottom":
            max_dim = height
            mask = cv2.rectangle(mask, (0, 0), (width, int(progress * max_dim)), 1, -1)

        elif shape_transition == "bottom_to_top":
            max_dim = height
            mask = cv2.rectangle(mask, (0, int((1 - progress) * max_dim)), (width, height), 1, -1)



        if feather > 0:
            mask = cv2.GaussianBlur(mask, (0, 0), feather * min(width, height))

        mask[mask < 1e-3] = 0

        return torch.tensor(mask).unsqueeze(0)


# 节点映射
NODE_CLASS_MAPPINGS = {
    "FAIDynamicMask": FAIDynamicMask
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FAIDynamicMask": "⚛️FAI Dynamic Mask⚛️"
}
