// Datei: src/shaders/MedicalVisualization.js
// Medizinische Visualisierungseffekte für das Veterinärspiel

import * as THREE from 'three';

class MedicalVisualization {
  constructor(model) {
    this.model = model;
    this.originalMaterials = new Map();
    this.currentMode = 'normal';
    
    // Speichere originale Materialien
    this.storeOriginalMaterials();
    
    // Initialisiere Shader-Materialien
    this.initializeShaders();
  }

  /**
   * Speichert die originalen Materialien für später
   */
  storeOriginalMaterials() {
    this.model.traverse((child) => {
      if (child.isMesh && child.material) {
        this.originalMaterials.set(child.uuid, child.material.clone());
      }
    });
  }

  /**
   * Initialisiert alle Shader-Materialien
   */
  initializeShaders() {
    this.shaders = {
      normal: this.createNormalState(),
      xray: this.createXrayState(),
      ultrasound: this.createUltrasoundState(),
      mri: this.createMRIState(),
      thermal: this.createThermalState()
    };
  }

  /**
   * Normal-Visualisierung (Original-Materialien)
   */
  createNormalState() {
    return {
      name: 'Normal View',
      description: 'Standard-Ansicht mit natürlichen Farben',
      apply: (mesh) => {
        const originalMaterial = this.originalMaterials.get(mesh.uuid);
        if (originalMaterial) {
          mesh.material = originalMaterial.clone();
        }
      }
    };
  }

  /**
   * Röntgen-Visualisierung
   */
  createXrayState() {
    const vertexShader = `
      varying vec3 vNormal;
      varying vec3 vPosition;
      
      void main() {
        vNormal = normalize(normalMatrix * normal);
        vPosition = (modelViewMatrix * vec4(position, 1.0)).xyz;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `;

    const fragmentShader = `
      varying vec3 vNormal;
      varying vec3 vPosition;
      uniform float time;
      uniform float intensity;
      
      void main() {
        // Fresnel-Effekt für Transparenz
        vec3 viewDirection = normalize(-vPosition);
        float fresnel = 1.0 - max(0.0, dot(viewDirection, vNormal));
        
        // Tiefenbasierte Intensität
        float depth = length(vPosition) / 10.0;
        float alpha = fresnel * intensity * (1.0 - depth * 0.1);
        
        // Röntgen-Farbe (bläulich-weiß)
        vec3 xrayColor = vec3(0.7, 0.8, 1.0);
        
        // Knochen-Simulation (höhere Dichte = heller)
        float boneIntensity = smoothstep(0.3, 0.8, fresnel);
        vec3 finalColor = mix(vec3(0.2, 0.2, 0.3), xrayColor, boneIntensity);
        
        gl_FragColor = vec4(finalColor, alpha);
      }
    `;

    return {
      name: 'X-Ray View',
      description: 'Röntgenaufnahme - zeigt Knochenstrukturen',
      apply: (mesh) => {
        mesh.material = new THREE.ShaderMaterial({
          vertexShader,
          fragmentShader,
          uniforms: {
            time: { value: 0 },
            intensity: { value: 0.8 }
          },
          transparent: true,
          side: THREE.DoubleSide,
          blending: THREE.AdditiveBlending
        });
      },
      animate: (material, time) => {
        if (material.uniforms) {
          material.uniforms.time.value = time;
        }
      }
    };
  }

  /**
   * Ultraschall-Visualisierung
   */
  createUltrasoundState() {
    const vertexShader = `
      varying vec2 vUv;
      varying vec3 vPosition;
      varying vec3 vNormal;
      
      void main() {
        vUv = uv;
        vPosition = (modelViewMatrix * vec4(position, 1.0)).xyz;
        vNormal = normalize(normalMatrix * normal);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `;

    const fragmentShader = `
      varying vec2 vUv;
      varying vec3 vPosition;
      varying vec3 vNormal;
      uniform float time;
      uniform float scanIntensity;
      
      // Noise-Funktion für Ultraschall-Textur
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
        return mix(a, b, u.x) + (c - a)* u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
      }
      
      void main() {
        // Ultraschall-Scan-Linien
        float scanLine = sin(vPosition.y * 20.0 + time * 5.0) * 0.5 + 0.5;
        
        // Noise für realistische Ultraschall-Textur
        vec2 noiseCoord = vUv * 50.0 + time * 0.1;
        float noiseValue = noise(noiseCoord);
        
        // Tiefenbasierte Dämpfung
        float depth = length(vPosition) / 8.0;
        float attenuation = exp(-depth * 0.5);
        
        // Akustische Schatten-Simulation
        float shadow = smoothstep(0.0, 1.0, dot(vNormal, vec3(0, 0, 1)));
        
        // Ultraschall-Farbe (Graustufenbereich)
        float intensity = scanLine * noiseValue * attenuation * shadow * scanIntensity;
        vec3 ultrasoundColor = vec3(intensity);
        
        // Leichte bläuliche Tönung
        ultrasoundColor.b += 0.1;
        
        gl_FragColor = vec4(ultrasoundColor, 1.0);
      }
    `;

    return {
      name: 'Ultrasound View',
      description: 'Ultraschallaufnahme - zeigt Weichgewebe',
      apply: (mesh) => {
        mesh.material = new THREE.ShaderMaterial({
          vertexShader,
          fragmentShader,
          uniforms: {
            time: { value: 0 },
            scanIntensity: { value: 0.7 }
          },
          transparent: false
        });
      },
      animate: (material, time) => {
        if (material.uniforms) {
          material.uniforms.time.value = time;
        }
      }
    };
  }

  /**
   * MRI-Visualisierung
   */
  createMRIState() {
    return {
      name: 'MRI View',
      description: 'Magnetresonanztomographie - detaillierte Gewebedarstellung',
      apply: (mesh) => {
        mesh.material = new THREE.MeshLambertMaterial({
          color: 0x444444,
          transparent: true,
          opacity: 0.9
        });
        
        // Simuliere verschiedene Gewebetypen durch Farbvariationen
        const position = mesh.geometry.attributes.position;
        if (position) {
          // Einfache MRI-Simulation basierend auf Geometrie
          mesh.material.color.setHSL(0.6, 0.2, 0.4);
        }
      }
    };
  }

  /**
   * Thermal-Visualisierung (Wärmebildkamera)
   */
  createThermalState() {
    const vertexShader = `
      varying vec3 vPosition;
      varying vec3 vNormal;
      
      void main() {
        vPosition = (modelViewMatrix * vec4(position, 1.0)).xyz;
        vNormal = normalize(normalMatrix * normal);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `;

    const fragmentShader = `
      varying vec3 vPosition;
      varying vec3 vNormal;
      uniform float time;
      
      vec3 heatColor(float temperature) {
        // Temperatur zu Farbe mapping (blau->grün->gelb->rot)
        if (temperature < 0.25) {
          return mix(vec3(0, 0, 1), vec3(0, 1, 1), temperature * 4.0);
        } else if (temperature < 0.5) {
          return mix(vec3(0, 1, 1), vec3(0, 1, 0), (temperature - 0.25) * 4.0);
        } else if (temperature < 0.75) {
          return mix(vec3(0, 1, 0), vec3(1, 1, 0), (temperature - 0.5) * 4.0);
        } else {
          return mix(vec3(1, 1, 0), vec3(1, 0, 0), (temperature - 0.75) * 4.0);
        }
      }
      
      void main() {
        // Simuliere Körperwärme basierend auf Position
        float temperature = 0.5 + sin(vPosition.y * 2.0 + time) * 0.2;
        temperature += dot(vNormal, vec3(0, 1, 0)) * 0.3; // Warmer oben
        
        vec3 thermalColor = heatColor(clamp(temperature, 0.0, 1.0));
        gl_FragColor = vec4(thermalColor, 1.0);
      }
    `;

    return {
      name: 'Thermal View',
      description: 'Wärmebild - zeigt Temperaturverteilung',
      apply: (mesh) => {
        mesh.material = new THREE.ShaderMaterial({
          vertexShader,
          fragmentShader,
          uniforms: {
            time: { value: 0 }
          }
        });
      },
      animate: (material, time) => {
        if (material.uniforms) {
          material.uniforms.time.value = time;
        }
      }
    };
  }

  /**
   * Wechselt zwischen Visualisierungsmodi
   * @param {string} mode 'normal' | 'xray' | 'ultrasound' | 'mri' | 'thermal'
   */
  switchMode(mode) {
    if (!this.shaders[mode]) {
      console.warn(`Unknown visualization mode: ${mode}`);
      return;
    }

    this.currentMode = mode;
    const shader = this.shaders[mode];
    
    // Animiere Übergang
    this.animateTransition(() => {
      this.model.traverse((child) => {
        if (child.isMesh) {
          shader.apply(child);
        }
      });
    });

    console.log(`🔬 Switched to ${shader.name}`);
  }

  /**
   * Animiert Übergänge zwischen Modi
   */
  animateTransition(callback) {
    // Einfache Fade-Animation
    const originalOpacity = this.model.traverse((child) => {
      if (child.isMesh && child.material) {
        return child.material.opacity || 1;
      }
    });

    // Fade out
    this.fadeModel(0, 200, () => {
      callback();
      // Fade in
      this.fadeModel(1, 200);
    });
  }

  /**
   * Fade-Animation für das Modell
   */
  fadeModel(targetOpacity, duration, onComplete) {
    const startTime = Date.now();
    const materials = [];
    
    this.model.traverse((child) => {
      if (child.isMesh && child.material) {
        materials.push({
          material: child.material,
          startOpacity: child.material.opacity || 1
        });
        child.material.transparent = true;
      }
    });

    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const opacity = materials[0]?.startOpacity + (targetOpacity - materials[0]?.startOpacity) * progress;

      materials.forEach(({ material }) => {
        material.opacity = opacity;
      });

      if (progress < 1) {
        requestAnimationFrame(animate);
      } else if (onComplete) {
        onComplete();
      }
    };

    animate();
  }

  /**
   * Update-Loop für animierte Shader
   */
  update(time) {
    const shader = this.shaders[this.currentMode];
    if (shader && shader.animate) {
      this.model.traverse((child) => {
        if (child.isMesh && child.material) {
          shader.animate(child.material, time);
        }
      });
    }
  }

  /**
   * Gibt Informationen über den aktuellen Modus zurück
   */
  getCurrentModeInfo() {
    const shader = this.shaders[this.currentMode];
    return {
      mode: this.currentMode,
      name: shader.name,
      description: shader.description
    };
  }

  /**
   * Gibt alle verfügbaren Modi zurück
   */
  getAvailableModes() {
    return Object.keys(this.shaders).map(mode => ({
      key: mode,
      name: this.shaders[mode].name,
      description: this.shaders[mode].description
    }));
  }

  /**
   * Cleanup
   */
  dispose() {
    // Dispose alle erstellten Materialien
    Object.values(this.shaders).forEach(shader => {
      // Shader-Materialien werden automatisch von Three.js bereinigt
    });

    // Originale Materialien bereinigen
    this.originalMaterials.forEach(material => {
      material.dispose();
    });

    this.originalMaterials.clear();
    console.log('🧹 MedicalVisualization disposed');
  }
}

export { MedicalVisualization };