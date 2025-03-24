from typing import Optional

class ManualCaptchaSolver:
    async def solve_captcha(self, image_data: bytes) -> Optional[str]:
        # Save image temporarily
        import tempfile
        import os
        from PIL import Image
        import io

        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            tmp.write(image_data)
            tmp_path = tmp.name

        # Open image with default viewer
        Image.open(tmp_path).show()
        
        # Get manual input
        solution = input("Please enter captcha solution: ")
        
        # Clean up
        os.unlink(tmp_path)
        
        return solution if solution else None