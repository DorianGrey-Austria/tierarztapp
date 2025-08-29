// Interactive Anatomy System for VetScan Pro 3000
// Professional veterinary diagnostic interface with clickable organs
// Real-time medical visualization and diagnostic feedback

import * as THREE from 'three';
import { ANIMAL_SPECIES } from '../../veterinary-medical-data.js';

class DiagnosticZone {
  constructor(config) {
    this.name = config.name;
    this.position = config.position;
    this.radius = config.radius;
    this.organs = config.organs || [];
    this.isHovered = false;
    this.isSelected = false;
    
    // Visual elements
    this.visualization = null;
    this.hoverEffect = null;
    this.diagnosticData = null;
    
    this.onHover = config.onHover;
    this.onClick = config.onClick;
    this.onExamine = config.onExamine;
  }

  createVisualization() {
    const group = new THREE.Group();
    group.name = `DiagnosticZone_${this.name}`;
    
    // Invisible collision sphere
    const geometry = new THREE.SphereGeometry(this.radius, 16, 12);
    const material = new THREE.MeshBasicMaterial({ 
      transparent: true, 
      opacity: 0,
      side: THREE.DoubleSide
    });
    
    const sphere = new THREE.Mesh(geometry, material);
    sphere.position.copy(this.position);
    sphere.userData = {
      type: 'diagnostic_zone',
      zone: this,
      interactive: true
    };
    
    group.add(sphere);
    
    // Hover effect (glowing ring)
    this.createHoverEffect(group);
    
    this.visualization = group;
    return group;
  }

  createHoverEffect(parent) {
    const ringGeometry = new THREE.RingGeometry(
      this.radius * 0.9, 
      this.radius * 1.1, 
      16
    );
    
    const ringMaterial = new THREE.MeshBasicMaterial({
      color: 0x00ff88,
      transparent: true,
      opacity: 0,
      side: THREE.DoubleSide
    });
    
    const ring = new THREE.Mesh(ringGeometry, ringMaterial);
    ring.position.copy(this.position);
    ring.lookAt(new THREE.Vector3(0, 0, 1)); // Face camera
    
    this.hoverEffect = ring;
    parent.add(ring);
  }

  setHovered(hovered) {
    if (this.isHovered === hovered) return;
    
    this.isHovered = hovered;
    
    if (this.hoverEffect) {
      const targetOpacity = hovered ? 0.6 : 0;
      this.animateOpacity(this.hoverEffect.material, targetOpacity, 200);
    }
    
    if (hovered && this.onHover) {
      this.onHover(this);
    }
  }

  setSelected(selected) {
    if (this.isSelected === selected) return;
    
    this.isSelected = selected;
    
    if (this.hoverEffect) {
      this.hoverEffect.material.color.setHex(selected ? 0xff4444 : 0x00ff88);
    }
  }

  animateOpacity(material, targetOpacity, duration) {
    const startOpacity = material.opacity;
    const startTime = Date.now();
    
    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      material.opacity = startOpacity + (targetOpacity - startOpacity) * progress;
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };
    
    animate();
  }

  dispose() {
    if (this.visualization) {
      this.visualization.traverse(child => {
        if (child.geometry) child.geometry.dispose();
        if (child.material) child.material.dispose();
      });
    }
  }
}

class InteractiveAnatomy {
  constructor(animalModel, speciesId, patientData = null) {
    this.model = animalModel;
    this.speciesId = speciesId;
    this.patientData = patientData;
    this.speciesData = ANIMAL_SPECIES.find(s => s.id === speciesId);
    
    // Diagnostic zones
    this.diagnosticZones = [];
    this.selectedZone = null;
    this.hoveredZone = null;
    
    // Interaction system
    this.raycaster = new THREE.Raycaster();
    this.mouse = new THREE.Vector2();
    this.camera = null;
    this.renderer = null;
    
    // Event handlers
    this.onDiagnosisCallback = null;
    this.onZoneSelectCallback = null;
    this.onVitalMeasureCallback = null;
    
    // Medical state
    this.activeMedicalMode = 'normal';
    this.diagnosticHistory = [];
    this.vitalSigns = this.initializeVitalSigns();
    
    console.log(`🫀 Interactive Anatomy initialized for ${speciesId}`);
    this.createDiagnosticZones();
  }

  /**
   * Initialize vital signs based on species
   */
  initializeVitalSigns() {
    if (!this.speciesData) return {};
    
    const vitals = this.speciesData.vitalSigns;
    const baseVitals = {};
    
    Object.keys(vitals).forEach(vital => {
      const range = vitals[vital];
      if (range.min && range.max) {
        // Generate random value within normal range
        const value = range.min + Math.random() * (range.max - range.min);
        baseVitals[vital] = {
          value: Math.round(value * 10) / 10,
          unit: range.unit,
          normal: true,
          range: { min: range.min, max: range.max }
        };
      }
    });
    
    return baseVitals;
  }

  /**
   * Create diagnostic zones based on species anatomy
   */
  createDiagnosticZones() {
    if (!this.speciesData || !this.model) return;
    
    const anatomyPoints = this.speciesData.model3D?.anatomyPoints || {};
    const scale = this.model.scale.x || 1;
    
    // Standard diagnostic zones for all species
    const zoneConfigs = [
      {
        name: 'head',
        organs: ['brain', 'eyes', 'ears', 'nose', 'mouth'],
        position: anatomyPoints.brain || { x: 0.6, y: 0.8, z: 0 },
        radius: 0.2 * scale,
        color: 0x4CAF50
      },
      {
        name: 'chest', 
        organs: ['heart', 'lungs'],
        position: anatomyPoints.heart || { x: 0.3, y: 0.6, z: 0 },
        radius: 0.25 * scale,
        color: 0x2196F3
      },
      {
        name: 'abdomen',
        organs: ['stomach', 'liver', 'kidneys', 'intestines'],
        position: anatomyPoints.stomach || { x: 0, y: 0.4, z: 0 },
        radius: 0.3 * scale,
        color: 0xFF9800
      },
      {
        name: 'limbs',
        organs: ['bones', 'joints', 'muscles'],
        position: { x: 0, y: 0.2, z: 0 },
        radius: 0.15 * scale,
        color: 0x9C27B0
      }
    ];
    
    // Create zones
    zoneConfigs.forEach(config => {
      const zone = new DiagnosticZone({
        name: config.name,
        organs: config.organs,
        position: new THREE.Vector3(config.position.x, config.position.y, config.position.z),
        radius: config.radius,
        onHover: (zone) => this.onZoneHover(zone),
        onClick: (zone) => this.onZoneClick(zone),
        onExamine: (zone) => this.performExamination(zone)
      });
      
      const visualization = zone.createVisualization();
      this.model.add(visualization);
      this.diagnosticZones.push(zone);
    });
    
    console.log(`🎯 Created ${this.diagnosticZones.length} diagnostic zones`);
  }

  /**
   * Setup interaction system
   */
  setupInteraction(camera, renderer, container) {
    this.camera = camera;
    this.renderer = renderer;
    
    // Mouse/touch event listeners
    container.addEventListener('mousemove', this.onMouseMove.bind(this));
    container.addEventListener('click', this.onMouseClick.bind(this));
    container.addEventListener('touchstart', this.onTouchStart.bind(this));
    
    console.log('🖱️ Interaction system setup completed');
  }

  /**
   * Handle mouse movement for hover effects
   */
  onMouseMove(event) {
    if (!this.camera || !this.renderer) return;
    
    const rect = this.renderer.domElement.getBoundingClientRect();
    this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    
    this.checkIntersections();
  }

  /**
   * Handle mouse clicks for zone selection
   */
  onMouseClick(event) {
    if (!this.camera || !this.renderer) return;
    
    const rect = this.renderer.domElement.getBoundingClientRect();
    this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    
    const intersected = this.checkIntersections();
    if (intersected && intersected.userData.type === 'diagnostic_zone') {
      const zone = intersected.userData.zone;
      this.selectZone(zone);
    }
  }

  /**
   * Handle touch events for mobile
   */
  onTouchStart(event) {
    if (event.touches.length === 1) {
      event.preventDefault();
      const touch = event.touches[0];
      const mouseEvent = new MouseEvent('click', {
        clientX: touch.clientX,
        clientY: touch.clientY
      });
      this.onMouseClick(mouseEvent);
    }
  }

  /**
   * Check for intersections with diagnostic zones
   */
  checkIntersections() {
    if (!this.camera) return null;
    
    this.raycaster.setFromCamera(this.mouse, this.camera);
    
    // Get all interactive objects
    const interactiveObjects = [];
    this.model.traverse(child => {
      if (child.userData.interactive && child.userData.type === 'diagnostic_zone') {
        interactiveObjects.push(child);
      }
    });
    
    const intersects = this.raycaster.intersectObjects(interactiveObjects);
    
    // Clear previous hover
    if (this.hoveredZone) {
      this.hoveredZone.setHovered(false);
      this.hoveredZone = null;
    }
    
    // Set new hover
    if (intersects.length > 0) {
      const intersected = intersects[0].object;
      const zone = intersected.userData.zone;
      
      if (zone) {
        zone.setHovered(true);
        this.hoveredZone = zone;
        this.updateCursor('pointer');
        return intersected;
      }
    } else {
      this.updateCursor('default');
    }
    
    return null;
  }

  /**
   * Update cursor style
   */
  updateCursor(cursor) {
    if (this.renderer && this.renderer.domElement) {
      this.renderer.domElement.style.cursor = cursor;
    }
  }

  /**
   * Handle zone hover
   */
  onZoneHover(zone) {
    // Show zone info tooltip or highlight
    this.showZoneInfo(zone);
  }

  /**
   * Handle zone click/selection
   */
  onZoneClick(zone) {
    this.selectZone(zone);
  }

  /**
   * Select a diagnostic zone
   */
  selectZone(zone) {
    // Clear previous selection
    if (this.selectedZone) {
      this.selectedZone.setSelected(false);
    }
    
    // Set new selection
    this.selectedZone = zone;
    zone.setSelected(true);
    
    console.log(`🎯 Selected zone: ${zone.name}`);
    
    // Trigger examination
    this.performExamination(zone);
    
    // Callback
    if (this.onZoneSelectCallback) {
      this.onZoneSelectCallback(zone);
    }
  }

  /**
   * Perform medical examination on selected zone
   */
  async performExamination(zone) {
    console.log(`🔬 Examining ${zone.name}...`);
    
    // Simulate examination time
    const examinationData = {
      zoneName: zone.name,
      organs: zone.organs,
      timestamp: new Date().toISOString(),
      findings: [],
      vitalSigns: {},
      recommendations: []
    };
    
    // Generate findings based on zone and patient data
    const findings = await this.generateFindings(zone);
    examinationData.findings = findings;
    
    // Measure relevant vital signs
    const vitals = this.measureVitalSigns(zone);
    examinationData.vitalSigns = vitals;
    
    // Generate recommendations
    const recommendations = this.generateRecommendations(findings, vitals);
    examinationData.recommendations = recommendations;
    
    // Store in history
    this.diagnosticHistory.push(examinationData);
    
    // Visual feedback
    this.showExaminationResults(examinationData);
    
    // Callback
    if (this.onDiagnosisCallback) {
      this.onDiagnosisCallback(examinationData);
    }
    
    return examinationData;
  }

  /**
   * Generate examination findings
   */
  async generateFindings(zone) {
    const findings = [];
    
    // Get patient-specific symptoms if available
    if (this.patientData && this.patientData.symptomSets) {
      const relevantSymptoms = this.patientData.symptomSets.filter(symptomSet => {
        return zone.organs.some(organ => 
          symptomSet.symptoms.some(symptom => 
            symptom.toLowerCase().includes(organ) ||
            this.getOrganAssociations(organ).some(assoc => 
              symptom.toLowerCase().includes(assoc)
            )
          )
        );
      });
      
      relevantSymptoms.forEach(symptomSet => {
        findings.push({
          type: 'symptom',
          description: symptomSet.diagnosis || 'Abnormal findings detected',
          severity: this.calculateSeverity(symptomSet),
          organs: zone.organs.filter(organ => 
            symptomSet.symptoms.some(symptom => 
              symptom.toLowerCase().includes(organ)
            )
          )
        });
      });
    }
    
    // Add normal findings if no issues detected
    if (findings.length === 0) {
      findings.push({
        type: 'normal',
        description: `${zone.name} appears normal`,
        severity: 'normal',
        organs: zone.organs
      });
    }
    
    return findings;
  }

  /**
   * Get organ associations for symptom matching
   */
  getOrganAssociations(organ) {
    const associations = {
      heart: ['cardiac', 'chest', 'breathing', 'pulse'],
      lungs: ['respiratory', 'breathing', 'cough', 'chest'],
      stomach: ['digestive', 'appetite', 'nausea', 'vomit'],
      liver: ['digestive', 'abdomen', 'jaundice'],
      brain: ['neurological', 'behavior', 'seizure', 'head'],
      eyes: ['vision', 'sight', 'discharge'],
      ears: ['hearing', 'balance', 'discharge']
    };
    
    return associations[organ] || [];
  }

  /**
   * Calculate symptom severity
   */
  calculateSeverity(symptomSet) {
    if (!symptomSet.vitalChanges) return 'normal';
    
    const changes = symptomSet.vitalChanges;
    let severityScore = 0;
    
    // Check vital sign deviations
    Object.keys(changes).forEach(vital => {
      const normal = this.vitalSigns[vital];
      if (normal && normal.range) {
        const deviation = Math.abs(changes[vital] - normal.value) / normal.range.max;
        severityScore += deviation;
      }
    });
    
    if (severityScore > 0.3) return 'severe';
    if (severityScore > 0.15) return 'moderate';
    if (severityScore > 0.05) return 'mild';
    return 'normal';
  }

  /**
   * Measure vital signs for specific zone
   */
  measureVitalSigns(zone) {
    const relevantVitals = {};
    
    // Zone-specific vital signs
    const zoneVitals = {
      chest: ['heartRate', 'respiratoryRate', 'bloodPressure', 'oxygenSaturation'],
      head: ['temperature', 'bloodPressure'],
      abdomen: ['temperature', 'bloodGlucose'],
      limbs: ['temperature', 'bloodPressure']
    };
    
    const vitalsToMeasure = zoneVitals[zone.name] || ['temperature'];
    
    vitalsToMeasure.forEach(vital => {
      if (this.vitalSigns[vital]) {
        // Simulate measurement variation
        const baseValue = this.vitalSigns[vital].value;
        const variation = (Math.random() - 0.5) * 0.1; // ±5% variation
        const measuredValue = baseValue * (1 + variation);
        
        relevantVitals[vital] = {
          ...this.vitalSigns[vital],
          value: Math.round(measuredValue * 10) / 10,
          measured: true,
          timestamp: new Date().toISOString()
        };
      }
    });
    
    return relevantVitals;
  }

  /**
   * Generate medical recommendations
   */
  generateRecommendations(findings, vitals) {
    const recommendations = [];
    
    findings.forEach(finding => {
      if (finding.severity !== 'normal') {
        switch (finding.type) {
          case 'symptom':
            recommendations.push({
              type: 'treatment',
              priority: finding.severity,
              action: `Further examination of ${finding.organs.join(', ')} recommended`,
              description: `Based on ${finding.description}`
            });
            break;
        }
      }
    });
    
    // Vital sign recommendations
    Object.keys(vitals).forEach(vital => {
      const vitalData = vitals[vital];
      if (!vitalData.normal) {
        recommendations.push({
          type: 'monitoring',
          priority: 'moderate',
          action: `Monitor ${vital} closely`,
          description: `Value outside normal range: ${vitalData.value} ${vitalData.unit}`
        });
      }
    });
    
    if (recommendations.length === 0) {
      recommendations.push({
        type: 'routine',
        priority: 'low',
        action: 'Continue routine monitoring',
        description: 'All findings within normal limits'
      });
    }
    
    return recommendations;
  }

  /**
   * Show zone information
   */
  showZoneInfo(zone) {
    // This would typically update a UI tooltip or info panel
    console.log(`ℹ️ Zone: ${zone.name}, Organs: ${zone.organs.join(', ')}`);
  }

  /**
   * Show examination results
   */
  showExaminationResults(data) {
    console.log('🔬 Examination Results:', data);
    
    // Visual feedback on the 3D model
    if (this.selectedZone) {
      this.animateExaminationEffect(this.selectedZone);
    }
  }

  /**
   * Animate examination effect
   */
  animateExaminationEffect(zone) {
    if (!zone.hoverEffect) return;
    
    const originalColor = zone.hoverEffect.material.color.clone();
    const flashColor = new THREE.Color(0x00ffff);
    
    // Flash effect
    let flashCount = 0;
    const maxFlashes = 3;
    
    const flash = () => {
      zone.hoverEffect.material.color.copy(flashColor);
      
      setTimeout(() => {
        zone.hoverEffect.material.color.copy(originalColor);
        flashCount++;
        
        if (flashCount < maxFlashes) {
          setTimeout(flash, 200);
        }
      }, 100);
    };
    
    flash();
  }

  /**
   * Switch medical visualization mode
   */
  switchMedicalMode(mode) {
    if (this.model.medicalViz) {
      this.model.medicalViz.switchMode(mode);
      this.activeMedicalMode = mode;
      
      // Update zone visibility based on mode
      this.updateZoneVisibility(mode);
    }
  }

  /**
   * Update zone visibility based on medical mode
   */
  updateZoneVisibility(mode) {
    this.diagnosticZones.forEach(zone => {
      if (zone.hoverEffect) {
        // Adjust zone colors based on medical mode
        const modeColors = {
          normal: 0x00ff88,
          xray: 0x4444ff,
          ultrasound: 0xffff44,
          thermal: 0xff4444,
          mri: 0xff88ff
        };
        
        const color = modeColors[mode] || 0x00ff88;
        zone.hoverEffect.material.color.setHex(color);
      }
    });
  }

  /**
   * Get diagnostic history
   */
  getDiagnosticHistory() {
    return this.diagnosticHistory;
  }

  /**
   * Get current vital signs
   */
  getCurrentVitalSigns() {
    return this.vitalSigns;
  }

  /**
   * Set callbacks
   */
  onDiagnosis(callback) {
    this.onDiagnosisCallback = callback;
  }

  onZoneSelect(callback) {
    this.onZoneSelectCallback = callback;
  }

  onVitalMeasure(callback) {
    this.onVitalMeasureCallback = callback;
  }

  /**
   * Cleanup and disposal
   */
  dispose() {
    // Remove event listeners
    if (this.renderer && this.renderer.domElement) {
      const container = this.renderer.domElement.parentElement;
      if (container) {
        container.removeEventListener('mousemove', this.onMouseMove);
        container.removeEventListener('click', this.onMouseClick);
        container.removeEventListener('touchstart', this.onTouchStart);
      }
    }
    
    // Dispose zones
    this.diagnosticZones.forEach(zone => zone.dispose());
    this.diagnosticZones = [];
    
    console.log('🧹 Interactive Anatomy disposed');
  }
}

export { InteractiveAnatomy, DiagnosticZone };