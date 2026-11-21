import unittest
from core.generator import generate_texture


class TextureGeneratorTests(unittest.TestCase):
    def test_all_materials_generate_rgb_images(self):
        for material in ("concrete", "wood", "metal", "wallpaper"):
            image = generate_texture(material, size=256, seed=42)
            self.assertEqual(image.size, (256, 256))
            self.assertEqual(image.mode, "RGB")

    def test_invalid_resolution_is_rejected(self):
        with self.assertRaises(ValueError):
            generate_texture(size=300)


if __name__ == "__main__":
    unittest.main()
