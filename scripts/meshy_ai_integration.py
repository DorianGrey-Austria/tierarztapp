#!/usr/bin/env python3
"""
MESHY AI INTEGRATION FOR ULTRA-REALISTIC ANIMALS
==================================================
Professional 3D model generation using Meshy AI API
Includes free trial and optimization for VetScan Pro
"""

import requests
import json
import time
import os
from pathlib import Path

class MeshyAIGenerator:
    """Generate ultra-realistic 3D animals using Meshy AI"""
    
    def __init__(self, api_key=None):
        # Use free trial if no key provided
        self.api_key = api_key or os.getenv('MESHY_API_KEY') or 'free-trial'
        self.base_url = 'https://api.meshy.ai/v2'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        self.output_dir = Path('/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/meshy')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def text_to_3d(self, prompt, animal_name, style='realistic'):
        """Generate 3D model from text prompt"""
        
        print(f"🎨 Generating {animal_name} with Meshy AI...")
        print(f"   Prompt: {prompt}")
        print(f"   Style: {style}")
        
        # Enhanced prompts for ultra-realistic animals
        enhanced_prompt = self._enhance_prompt(prompt, style)
        
        # Create generation request
        payload = {
            'prompt': enhanced_prompt,
            'mode': 'preview',  # or 'refine' for higher quality
            'art_style': style,
            'negative_prompt': 'low quality, low poly, cartoon, anime, blurry',
            'ai_model': 'meshy-4'  # Latest model
        }
        
        try:
            # Start generation
            response = requests.post(
                f'{self.base_url}/text-to-3d',
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 402:
                print("⚠️ Using free tier limits. Switching to procedural generation...")
                return self._procedural_fallback(animal_name)
                
            response.raise_for_status()
            task_id = response.json()['result']
            
            print(f"   Task ID: {task_id}")
            
            # Poll for completion
            model_url = self._wait_for_completion(task_id)
            
            if model_url:
                # Download model
                return self._download_model(model_url, animal_name)
            else:
                return self._procedural_fallback(animal_name)
                
        except Exception as e:
            print(f"❌ Meshy AI Error: {e}")
            return self._procedural_fallback(animal_name)
            
    def _enhance_prompt(self, base_prompt, style):
        """Enhance prompt for better quality"""
        
        style_modifiers = {
            'realistic': 'photorealistic, highly detailed, anatomically correct, professional 3D model, PBR textures',
            'medical': 'anatomically accurate, medical visualization, scientific accuracy, clean topology',
            'game': 'game-ready, optimized topology, clean UV mapping, low poly but detailed'
        }
        
        modifier = style_modifiers.get(style, style_modifiers['realistic'])
        return f"{base_prompt}, {modifier}"
        
    def _wait_for_completion(self, task_id, max_wait=300):
        """Poll for task completion"""
        
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            response = requests.get(
                f'{self.base_url}/text-to-3d/{task_id}',
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                status = data.get('status')
                
                if status == 'SUCCEEDED':
                    print("✅ Generation complete!")
                    return data['model_urls']['glb']
                elif status == 'FAILED':
                    print("❌ Generation failed")
                    return None
                else:
                    print(f"   Status: {status}... ({int(data.get('progress', 0))}%)")
                    
            time.sleep(5)
            
        print("⏱️ Generation timeout")
        return None
        
    def _download_model(self, url, name):
        """Download the generated model"""
        
        output_path = self.output_dir / f"{name}_meshy.glb"
        
        print(f"📥 Downloading model to {output_path}")
        
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Model saved: {output_path}")
            return str(output_path)
        else:
            print("❌ Download failed")
            return None
            
    def _procedural_fallback(self, animal_name):
        """Fallback to procedural generation"""
        
        print("🔄 Using procedural fallback generation...")
        
        # Import our procedural generator
        import sys
        sys.path.append('/Users/doriangrey/Desktop/coding/tierarztspiel/scripts')
        from blender_parametric_animals import ParametricAnimalGenerator
        
        # Generate procedural model
        generator = ParametricAnimalGenerator()
        
        if animal_name == 'dog':
            generator.create_parametric_dog()
        elif animal_name == 'cat':
            generator.create_parametric_cat()
        else:
            generator.create_generic_animal(animal_name)
            
        # Export
        export_path = generator.export_for_web()
        return export_path
        
    def generate_all_animals(self):
        """Generate all animals for VetScan Pro"""
        
        animals = [
            {
                'name': 'dog',
                'prompt': 'Golden Retriever dog, standing pose, friendly expression',
                'style': 'realistic'
            },
            {
                'name': 'cat',
                'prompt': 'Persian cat, sitting, fluffy fur, elegant pose',
                'style': 'realistic'
            },
            {
                'name': 'rabbit',
                'prompt': 'Dutch rabbit, white and brown fur, long ears, sitting',
                'style': 'realistic'
            },
            {
                'name': 'horse',
                'prompt': 'Arabian horse, standing, muscular, brown coat',
                'style': 'realistic'
            },
            {
                'name': 'parrot',
                'prompt': 'Scarlet Macaw parrot, colorful feathers, perched',
                'style': 'realistic'
            },
            {
                'name': 'turtle',
                'prompt': 'Red-eared slider turtle, detailed shell pattern',
                'style': 'realistic'
            },
            {
                'name': 'snake',
                'prompt': 'Ball python snake, coiled position, detailed scales',
                'style': 'realistic'
            },
            {
                'name': 'hamster',
                'prompt': 'Golden hamster, chubby cheeks, small paws',
                'style': 'realistic'
            },
            {
                'name': 'guinea_pig',
                'prompt': 'Guinea pig, tri-color fur, rounded body',
                'style': 'realistic'
            },
            {
                'name': 'goldfish',
                'prompt': 'Fancy goldfish, flowing fins, orange scales',
                'style': 'realistic'
            }
        ]
        
        results = []
        for animal in animals:
            print(f"\n{'='*50}")
            print(f"Generating {animal['name']}...")
            print('='*50)
            
            result = self.text_to_3d(
                prompt=animal['prompt'],
                animal_name=animal['name'],
                style=animal['style']
            )
            
            results.append({
                'name': animal['name'],
                'path': result,
                'success': result is not None
            })
            
        # Summary
        print(f"\n{'='*60}")
        print("GENERATION SUMMARY")
        print('='*60)
        
        for r in results:
            status = "✅" if r['success'] else "❌"
            print(f"{status} {r['name']}: {r['path']}")
            
        return results


class MeshyAPIWrapper:
    """Wrapper for easy integration with Blender MCP"""
    
    @staticmethod
    def quick_generate(animal_type='dog'):
        """Quick generation for testing"""
        
        prompts = {
            'dog': 'Realistic golden retriever dog, standing, detailed fur',
            'cat': 'Realistic tabby cat, sitting, detailed whiskers',
            'rabbit': 'Realistic white rabbit, long ears, fluffy tail',
            'horse': 'Realistic brown horse, standing, muscular build',
            'parrot': 'Colorful macaw parrot, spread wings, detailed feathers'
        }
        
        generator = MeshyAIGenerator()
        prompt = prompts.get(animal_type, f'Realistic {animal_type}')
        
        return generator.text_to_3d(prompt, animal_type, 'realistic')
        

# Integration with Blender
def integrate_with_blender():
    """Code to run inside Blender via MCP"""
    
    import bpy
    import os
    
    # Generate animal with Meshy
    generator = MeshyAIGenerator()
    model_path = generator.quick_generate('dog')
    
    if model_path and os.path.exists(model_path):
        # Import into Blender
        bpy.ops.import_scene.gltf(filepath=model_path)
        
        # Get imported object
        imported_objects = bpy.context.selected_objects
        
        if imported_objects:
            obj = imported_objects[0]
            obj.name = "MeshyAI_Dog"
            
            # Center and scale
            obj.location = (0, 0, 0)
            obj.scale = (1, 1, 1)
            
            print(f"✅ Model imported: {obj.name}")
            
            # Add medical materials
            from blender_parametric_animals import ParametricAnimalGenerator
            generator = ParametricAnimalGenerator()
            generator.apply_xray_material(obj)
            
            return True
    
    return False


if __name__ == "__main__":
    print("="*60)
    print("🚀 MESHY AI ULTRA-REALISTIC ANIMAL GENERATOR")
    print("="*60)
    
    # Test single generation
    generator = MeshyAIGenerator()
    
    # Quick test
    print("\n🐕 Testing single dog generation...")
    result = MeshyAPIWrapper.quick_generate('dog')
    
    if result:
        print(f"✅ Success! Model at: {result}")
    else:
        print("❌ Generation failed, using fallback")
    
    # Optional: Generate all
    # generator.generate_all_animals()