// Advanced Medical Visualization Shaders for VetScan Pro 3000
// Professional veterinary medical imaging simulation
// Includes CT scan, enhanced MRI, Doppler ultrasound, and advanced X-Ray

import * as THREE from 'three';

class AdvancedMedicalShaders {
  constructor() {
    this.shaderCache = new Map();
    this.uniformCache = new Map();
    this.animationCallbacks = new Map();
    
    console.log('🔬 Advanced Medical Shaders initialized');
  }

  /**
   * Enhanced X-Ray Shader with bone density simulation
   */
  createAdvancedXrayShader() {
    const vertexShader = `
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec3 vWorldPosition;
      varying vec2 vUv;
      
      void main() {
        vNormal = normalize(normalMatrix * normal);
        vPosition = (modelViewMatrix * vec4(position, 1.0)).xyz;
        vWorldPosition = (modelMatrix * vec4(position, 1.0)).xyz;
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `;

    const fragmentShader = `
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec3 vWorldPosition;
      varying vec2 vUv;
      
      uniform float time;
      uniform float intensity;
      uniform float boneThreshold;
      uniform float tissueOpacity;
      uniform float contrastLevel;
      uniform vec3 xrayColor;
      uniform bool showBones;
      uniform bool showSoftTissue;
      
      // Noise function for tissue variation
      float noise(vec3 p) {
        vec3 i = floor(p);
        vec3 f = fract(p);
        f = f * f * (3.0 - 2.0 * f);
        
        float n = dot(i, vec3(1.0, 57.0, 113.0));
        return mix(mix(mix(sin(n), sin(n + 1.0), f.x),
                      mix(sin(n + 57.0), sin(n + 58.0), f.x), f.y),
                  mix(mix(sin(n + 113.0), sin(n + 114.0), f.x),
                      mix(sin(n + 170.0), sin(n + 171.0), f.x), f.y), f.z) * 0.5 + 0.5;
      }
      
      // Simulate tissue density
      float getTissueDensity(vec3 pos) {
        float density = 0.5;
        
        // Add noise for realistic tissue variation
        density += noise(pos * 10.0) * 0.2;
        density += noise(pos * 25.0) * 0.1;
        density += noise(pos * 50.0) * 0.05;
        
        // Simulate different tissue types
        float distanceFromCenter = length(pos);
        
        // Bones (higher density near center)
        if (distanceFromCenter < 0.3) {
          density = mix(density, 0.9, 0.6); // Bone density
        }
        // Soft tissue
        else if (distanceFromCenter < 0.6) {
          density = mix(density, 0.3, 0.4); // Soft tissue
        }
        // Air/low density
        else {
          density = mix(density, 0.1, 0.3);
        }
        
        return clamp(density, 0.0, 1.0);
      }
      
      void main() {
        // Fresnel effect for edge detection
        vec3 viewDirection = normalize(-vPosition);
        float fresnel = 1.0 - max(0.0, dot(viewDirection, vNormal));
        
        // Get tissue density at current position
        float tissueDensity = getTissueDensity(vWorldPosition);
        
        // X-ray penetration simulation
        float penetration = exp(-tissueDensity * 2.0);
        
        // Bone visualization
        float boneIntensity = 0.0;
        if (showBones && tissueDensity > boneThreshold) {
          boneIntensity = smoothstep(boneThreshold, 1.0, tissueDensity);
          boneIntensity *= contrastLevel;
        }
        
        // Soft tissue visualization
        float tissueIntensity = 0.0;
        if (showSoftTissue && tissueDensity <= boneThreshold) {
          tissueIntensity = (1.0 - tissueDensity) * tissueOpacity;
        }
        
        // Combine intensities
        float totalIntensity = max(boneIntensity, tissueIntensity);
        totalIntensity *= fresnel * intensity * penetration;
        
        // X-ray color mapping
        vec3 finalColor = xrayColor * totalIntensity;
        
        // Add subtle animation for "live" feel
        finalColor += vec3(0.1) * sin(time * 2.0) * 0.1;
        
        float alpha = totalIntensity;
        
        gl_FragColor = vec4(finalColor, alpha);
      }
    `;

    const uniforms = {
      time: { value: 0 },
      intensity: { value: 0.8 },
      boneThreshold: { value: 0.6 },
      tissueOpacity: { value: 0.3 },
      contrastLevel: { value: 2.0 },
      xrayColor: { value: new THREE.Color(0.7, 0.8, 1.0) },
      showBones: { value: true },
      showSoftTissue: { value: true }
    };

    return {
      vertexShader,
      fragmentShader,
      uniforms,
      transparent: true,
      side: THREE.DoubleSide,
      blending: THREE.AdditiveBlending
    };
  }

  /**
   * CT Scan Shader with slice navigation
   */
  createCTScanShader() {
    const vertexShader = `
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec2 vUv;
      
      void main() {
        vPosition = position;
        vNormal = normalize(normalMatrix * normal);
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `;

    const fragmentShader = `
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec2 vUv;
      
      uniform float time;
      uniform float slicePosition;
      uniform float sliceThickness;
      uniform float windowLevel;
      uniform float windowWidth;
      uniform int sliceAxis; // 0=X, 1=Y, 2=Z
      uniform bool showSlicePlane;
      uniform vec3 ctColor;
      
      // Hounsfield Unit simulation
      float getHounsfieldUnit(vec3 pos) {
        float hu = -1000.0; // Air
        
        float distanceFromCenter = length(pos);
        
        // Bone simulation (+400 to +1000 HU)
        if (distanceFromCenter < 0.4) {
          hu = mix(400.0, 1000.0, (0.4 - distanceFromCenter) / 0.4);
        }
        // Soft tissue (0 to +100 HU)
        else if (distanceFromCenter < 0.7) {
          hu = mix(0.0, 100.0, (0.7 - distanceFromCenter) / 0.3);
        }
        // Fat (-200 to -50 HU)
        else if (distanceFromCenter < 0.9) {
          hu = mix(-200.0, -50.0, (0.9 - distanceFromCenter) / 0.2);
        }
        
        return hu;
      }
      
      // Window/Level function for CT display
      float windowLevel(float hu, float level, float width) {
        float min = level - width / 2.0;
        float max = level + width / 2.0;
        return clamp((hu - min) / (max - min), 0.0, 1.0);
      }
      
      void main() {
        vec3 pos = vPosition;
        
        // Determine if current fragment is in active slice
        float sliceCoord;
        if (sliceAxis == 0) sliceCoord = pos.x;
        else if (sliceAxis == 1) sliceCoord = pos.y;
        else sliceCoord = pos.z;
        
        float distanceFromSlice = abs(sliceCoord - slicePosition);
        
        if (showSlicePlane && distanceFromSlice > sliceThickness) {
          discard; // Only show current slice
        }
        
        // Get Hounsfield Unit for this position
        float hu = getHounsfieldUnit(pos);
        
        // Apply window/level
        float intensity = windowLevel(hu, windowLevel, windowWidth);
        
        // CT color mapping (grayscale with blue tint)
        vec3 finalColor = ctColor * intensity;
        
        // Add slice plane highlighting
        if (showSlicePlane && distanceFromSlice < sliceThickness * 0.1) {
          finalColor += vec3(0.0, 0.5, 1.0) * 0.3;
        }
        
        // Pulsing animation for active scanning
        finalColor *= 0.8 + 0.2 * sin(time * 4.0);
        
        gl_FragColor = vec4(finalColor, intensity);
      }
    `;

    const uniforms = {
      time: { value: 0 },
      slicePosition: { value: 0.0 },
      sliceThickness: { value: 0.05 },
      windowLevel: { value: 40 },
      windowWidth: { value: 400 },
      sliceAxis: { value: 2 }, // Z-axis by default
      showSlicePlane: { value: true },
      ctColor: { value: new THREE.Color(0.8, 0.8, 1.0) }
    };

    return {
      vertexShader,
      fragmentShader,
      uniforms,
      transparent: true,
      side: THREE.FrontSide
    };
  }

  /**
   * Enhanced MRI Shader with T1/T2 weighting
   */
  createEnhancedMRIShader() {
    const vertexShader = `
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec2 vUv;
      
      void main() {
        vPosition = position;
        vNormal = normalize(normalMatrix * normal);
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `;

    const fragmentShader = `
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec2 vUv;
      
      uniform float time;
      uniform float t1Contrast;
      uniform float t2Contrast;
      uniform float sliceThickness;
      uniform bool contrastEnhancement;
      uniform vec3 mriColor;
      uniform float sequenceType; // 0=T1, 1=T2, 2=FLAIR
      
      // Tissue relaxation times simulation
      struct TissueProperties {
        float t1;
        float t2;
        float pd; // Proton density
      };
      
      TissueProperties getTissueProperties(vec3 pos) {
        TissueProperties tissue;
        
        float distanceFromCenter = length(pos);
        
        // CSF (Cerebrospinal fluid)
        if (distanceFromCenter > 0.8) {
          tissue.t1 = 4000.0;
          tissue.t2 = 2000.0;
          tissue.pd = 1.0;
        }
        // Gray matter
        else if (distanceFromCenter > 0.5) {
          tissue.t1 = 920.0;
          tissue.t2 = 100.0;
          tissue.pd = 0.8;
        }
        // White matter
        else if (distanceFromCenter > 0.2) {
          tissue.t1 = 600.0;
          tissue.t2 = 80.0;
          tissue.pd = 0.7;
        }
        // Fat
        else {
          tissue.t1 = 300.0;
          tissue.t2 = 70.0;
          tissue.pd = 0.9;
        }
        
        return tissue;
      }
      
      float calculateSignalIntensity(TissueProperties tissue, float sequenceType) {
        float signal = 0.0;
        
        if (sequenceType < 0.5) {
          // T1-weighted
          signal = tissue.pd * (1.0 - exp(-2000.0 / tissue.t1));
          signal *= t1Contrast;
        }
        else if (sequenceType < 1.5) {
          // T2-weighted  
          signal = tissue.pd * exp(-80.0 / tissue.t2);
          signal *= t2Contrast;
        }
        else {
          // FLAIR (T2 with CSF suppression)
          signal = tissue.pd * exp(-80.0 / tissue.t2);
          if (tissue.t1 > 3000.0) signal *= 0.1; // Suppress CSF
          signal *= t2Contrast;
        }
        
        return clamp(signal, 0.0, 1.0);
      }
      
      void main() {
        vec3 pos = vPosition;
        
        // Get tissue properties for current position
        TissueProperties tissue = getTissueProperties(pos);
        
        // Calculate MRI signal intensity
        float intensity = calculateSignalIntensity(tissue, sequenceType);
        
        // Apply contrast enhancement if enabled
        if (contrastEnhancement) {
          // Simulate contrast agent uptake in vascular areas
          float vascularProximity = 1.0 - length(pos) * 0.5;
          intensity += vascularProximity * 0.3;
        }
        
        // MRI color mapping
        vec3 finalColor = mriColor * intensity;
        
        // Add scanning animation (RF pulse simulation)
        float scanPulse = sin(time * 8.0) * 0.1 + 0.9;
        finalColor *= scanPulse;
        
        // Noise simulation (typical in MRI)
        float noise = (sin(pos.x * 100.0) * sin(pos.y * 100.0) * sin(pos.z * 100.0)) * 0.05;
        intensity += noise;
        
        gl_FragColor = vec4(finalColor, clamp(intensity, 0.0, 1.0));
      }
    `;

    const uniforms = {
      time: { value: 0 },
      t1Contrast: { value: 1.2 },
      t2Contrast: { value: 0.8 },
      sliceThickness: { value: 3.0 },
      contrastEnhancement: { value: false },
      mriColor: { value: new THREE.Color(0.9, 0.9, 0.9) },
      sequenceType: { value: 0.0 } // T1-weighted by default
    };

    return {
      vertexShader,
      fragmentShader,
      uniforms,
      transparent: false,
      side: THREE.FrontSide
    };
  }

  /**
   * Doppler Ultrasound Shader with flow visualization
   */
  createDopplerUltrasoundShader() {
    const vertexShader = `
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec2 vUv;
      
      void main() {
        vPosition = position;
        vNormal = normalize(normalMatrix * normal);
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `;

    const fragmentShader = `
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec2 vUv;
      
      uniform float time;
      uniform float frequency;
      uniform float penetration;
      uniform float gain;
      uniform bool dopplerMode;
      uniform vec3 probeDirection;
      uniform float dopplerSensitivity;
      
      // Noise function for tissue echoes
      float noise(vec3 p) {
        return fract(sin(dot(p, vec3(12.9898, 78.233, 45.164))) * 43758.5453);
      }
      
      // Simulate blood flow velocity
      vec3 getFlowVelocity(vec3 pos) {
        // Simulate arterial flow pattern
        float distance = length(pos);
        vec3 flowDirection = normalize(vec3(1.0, 0.0, 0.0));
        
        // Pulsatile flow (heartbeat simulation)
        float heartbeat = sin(time * 3.14159 * 2.0) * 0.5 + 0.5;
        float velocity = heartbeat * exp(-distance * 2.0);
        
        return flowDirection * velocity * 0.5;
      }
      
      // Calculate Doppler shift
      float getDopplerShift(vec3 pos, vec3 flowVel) {
        float cosTheta = dot(normalize(flowVel), normalize(probeDirection));
        return cosTheta * length(flowVel) * frequency * 2.0 / 1540.0; // Speed of sound in tissue
      }
      
      // Tissue echo calculation
      float getTissueEcho(vec3 pos) {
        float echo = 0.0;
        
        // Different tissue impedances
        float distance = length(pos);
        
        // Bone (strong reflection)
        if (distance < 0.3) {
          echo = 0.9;
        }
        // Soft tissue interfaces
        else if (distance < 0.6) {
          echo = 0.3 + noise(pos * 20.0) * 0.2;
        }
        // Fluid (low echo)
        else {
          echo = 0.1;
        }
        
        // Attenuation with depth
        float depth = abs(dot(pos, probeDirection));
        echo *= exp(-depth * penetration);
        
        return echo * gain;
      }
      
      void main() {
        vec3 pos = vPosition;
        
        // Basic ultrasound echo
        float echo = getTissueEcho(pos);
        
        vec3 finalColor;
        
        if (dopplerMode) {
          // Doppler ultrasound mode
          vec3 flowVelocity = getFlowVelocity(pos);
          float dopplerShift = getDopplerShift(pos, flowVelocity);
          
          // Color mapping for flow direction
          if (abs(dopplerShift) > 0.1 * dopplerSensitivity) {
            if (dopplerShift > 0.0) {
              // Flow towards probe (red)
              finalColor = vec3(1.0, 0.2, 0.2) * abs(dopplerShift) * 10.0;
            } else {
              // Flow away from probe (blue)
              finalColor = vec3(0.2, 0.2, 1.0) * abs(dopplerShift) * 10.0;
            }
            finalColor = mix(vec3(echo), finalColor, 0.7);
          } else {
            // No significant flow - grayscale
            finalColor = vec3(echo);
          }
        } else {
          // Standard B-mode ultrasound
          finalColor = vec3(echo);
        }
        
        // Scan line animation
        float scanLine = sin(pos.x * 50.0 + time * 10.0) * 0.1 + 0.9;
        finalColor *= scanLine;
        
        // Add ultrasound speckle noise
        float speckle = noise(pos * 100.0 + time * 0.1) * 0.2;
        finalColor += vec3(speckle);
        
        gl_FragColor = vec4(finalColor, 1.0);
      }
    `;

    const uniforms = {
      time: { value: 0 },
      frequency: { value: 7.5 }, // MHz
      penetration: { value: 0.5 },
      gain: { value: 0.75 },
      dopplerMode: { value: false },
      probeDirection: { value: new THREE.Vector3(0, 0, 1) },
      dopplerSensitivity: { value: 1.0 }
    };

    return {
      vertexShader,
      fragmentShader,
      uniforms,
      transparent: false,
      side: THREE.FrontSide
    };
  }

  /**
   * Advanced Thermal Shader with inflammation detection
   */
  createAdvancedThermalShader() {
    const vertexShader = `
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec2 vUv;
      
      void main() {
        vPosition = position;
        vNormal = normalize(normalMatrix * normal);
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `;

    const fragmentShader = `
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec2 vUv;
      
      uniform float time;
      uniform float bodyTemp;
      uniform float sensitivity;
      uniform vec2 tempRange;
      uniform bool showInflammation;
      uniform float ambientTemp;
      
      // Simulate body temperature distribution
      float getBodyTemperature(vec3 pos) {
        float temp = bodyTemp;
        
        float distanceFromCore = length(pos);
        
        // Core temperature (internal organs)
        if (distanceFromCore < 0.4) {
          temp = bodyTemp + 1.0; // Core is warmer
        }
        // Surface temperature
        else if (distanceFromCore > 0.7) {
          temp = mix(bodyTemp, ambientTemp, (distanceFromCore - 0.7) / 0.3);
        }
        
        // Add circulation patterns
        float circulation = sin(pos.x * 5.0) * sin(pos.y * 5.0) * 0.5;
        temp += circulation * 0.3;
        
        // Inflammation hotspots (random simulation)
        float inflammation = 0.0;
        if (showInflammation) {
          vec3 hotspot1 = vec3(0.2, 0.3, 0.1);
          vec3 hotspot2 = vec3(-0.1, 0.4, -0.2);
          
          inflammation += exp(-length(pos - hotspot1) * 10.0) * 2.0;
          inflammation += exp(-length(pos - hotspot2) * 8.0) * 1.5;
        }
        
        temp += inflammation;
        
        // Breathing effect on chest area
        if (abs(pos.y - 0.6) < 0.2 && abs(pos.z) < 0.3) {
          temp += sin(time * 1.5) * 0.2; // Breathing pattern
        }
        
        return temp;
      }
      
      // Temperature to color mapping
      vec3 temperatureToColor(float temp) {
        // Normalize temperature to 0-1 range
        float normalized = (temp - tempRange.x) / (tempRange.y - tempRange.x);
        normalized = clamp(normalized, 0.0, 1.0);
        
        vec3 color;
        
        if (normalized < 0.2) {
          // Cold - Blue to Cyan
          color = mix(vec3(0.0, 0.0, 1.0), vec3(0.0, 1.0, 1.0), normalized * 5.0);
        }
        else if (normalized < 0.4) {
          // Cool - Cyan to Green
          color = mix(vec3(0.0, 1.0, 1.0), vec3(0.0, 1.0, 0.0), (normalized - 0.2) * 5.0);
        }
        else if (normalized < 0.6) {
          // Normal - Green to Yellow
          color = mix(vec3(0.0, 1.0, 0.0), vec3(1.0, 1.0, 0.0), (normalized - 0.4) * 5.0);
        }
        else if (normalized < 0.8) {
          // Warm - Yellow to Orange
          color = mix(vec3(1.0, 1.0, 0.0), vec3(1.0, 0.5, 0.0), (normalized - 0.6) * 5.0);
        }
        else {
          // Hot - Orange to Red
          color = mix(vec3(1.0, 0.5, 0.0), vec3(1.0, 0.0, 0.0), (normalized - 0.8) * 5.0);
        }
        
        return color;
      }
      
      void main() {
        vec3 pos = vPosition;
        
        // Get temperature at current position
        float temperature = getBodyTemperature(pos);
        
        // Convert to thermal color
        vec3 thermalColor = temperatureToColor(temperature);
        
        // Add thermal camera noise
        float noise = (sin(pos.x * 200.0) * sin(pos.y * 200.0)) * 0.05;
        thermalColor += vec3(noise);
        
        // Thermal camera refresh rate simulation
        float refresh = step(0.8, sin(time * 60.0)); // 60 Hz refresh
        thermalColor *= 0.9 + refresh * 0.1;
        
        // Edge detection for better visibility
        float edge = 1.0 - abs(dot(vNormal, vec3(0, 0, 1)));
        thermalColor = mix(thermalColor, thermalColor * 1.5, edge * 0.3);
        
        gl_FragColor = vec4(thermalColor, 1.0);
      }
    `;

    const uniforms = {
      time: { value: 0 },
      bodyTemp: { value: 38.5 }, // °C
      sensitivity: { value: 0.1 },
      tempRange: { value: new THREE.Vector2(30.0, 42.0) },
      showInflammation: { value: true },
      ambientTemp: { value: 22.0 }
    };

    return {
      vertexShader,
      fragmentShader,
      uniforms,
      transparent: false,
      side: THREE.FrontSide
    };
  }

  /**
   * Get shader configuration by name
   */
  getShader(name) {
    if (this.shaderCache.has(name)) {
      return this.shaderCache.get(name);
    }

    let shaderConfig;
    
    switch (name) {
      case 'xray_advanced':
        shaderConfig = this.createAdvancedXrayShader();
        break;
      case 'ct_scan':
        shaderConfig = this.createCTScanShader();
        break;
      case 'mri_enhanced':
        shaderConfig = this.createEnhancedMRIShader();
        break;
      case 'ultrasound_doppler':
        shaderConfig = this.createDopplerUltrasoundShader();
        break;
      case 'thermal_advanced':
        shaderConfig = this.createAdvancedThermalShader();
        break;
      default:
        console.warn(`Unknown shader: ${name}`);
        return null;
    }

    this.shaderCache.set(name, shaderConfig);
    return shaderConfig;
  }

  /**
   * Create shader material
   */
  createMaterial(shaderName, customUniforms = {}) {
    const config = this.getShader(shaderName);
    if (!config) return null;

    // Merge custom uniforms
    const uniforms = { ...config.uniforms };
    Object.keys(customUniforms).forEach(key => {
      if (uniforms[key]) {
        uniforms[key].value = customUniforms[key];
      }
    });

    const material = new THREE.ShaderMaterial({
      vertexShader: config.vertexShader,
      fragmentShader: config.fragmentShader,
      uniforms: uniforms,
      transparent: config.transparent || false,
      side: config.side || THREE.FrontSide,
      blending: config.blending || THREE.NormalBlending
    });

    // Store reference for uniform updates
    this.uniformCache.set(material.uuid, uniforms);

    return material;
  }

  /**
   * Update shader uniforms
   */
  updateUniforms(material, updates) {
    const uniforms = this.uniformCache.get(material.uuid);
    if (!uniforms) return;

    Object.keys(updates).forEach(key => {
      if (uniforms[key]) {
        uniforms[key].value = updates[key];
      }
    });
  }

  /**
   * Animate shader (call in render loop)
   */
  animate(material, deltaTime) {
    const uniforms = this.uniformCache.get(material.uuid);
    if (!uniforms) return;

    // Update time uniform if present
    if (uniforms.time) {
      uniforms.time.value += deltaTime;
    }

    // Call custom animation callback if registered
    const callback = this.animationCallbacks.get(material.uuid);
    if (callback) {
      callback(uniforms, deltaTime);
    }
  }

  /**
   * Register animation callback for material
   */
  setAnimationCallback(material, callback) {
    this.animationCallbacks.set(material.uuid, callback);
  }

  /**
   * Get available shader names
   */
  getAvailableShaders() {
    return [
      'xray_advanced',
      'ct_scan', 
      'mri_enhanced',
      'ultrasound_doppler',
      'thermal_advanced'
    ];
  }

  /**
   * Cleanup and disposal
   */
  dispose() {
    this.shaderCache.clear();
    this.uniformCache.clear();
    this.animationCallbacks.clear();
    console.log('🧹 Advanced Medical Shaders disposed');
  }
}

export { AdvancedMedicalShaders };