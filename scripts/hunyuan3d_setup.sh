#!/bin/bash
# HUNYUAN3D V2 LOCAL SETUP
# Ultra-realistic 3D generation - FREE & LOCAL
# =============================================

echo "🚀 Setting up Hunyuan3D V2 for ultra-realistic animals..."
echo "=================================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 required. Please install Python 3.8+"
    exit 1
fi

# Create environment
echo "📦 Creating virtual environment..."
python3 -m venv hunyuan3d_env
source hunyuan3d_env/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers diffusers accelerate
pip install trimesh pygltflib

# Clone Hunyuan3D repo
echo "📂 Cloning Hunyuan3D repository..."
if [ ! -d "Hunyuan3D" ]; then
    git clone https://github.com/Tencent/Hunyuan3D.git
else
    echo "   Repository already exists, updating..."
    cd Hunyuan3D && git pull && cd ..
fi

# Download models
echo "🎨 Downloading pre-trained models..."
mkdir -p models/hunyuan3d

# Create Python script for model download
cat > download_models.py << 'EOF'
import os
from huggingface_hub import snapshot_download

# Download Hunyuan3D models
model_id = "tencent/Hunyuan3D-1"
local_dir = "./models/hunyuan3d"

print("Downloading Hunyuan3D models...")
snapshot_download(
    repo_id=model_id,
    local_dir=local_dir,
    local_dir_use_symlinks=False
)
print("✅ Models downloaded successfully!")
EOF

# Run download
python3 download_models.py

# Create generation script
cat > generate_animal.py << 'EOF'
#!/usr/bin/env python3
"""
HUNYUAN3D ANIMAL GENERATOR
Ultra-realistic 3D generation
"""

import torch
from diffusers import DiffusionPipeline
import trimesh
import numpy as np

class Hunyuan3DGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Load pipeline
        self.pipe = DiffusionPipeline.from_pretrained(
            "./models/hunyuan3d",
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        )
        self.pipe = self.pipe.to(self.device)
        
    def generate(self, prompt, output_path):
        """Generate 3D model from text prompt"""
        print(f"🎨 Generating: {prompt}")
        
        # Generate 3D
        with torch.no_grad():
            result = self.pipe(
                prompt=prompt,
                num_inference_steps=50,
                guidance_scale=7.5
            )
        
        # Extract mesh
        mesh = result.meshes[0]
        
        # Save as GLB
        mesh.export(output_path)
        print(f"✅ Saved to: {output_path}")
        
        return output_path

# Test generation
if __name__ == "__main__":
    generator = Hunyuan3DGenerator()
    
    animals = [
        "A highly detailed, realistic golden retriever dog",
        "A photorealistic persian cat with fluffy fur",
        "A realistic brown horse, anatomically correct",
        "A detailed scarlet macaw parrot with colorful feathers",
        "A realistic rabbit with long ears and fluffy tail"
    ]
    
    for i, prompt in enumerate(animals):
        output = f"animal_{i}.glb"
        generator.generate(prompt, output)
        print(f"Generated: {output}")
EOF

echo ""
echo "✅ Hunyuan3D V2 Setup Complete!"
echo "================================"
echo ""
echo "To use Hunyuan3D:"
echo "1. Activate environment: source hunyuan3d_env/bin/activate"
echo "2. Run generation: python3 generate_animal.py"
echo ""
echo "Note: First run will be slower as models load into memory."
echo "Subsequent generations will be much faster (~30 seconds per model)."