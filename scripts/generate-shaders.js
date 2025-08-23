#!/usr/bin/env node
// Datei: scripts/generate-shaders.js
// Generator für medizinische Visualisierungs-Shader

import fs from 'fs';
import path from 'path';

const SHADER_TEMPLATES = {
  xray: {
    name: 'X-Ray Visualization',
    description: 'Röntgen-Visualization mit Fresnel-basierten Effekten',
    vertex: `
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec2 vUv;
      
      void main() {
        vNormal = normalize(normalMatrix * normal);
        vPosition = (modelViewMatrix * vec4(position, 1.0)).xyz;
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragment: `
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec2 vUv;
      uniform float time;
      uniform float intensity;
      uniform vec3 boneColor;
      uniform vec3 tissueColor;
      
      void main() {
        // Fresnel-Effekt für realistische Transparenz
        vec3 viewDirection = normalize(-vPosition);
        float fresnel = 1.0 - max(0.0, dot(viewDirection, vNormal));
        
        // Tiefenbasierte Intensität
        float depth = length(vPosition) / 15.0;
        float depthFade = exp(-depth * 0.8);
        
        // Knochen-Simulation (höhere Dichte = heller)
        float boneIntensity = smoothstep(0.2, 0.9, fresnel);
        float tissueIntensity = 1.0 - boneIntensity;
        
        // Röntgen-Farbmischung
        vec3 xrayColor = mix(tissueColor, boneColor, boneIntensity);
        
        // Pulsierender Scan-Effekt
        float pulse = 0.8 + 0.2 * sin(time * 3.0);
        
        float alpha = fresnel * intensity * depthFade * pulse;
        
        gl_FragColor = vec4(xrayColor, alpha);
      }
    `,
    uniforms: {
      time: 0.0,
      intensity: 0.8,
      boneColor: [1.0, 1.0, 1.0],
      tissueColor: [0.3, 0.3, 0.5]
    }
  },

  ultrasound: {
    name: 'Ultrasound Visualization',
    description: 'Ultraschall mit realistischen Noise- und Scan-Effekten',
    vertex: `
      varying vec2 vUv;
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec3 vWorldPosition;
      
      void main() {
        vUv = uv;
        vPosition = (modelViewMatrix * vec4(position, 1.0)).xyz;
        vNormal = normalize(normalMatrix * normal);
        vWorldPosition = (modelMatrix * vec4(position, 1.0)).xyz;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragment: `
      varying vec2 vUv;
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec3 vWorldPosition;
      uniform float time;
      uniform float scanIntensity;
      uniform vec3 scanDirection;
      uniform float frequency;
      uniform float amplitude;
      
      // Perlin-ähnliche Noise-Funktion
      float hash(vec2 p) {
        return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
      }
      
      float noise(vec2 p) {
        vec2 i = floor(p);
        vec2 f = fract(p);
        vec2 u = f * f * (3.0 - 2.0 * f);
        
        return mix(
          mix(hash(i + vec2(0.0,0.0)), hash(i + vec2(1.0,0.0)), u.x),
          mix(hash(i + vec2(0.0,1.0)), hash(i + vec2(1.0,1.0)), u.x), 
          u.y
        );
      }
      
      float fbm(vec2 p) {
        float value = 0.0;
        float amplitude = 0.5;
        for (int i = 0; i < 6; i++) {
          value += amplitude * noise(p);
          p *= 2.0;
          amplitude *= 0.5;
        }
        return value;
      }
      
      void main() {
        // Ultraschall-Scan-Linien
        float scanPos = dot(vWorldPosition, scanDirection) + time * 2.0;
        float scanLine = sin(scanPos * frequency) * 0.5 + 0.5;
        
        // Multi-Oktav-Noise für realistische Textur
        vec2 noiseCoord = vUv * 80.0 + time * 0.05;
        float noiseValue = fbm(noiseCoord);
        
        // Tiefenbasierte Dämpfung (akustische Absorption)
        float depth = length(vPosition) / 12.0;
        float attenuation = exp(-depth * 1.2);
        
        // Akustische Schatten und Reflexionen
        float reflection = max(0.0, dot(vNormal, scanDirection));
        float shadowFactor = smoothstep(0.0, 1.0, reflection);
        
        // Gewebedichte-Simulation
        float tissueDensity = 0.3 + 0.7 * noiseValue;
        
        // Ultraschall-Intensität berechnen
        float intensity = scanLine * noiseValue * attenuation * shadowFactor * scanIntensity;
        intensity *= tissueDensity;
        
        // Dynamische Helligkeit basierend auf Tiefe
        float brightness = mix(0.9, 0.1, depth);
        
        // Ultraschall-Farbe (monochrom mit leichter Tönung)
        vec3 ultrasoundColor = vec3(intensity * brightness);
        ultrasoundColor.b += 0.1; // Leichte bläuliche Tönung
        
        // Grain-Effekt für Realismus
        float grain = hash(vUv * 1000.0 + time) * 0.05;
        ultrasoundColor += grain;
        
        gl_FragColor = vec4(ultrasoundColor, 1.0);
      }
    `,
    uniforms: {
      time: 0.0,
      scanIntensity: 0.7,
      scanDirection: [0.0, 0.0, 1.0],
      frequency: 15.0,
      amplitude: 1.0
    }
  },

  thermal: {
    name: 'Thermal Imaging',
    description: 'Wärmebild-Visualization mit realistischer Farbverteilung',
    vertex: `
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec2 vUv;
      varying vec3 vWorldPosition;
      
      void main() {
        vPosition = (modelViewMatrix * vec4(position, 1.0)).xyz;
        vNormal = normalize(normalMatrix * normal);
        vUv = uv;
        vWorldPosition = (modelMatrix * vec4(position, 1.0)).xyz;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragment: `
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec2 vUv;
      varying vec3 vWorldPosition;
      uniform float time;
      uniform float minTemp;
      uniform float maxTemp;
      uniform vec3 corePosition;
      uniform float heatRadius;
      
      // Erweiterte Temperatur-zu-Farbe Konvertierung
      vec3 temperatureToColor(float temp) {
        temp = clamp(temp, 0.0, 1.0);
        
        // Definiere Farbstufen (von kalt zu heiß)
        vec3 colors[7];
        colors[0] = vec3(0.0, 0.0, 0.3);    // Sehr kalt - Dunkelblau
        colors[1] = vec3(0.0, 0.0, 1.0);    // Kalt - Blau
        colors[2] = vec3(0.0, 1.0, 1.0);    // Kühl - Cyan
        colors[3] = vec3(0.0, 1.0, 0.0);    // Normal - Grün
        colors[4] = vec3(1.0, 1.0, 0.0);    // Warm - Gelb
        colors[5] = vec3(1.0, 0.5, 0.0);    // Heiß - Orange
        colors[6] = vec3(1.0, 0.0, 0.0);    // Sehr heiß - Rot
        
        float scaledTemp = temp * 6.0;
        int index = int(floor(scaledTemp));
        float frac = fract(scaledTemp);
        
        if (index >= 6) return colors[6];
        if (index < 0) return colors[0];
        
        return mix(colors[index], colors[index + 1], frac);
      }
      
      // Noise für realistische Temperaturschwankungen
      float random(vec2 st) {
        return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
      }
      
      float noise(vec2 st) {
        vec2 i = floor(st);
        vec2 f = fract(st);
        
        float a = random(i);
        float b = random(i + vec2(1.0, 0.0));
        float c = random(i + vec2(0.0, 1.0));
        float d = random(i + vec2(1.0, 1.0));
        
        vec2 u = f * f * (3.0 - 2.0 * f);
        
        return mix(a, b, u.x) + 
               (c - a) * u.y * (1.0 - u.x) + 
               (d - b) * u.x * u.y;
      }
      
      void main() {
        // Basis-Körpertemperatur (höher im Zentrum)
        float distanceFromCore = distance(vWorldPosition, corePosition);
        float coreTemperature = exp(-distanceFromCore / heatRadius);
        
        // Höhere Temperatur in Kopf und Brustbereich
        float headFactor = max(0.0, vWorldPosition.y - 0.5) * 0.3;
        float chestFactor = exp(-abs(vWorldPosition.y) * 2.0) * 0.2;
        
        // Oberflächennormale beeinflusst Wärmeabstrahlung
        float surfaceFactor = max(0.0, dot(vNormal, vec3(0, 1, 0))) * 0.2;
        
        // Pulsierender Herzschlag-Effekt
        float heartbeat = 0.95 + 0.05 * sin(time * 8.0); // ~120 BPM
        
        // Atmungs-Simulation
        float breathing = 1.0 + 0.03 * sin(time * 1.5); // ~20 Atemzüge/min
        
        // Noise für natürliche Variation
        vec2 noiseCoord = vUv * 10.0 + time * 0.02;
        float temperatureNoise = noise(noiseCoord) * 0.1;
        
        // Finale Temperaturberechnung
        float temperature = coreTemperature + headFactor + chestFactor + surfaceFactor;
        temperature *= heartbeat * breathing;
        temperature += temperatureNoise;
        
        // Temperatur in 0-1 Bereich normalisieren
        temperature = (temperature - minTemp) / (maxTemp - minTemp);
        temperature = clamp(temperature, 0.0, 1.0);
        
        // Zu Farbe konvertieren
        vec3 thermalColor = temperatureToColor(temperature);
        
        // Subtile Glüheffekte für heiße Bereiche
        if (temperature > 0.8) {
          float glow = (temperature - 0.8) * 5.0;
          thermalColor += vec3(glow * 0.2, glow * 0.1, 0.0);
        }
        
        gl_FragColor = vec4(thermalColor, 1.0);
      }
    `,
    uniforms: {
      time: 0.0,
      minTemp: 0.0,
      maxTemp: 1.0,
      corePosition: [0.0, 0.0, 0.0],
      heatRadius: 2.0
    }
  },

  mri: {
    name: 'MRI Visualization',
    description: 'MRT-Simulation mit Gewebedifferenzierung',
    vertex: `
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec2 vUv;
      varying vec3 vViewPosition;
      
      void main() {
        vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
        vViewPosition = -mvPosition.xyz;
        vPosition = (modelMatrix * vec4(position, 1.0)).xyz;
        vNormal = normalize(normalMatrix * normal);
        vUv = uv;
        gl_Position = projectionMatrix * mvPosition;
      }
    `,
    fragment: `
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec2 vUv;
      varying vec3 vViewPosition;
      uniform float time;
      uniform float t1Weighting;
      uniform float t2Weighting;
      uniform float protonDensity;
      
      // Simuliert verschiedene Gewebetypen
      float getT1Value(vec3 pos) {
        // Knochen: kurze T1
        float bone = step(0.8, length(pos.xz));
        
        // Weichgewebe: mittlere T1
        float tissue = 1.0 - bone;
        
        // Fett: sehr kurze T1
        float fat = smoothstep(0.3, 0.5, sin(pos.x * 10.0) * cos(pos.z * 8.0)) * tissue;
        
        return bone * 0.2 + tissue * 0.6 + fat * 0.1;
      }
      
      float getT2Value(vec3 pos) {
        // Wasser/Flüssigkeiten: lange T2
        float fluid = smoothstep(0.0, 0.3, pos.y) * 0.9;
        
        // Weichgewebe: mittlere T2
        float tissue = 0.5;
        
        // Knochen: sehr kurze T2
        float bone = step(0.8, length(pos.xz)) * 0.1;
        
        return max(fluid, max(tissue, bone));
      }
      
      float getProtonDensity(vec3 pos) {
        // Höhere Dichte in Weichgewebe und Flüssigkeiten
        return 0.3 + 0.7 * smoothstep(-1.0, 1.0, sin(pos.x * 3.0) * cos(pos.y * 2.0));
      }
      
      void main() {
        float t1 = getT1Value(vPosition);
        float t2 = getT2Value(vPosition);
        float pd = getProtonDensity(vPosition);
        
        // MRI-Signal basierend auf Relaxationszeiten
        float signal = pd * (1.0 - exp(-t1Weighting / max(t1, 0.01))) * exp(-t2Weighting / max(t2, 0.01));
        
        // Phasen-Kodierung Simulation
        float phase = sin(vPosition.x * 5.0 + time * 0.1) * 0.1;
        signal += phase;
        
        // Frequenz-Kodierung
        float frequency = cos(vPosition.y * 8.0) * 0.05;
        signal += frequency;
        
        // MRI typische Graustufen mit leichtem Kontrast
        vec3 mriColor = vec3(signal);
        
        // Kontrast-Enhancement für bessere Sichtbarkeit
        mriColor = pow(mriColor, vec3(0.8));
        mriColor = mriColor * 1.2 - 0.1;
        
        gl_FragColor = vec4(clamp(mriColor, 0.0, 1.0), 1.0);
      }
    `,
    uniforms: {
      time: 0.0,
      t1Weighting: 500.0,
      t2Weighting: 80.0,
      protonDensity: 1.0
    }
  }
};

function generateShaderFile(shaderName, shaderData, outputDir) {
  const shaderCode = `
// Auto-generated medical visualization shader: ${shaderData.name}
// ${shaderData.description}
// Generated on: ${new Date().toISOString()}

export const ${shaderName}Shader = {
  name: '${shaderData.name}',
  description: '${shaderData.description}',
  
  vertexShader: \`${shaderData.vertex.trim()}\`,
  
  fragmentShader: \`${shaderData.fragment.trim()}\`,
  
  uniforms: ${JSON.stringify(shaderData.uniforms, null, 4).replace(/"/g, '').replace(/:/g, ': { value:').replace(/,/g, ' },').replace(/}$/, ' }\n  }')},
  
  // Animation update function
  updateUniforms: (uniforms, time, params = {}) => {
    if (uniforms.time) uniforms.time.value = time;
    
    // Shader-specific parameter updates
    ${generateUpdateLogic(shaderName)}
  },
  
  // Default material configuration
  createMaterial: () => {
    return {
      transparent: ${shaderName === 'xray'},
      side: THREE.DoubleSide,
      blending: ${shaderName === 'xray' ? 'THREE.AdditiveBlending' : 'THREE.NormalBlending'},
      depthWrite: ${shaderName !== 'xray'},
      alphaTest: ${shaderName === 'xray' ? 0.01 : 0}
    };
  }
};
`;

  const filename = path.join(outputDir, `${shaderName}Shader.js`);
  fs.writeFileSync(filename, shaderCode.trim());
  console.log(`✅ Generated: ${filename}`);
}

function generateUpdateLogic(shaderName) {
  const updateLogics = {
    xray: `
    // X-Ray specific updates
    if (params.intensity !== undefined && uniforms.intensity) {
      uniforms.intensity.value = params.intensity;
    }
    if (params.boneColor && uniforms.boneColor) {
      uniforms.boneColor.value = params.boneColor;
    }`,
    
    ultrasound: `
    // Ultrasound specific updates
    if (params.scanIntensity !== undefined && uniforms.scanIntensity) {
      uniforms.scanIntensity.value = params.scanIntensity;
    }
    if (params.frequency !== undefined && uniforms.frequency) {
      uniforms.frequency.value = params.frequency;
    }`,
    
    thermal: `
    // Thermal specific updates  
    if (params.corePosition && uniforms.corePosition) {
      uniforms.corePosition.value = params.corePosition;
    }
    if (params.heatRadius !== undefined && uniforms.heatRadius) {
      uniforms.heatRadius.value = params.heatRadius;
    }`,
    
    mri: `
    // MRI specific updates
    if (params.t1Weighting !== undefined && uniforms.t1Weighting) {
      uniforms.t1Weighting.value = params.t1Weighting;
    }
    if (params.t2Weighting !== undefined && uniforms.t2Weighting) {
      uniforms.t2Weighting.value = params.t2Weighting;
    }`
  };
  
  return updateLogics[shaderName] || '// No specific updates needed';
}

function generateMasterShaderFile(outputDir) {
  const imports = Object.keys(SHADER_TEMPLATES)
    .map(name => `import { ${name}Shader } from './${name}Shader.js';`)
    .join('\n');
  
  const exports = Object.keys(SHADER_TEMPLATES)
    .map(name => `  ${name}: ${name}Shader`)
    .join(',\n');

  const masterFile = `
// Auto-generated medical visualization shaders collection
// Generated on: ${new Date().toISOString()}

${imports}

export const MedicalShaders = {
${exports}
};

export class MedicalShaderManager {
  constructor() {
    this.activeShaders = new Map();
    this.animationCallbacks = new Map();
  }
  
  getShader(name) {
    return MedicalShaders[name];
  }
  
  createShaderMaterial(name, customUniforms = {}) {
    const shader = this.getShader(name);
    if (!shader) {
      console.warn(\`Unknown shader: \${name}\`);
      return null;
    }
    
    const uniforms = { ...shader.uniforms };
    Object.keys(customUniforms).forEach(key => {
      if (uniforms[key]) {
        uniforms[key].value = customUniforms[key];
      }
    });
    
    return new THREE.ShaderMaterial({
      vertexShader: shader.vertexShader,
      fragmentShader: shader.fragmentShader,
      uniforms,
      ...shader.createMaterial()
    });
  }
  
  registerForAnimation(name, material) {
    this.activeShaders.set(name, material);
    
    const shader = this.getShader(name);
    if (shader) {
      this.animationCallbacks.set(name, (time, params) => {
        shader.updateUniforms(material.uniforms, time, params);
      });
    }
  }
  
  update(time, shaderParams = {}) {
    this.animationCallbacks.forEach((callback, name) => {
      const params = shaderParams[name] || {};
      callback(time, params);
    });
  }
  
  dispose() {
    this.activeShaders.clear();
    this.animationCallbacks.clear();
  }
}

export default MedicalShaders;
`;

  const filename = path.join(outputDir, 'index.js');
  fs.writeFileSync(filename, masterFile.trim());
  console.log(`✅ Generated master file: ${filename}`);
}

function main() {
  const args = process.argv.slice(2);
  const modelArg = args.find(arg => arg.startsWith('--model='));
  const modelName = modelArg ? modelArg.split('=')[1] : 'default';
  
  console.log(`🎨 Generating medical visualization shaders for model: ${modelName}`);
  
  // Erstelle Output-Verzeichnis
  const outputDir = path.join(process.cwd(), 'src', 'shaders', 'generated');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  // Generiere individuelle Shader-Dateien
  Object.entries(SHADER_TEMPLATES).forEach(([name, data]) => {
    generateShaderFile(name, data, outputDir);
  });
  
  // Generiere Master-Datei
  generateMasterShaderFile(outputDir);
  
  console.log(`🎯 Shader generation completed! Files created in: ${outputDir}`);
  console.log(`📁 Generated ${Object.keys(SHADER_TEMPLATES).length + 1} shader files`);
  
  // Erstelle Dokumentation
  generateDocumentation(outputDir);
}

function generateDocumentation(outputDir) {
  const docContent = `
# Medical Visualization Shaders

Auto-generated documentation for medical visualization shaders.
Generated on: ${new Date().toISOString()}

## Available Shaders

${Object.entries(SHADER_TEMPLATES).map(([name, data]) => `
### ${data.name}
**File**: \`${name}Shader.js\`
**Description**: ${data.description}

**Uniforms**:
${Object.entries(data.uniforms).map(([key, value]) => 
  `- \`${key}\`: ${Array.isArray(value) ? `vec3(${value.join(', ')})` : typeof value === 'number' ? `float(${value})` : value}`
).join('\n')}

**Usage Example**:
\`\`\`javascript
import { ${name}Shader } from './generated/${name}Shader.js';

const material = new THREE.ShaderMaterial({
  vertexShader: ${name}Shader.vertexShader,
  fragmentShader: ${name}Shader.fragmentShader,
  uniforms: ${name}Shader.uniforms,
  ...${name}Shader.createMaterial()
});

// Animation loop
function animate(time) {
  ${name}Shader.updateUniforms(material.uniforms, time);
}
\`\`\`
`).join('\n')}

## Usage with MedicalShaderManager

\`\`\`javascript
import { MedicalShaderManager } from './generated/index.js';

const shaderManager = new MedicalShaderManager();

// Create shader material
const xrayMaterial = shaderManager.createShaderMaterial('xray', {
  intensity: 0.9,
  boneColor: [1, 1, 1]
});

// Register for animation
shaderManager.registerForAnimation('xray', xrayMaterial);

// Update in animation loop
function animate(time) {
  shaderManager.update(time, {
    xray: { intensity: 0.8 + 0.2 * Math.sin(time) }
  });
}
\`\`\`

## Integration with Bello Model

The shaders are designed to work with the Bello 3D model and can be easily integrated:

\`\`\`javascript
import { AnimalLoader } from '../game/AnimalLoader.js';
import { MedicalShaderManager } from './generated/index.js';

const animalLoader = new AnimalLoader();
const shaderManager = new MedicalShaderManager();

const bello = await animalLoader.loadBello();
const xrayMaterial = shaderManager.createShaderMaterial('xray');

// Apply to model
bello.traverse((child) => {
  if (child.isMesh) {
    child.material = xrayMaterial;
  }
});
\`\`\`
`;

  const docPath = path.join(outputDir, 'README.md');
  fs.writeFileSync(docPath, docContent.trim());
  console.log(`📚 Generated documentation: ${docPath}`);
}

// Run the generator
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

export { SHADER_TEMPLATES, generateShaderFile, generateMasterShaderFile };