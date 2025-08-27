/**
 * Hyper3D-Style Procedural Animal Generator for Three.js
 * Creates realistic animal models using intelligent procedural generation
 * Simulates AI-generated models without actual AI API calls
 */

export class Hyper3DAnimalGenerator {
    constructor(scene) {
        this.scene = scene;
        this.materials = {};
        this.setupMaterials();
    }

    setupMaterials() {
        // Dog Materials
        this.materials.goldenFur = new THREE.MeshStandardMaterial({
            color: new THREE.Color(0.85, 0.65, 0.35),
            roughness: 0.85,
            metalness: 0.1
        });

        this.materials.blackFur = new THREE.MeshStandardMaterial({
            color: new THREE.Color(0.15, 0.15, 0.15),
            roughness: 0.9,
            metalness: 0.05
        });

        this.materials.brownFur = new THREE.MeshStandardMaterial({
            color: new THREE.Color(0.4, 0.25, 0.15),
            roughness: 0.85,
            metalness: 0.1
        });

        // Cat Materials  
        this.materials.greyFur = new THREE.MeshStandardMaterial({
            color: new THREE.Color(0.5, 0.5, 0.5),
            roughness: 0.8,
            metalness: 0.05
        });

        this.materials.orangeFur = new THREE.MeshStandardMaterial({
            color: new THREE.Color(0.9, 0.5, 0.2),
            roughness: 0.8,
            metalness: 0.05
        });

        // Reptile Materials
        this.materials.scales = new THREE.MeshStandardMaterial({
            color: new THREE.Color(0.3, 0.5, 0.2),
            roughness: 0.3,
            metalness: 0.4
        });

        // Bird Materials
        this.materials.feathers = new THREE.MeshStandardMaterial({
            color: new THREE.Color(0.1, 0.5, 0.9),
            roughness: 0.6,
            metalness: 0.2
        });

        // Fish Materials
        this.materials.fishScales = new THREE.MeshStandardMaterial({
            color: new THREE.Color(0.9, 0.6, 0.1),
            roughness: 0.2,
            metalness: 0.6
        });
    }

    generateAnimal(animalType) {
        console.log(`🤖 Hyper3D generating: ${animalType}`);
        
        const group = new THREE.Group();
        group.name = `Hyper3D_${animalType}`;

        switch(animalType) {
            case 'dog':
                return this.generateDog();
            case 'cat':
                return this.generateCat();
            case 'rabbit':
                return this.generateRabbit();
            case 'guinea_pig':
                return this.generateGuineaPig();
            case 'horse':
                return this.generateHorse();
            case 'parrot':
                return this.generateParrot();
            case 'turtle':
                return this.generateTurtle();
            case 'snake':
                return this.generateSnake();
            case 'hamster':
                return this.generateHamster();
            case 'goldfish':
                return this.generateGoldfish();
            default:
                return this.generateGenericAnimal();
        }
    }

    generateDog() {
        const group = new THREE.Group();
        
        // Body - elongated ellipsoid
        const bodyGeometry = new THREE.SphereGeometry(1, 16, 12);
        bodyGeometry.scale(1.8, 0.8, 0.7);
        const body = new THREE.Mesh(bodyGeometry, this.materials.goldenFur);
        body.position.set(0, 0, 0);
        body.castShadow = true;
        group.add(body);
        
        // Head - sphere with snout
        const headGeometry = new THREE.SphereGeometry(0.5, 16, 12);
        headGeometry.scale(1.2, 1, 1);
        const head = new THREE.Mesh(headGeometry, this.materials.goldenFur);
        head.position.set(1.5, 0.3, 0);
        head.castShadow = true;
        group.add(head);
        
        // Snout
        const snoutGeometry = new THREE.ConeGeometry(0.2, 0.6, 8);
        snoutGeometry.rotateZ(Math.PI / 2);
        const snout = new THREE.Mesh(snoutGeometry, this.materials.goldenFur);
        snout.position.set(2.1, 0.2, 0);
        group.add(snout);
        
        // Ears
        const earGeometry = new THREE.ConeGeometry(0.15, 0.4, 6);
        const leftEar = new THREE.Mesh(earGeometry, this.materials.goldenFur);
        leftEar.position.set(1.3, 0.7, -0.3);
        leftEar.rotation.z = -0.3;
        group.add(leftEar);
        
        const rightEar = leftEar.clone();
        rightEar.position.z = 0.3;
        group.add(rightEar);
        
        // Legs
        const legGeometry = new THREE.CylinderGeometry(0.15, 0.12, 0.8, 8);
        const legPositions = [
            [0.8, -0.6, 0.3],
            [0.8, -0.6, -0.3],
            [-0.8, -0.6, 0.3],
            [-0.8, -0.6, -0.3]
        ];
        
        legPositions.forEach(pos => {
            const leg = new THREE.Mesh(legGeometry, this.materials.goldenFur);
            leg.position.set(...pos);
            leg.castShadow = true;
            group.add(leg);
        });
        
        // Tail
        const tailGeometry = new THREE.CylinderGeometry(0.08, 0.15, 1, 8);
        const tail = new THREE.Mesh(tailGeometry, this.materials.goldenFur);
        tail.position.set(-1.5, 0.2, 0);
        tail.rotation.z = 0.5;
        group.add(tail);
        
        return group;
    }

    generateCat() {
        const group = new THREE.Group();
        
        // Body - compact ellipsoid
        const bodyGeometry = new THREE.SphereGeometry(0.8, 16, 12);
        bodyGeometry.scale(1.5, 0.7, 0.6);
        const body = new THREE.Mesh(bodyGeometry, this.materials.greyFur);
        body.castShadow = true;
        group.add(body);
        
        // Head - round with triangular shape
        const headGeometry = new THREE.SphereGeometry(0.4, 16, 12);
        const head = new THREE.Mesh(headGeometry, this.materials.greyFur);
        head.position.set(1.2, 0.3, 0);
        head.castShadow = true;
        group.add(head);
        
        // Ears - triangular
        const earGeometry = new THREE.ConeGeometry(0.12, 0.25, 4);
        const leftEar = new THREE.Mesh(earGeometry, this.materials.greyFur);
        leftEar.position.set(1.1, 0.6, -0.2);
        group.add(leftEar);
        
        const rightEar = leftEar.clone();
        rightEar.position.z = 0.2;
        group.add(rightEar);
        
        // Legs - slender
        const legGeometry = new THREE.CylinderGeometry(0.08, 0.08, 0.6, 8);
        const legPositions = [
            [0.6, -0.5, 0.2],
            [0.6, -0.5, -0.2],
            [-0.6, -0.5, 0.2],
            [-0.6, -0.5, -0.2]
        ];
        
        legPositions.forEach(pos => {
            const leg = new THREE.Mesh(legGeometry, this.materials.greyFur);
            leg.position.set(...pos);
            leg.castShadow = true;
            group.add(leg);
        });
        
        // Tail - long and curved
        const tailCurve = new THREE.CatmullRomCurve3([
            new THREE.Vector3(-1, 0, 0),
            new THREE.Vector3(-1.5, 0.3, 0),
            new THREE.Vector3(-1.8, 0.7, 0),
            new THREE.Vector3(-1.9, 1.2, 0)
        ]);
        
        const tailGeometry = new THREE.TubeGeometry(tailCurve, 10, 0.06, 8, false);
        const tail = new THREE.Mesh(tailGeometry, this.materials.greyFur);
        group.add(tail);
        
        return group;
    }

    generateRabbit() {
        const group = new THREE.Group();
        
        // Body - round
        const bodyGeometry = new THREE.SphereGeometry(0.7, 16, 12);
        bodyGeometry.scale(1.2, 0.9, 0.8);
        const body = new THREE.Mesh(bodyGeometry, this.materials.brownFur);
        body.castShadow = true;
        group.add(body);
        
        // Head
        const headGeometry = new THREE.SphereGeometry(0.35, 16, 12);
        const head = new THREE.Mesh(headGeometry, this.materials.brownFur);
        head.position.set(0.8, 0.3, 0);
        head.castShadow = true;
        group.add(head);
        
        // Long ears
        const earGeometry = new THREE.CylinderGeometry(0.08, 0.1, 0.8, 8);
        const leftEar = new THREE.Mesh(earGeometry, this.materials.brownFur);
        leftEar.position.set(0.7, 0.8, -0.15);
        leftEar.rotation.z = -0.1;
        group.add(leftEar);
        
        const rightEar = leftEar.clone();
        rightEar.position.z = 0.15;
        group.add(rightEar);
        
        // Strong hind legs
        const hindLegGeometry = new THREE.SphereGeometry(0.25, 8, 6);
        hindLegGeometry.scale(0.8, 1.2, 0.8);
        
        const leftHindLeg = new THREE.Mesh(hindLegGeometry, this.materials.brownFur);
        leftHindLeg.position.set(-0.4, -0.5, 0.3);
        group.add(leftHindLeg);
        
        const rightHindLeg = leftHindLeg.clone();
        rightHindLeg.position.z = -0.3;
        group.add(rightHindLeg);
        
        // Front paws
        const frontPawGeometry = new THREE.CylinderGeometry(0.06, 0.06, 0.3, 6);
        const leftPaw = new THREE.Mesh(frontPawGeometry, this.materials.brownFur);
        leftPaw.position.set(0.4, -0.5, 0.15);
        group.add(leftPaw);
        
        const rightPaw = leftPaw.clone();
        rightPaw.position.z = -0.15;
        group.add(rightPaw);
        
        // Fluffy tail
        const tailGeometry = new THREE.SphereGeometry(0.15, 8, 8);
        const tail = new THREE.Mesh(tailGeometry, this.materials.brownFur);
        tail.position.set(-0.9, 0, 0);
        group.add(tail);
        
        return group;
    }

    generateHorse() {
        const group = new THREE.Group();
        
        // Large body
        const bodyGeometry = new THREE.SphereGeometry(1.2, 16, 12);
        bodyGeometry.scale(2, 0.9, 0.8);
        const body = new THREE.Mesh(bodyGeometry, this.materials.brownFur);
        body.castShadow = true;
        group.add(body);
        
        // Neck
        const neckGeometry = new THREE.CylinderGeometry(0.4, 0.5, 1.2, 8);
        const neck = new THREE.Mesh(neckGeometry, this.materials.brownFur);
        neck.position.set(1.8, 0.6, 0);
        neck.rotation.z = -0.5;
        group.add(neck);
        
        // Head
        const headGeometry = new THREE.SphereGeometry(0.4, 12, 10);
        headGeometry.scale(1.5, 0.8, 0.7);
        const head = new THREE.Mesh(headGeometry, this.materials.brownFur);
        head.position.set(2.3, 1, 0);
        group.add(head);
        
        // Long legs
        const legGeometry = new THREE.CylinderGeometry(0.12, 0.1, 1.5, 8);
        const legPositions = [
            [1.2, -1, 0.4],
            [1.2, -1, -0.4],
            [-1.2, -1, 0.4],
            [-1.2, -1, -0.4]
        ];
        
        legPositions.forEach(pos => {
            const leg = new THREE.Mesh(legGeometry, this.materials.brownFur);
            leg.position.set(...pos);
            leg.castShadow = true;
            group.add(leg);
        });
        
        // Mane
        const maneGeometry = new THREE.BoxGeometry(0.1, 0.8, 0.6);
        const mane = new THREE.Mesh(maneGeometry, this.materials.blackFur);
        mane.position.set(1.5, 1, 0);
        group.add(mane);
        
        // Tail
        const tailGeometry = new THREE.CylinderGeometry(0.15, 0.05, 1.5, 8);
        const tail = new THREE.Mesh(tailGeometry, this.materials.blackFur);
        tail.position.set(-2, -0.2, 0);
        tail.rotation.z = 0.6;
        group.add(tail);
        
        return group;
    }

    generateParrot() {
        const group = new THREE.Group();
        
        // Body
        const bodyGeometry = new THREE.SphereGeometry(0.5, 12, 10);
        bodyGeometry.scale(1, 1.5, 0.7);
        const body = new THREE.Mesh(bodyGeometry, this.materials.feathers);
        body.castShadow = true;
        group.add(body);
        
        // Head
        const headGeometry = new THREE.SphereGeometry(0.25, 12, 10);
        const head = new THREE.Mesh(headGeometry, this.materials.feathers);
        head.position.set(0, 0.8, 0);
        group.add(head);
        
        // Beak
        const beakGeometry = new THREE.ConeGeometry(0.08, 0.2, 6);
        beakGeometry.rotateX(Math.PI / 2);
        const beak = new THREE.Mesh(beakGeometry, this.materials.orangeFur);
        beak.position.set(0, 0.75, 0.25);
        group.add(beak);
        
        // Wings
        const wingGeometry = new THREE.SphereGeometry(0.4, 8, 6);
        wingGeometry.scale(0.2, 1.2, 0.8);
        
        const leftWing = new THREE.Mesh(wingGeometry, this.materials.feathers);
        leftWing.position.set(-0.4, 0, 0);
        leftWing.rotation.z = 0.3;
        group.add(leftWing);
        
        const rightWing = leftWing.clone();
        rightWing.position.x = 0.4;
        rightWing.rotation.z = -0.3;
        group.add(rightWing);
        
        // Tail feathers
        const tailGeometry = new THREE.ConeGeometry(0.2, 0.8, 6);
        const tail = new THREE.Mesh(tailGeometry, this.materials.feathers);
        tail.position.set(0, -0.8, 0);
        tail.rotation.z = Math.PI;
        group.add(tail);
        
        // Feet
        const footGeometry = new THREE.CylinderGeometry(0.03, 0.03, 0.3, 4);
        const leftFoot = new THREE.Mesh(footGeometry, this.materials.orangeFur);
        leftFoot.position.set(-0.1, -0.7, 0);
        group.add(leftFoot);
        
        const rightFoot = leftFoot.clone();
        rightFoot.position.x = 0.1;
        group.add(rightFoot);
        
        return group;
    }

    generateTurtle() {
        const group = new THREE.Group();
        
        // Shell - dome shape
        const shellGeometry = new THREE.SphereGeometry(0.8, 12, 8, 0, Math.PI * 2, 0, Math.PI / 2);
        const shell = new THREE.Mesh(shellGeometry, this.materials.scales);
        shell.castShadow = true;
        group.add(shell);
        
        // Bottom shell
        const bottomGeometry = new THREE.CylinderGeometry(0.7, 0.7, 0.1, 12);
        const bottom = new THREE.Mesh(bottomGeometry, this.materials.scales);
        bottom.position.y = -0.05;
        group.add(bottom);
        
        // Head
        const headGeometry = new THREE.SphereGeometry(0.2, 8, 6);
        const head = new THREE.Mesh(headGeometry, this.materials.scales);
        head.position.set(0.7, 0, 0);
        group.add(head);
        
        // Legs
        const legGeometry = new THREE.SphereGeometry(0.15, 6, 4);
        legGeometry.scale(1, 0.5, 0.8);
        
        const legPositions = [
            [0.5, -0.1, 0.5],
            [0.5, -0.1, -0.5],
            [-0.5, -0.1, 0.5],
            [-0.5, -0.1, -0.5]
        ];
        
        legPositions.forEach(pos => {
            const leg = new THREE.Mesh(legGeometry, this.materials.scales);
            leg.position.set(...pos);
            group.add(leg);
        });
        
        return group;
    }

    generateSnake() {
        const group = new THREE.Group();
        
        // Create snake body with segments
        const segments = 15;
        const segmentLength = 0.3;
        
        for (let i = 0; i < segments; i++) {
            const radius = 0.15 - (i * 0.008); // Taper
            const segmentGeometry = new THREE.SphereGeometry(radius, 8, 6);
            const segment = new THREE.Mesh(segmentGeometry, this.materials.scales);
            
            // Create S-curve
            const angle = (i / segments) * Math.PI * 2;
            segment.position.set(
                i * segmentLength,
                Math.sin(angle) * 0.3,
                Math.cos(angle) * 0.2
            );
            
            segment.castShadow = true;
            group.add(segment);
        }
        
        // Head
        const headGeometry = new THREE.SphereGeometry(0.18, 10, 8);
        headGeometry.scale(1.3, 0.8, 0.9);
        const head = new THREE.Mesh(headGeometry, this.materials.scales);
        head.position.set(-0.3, 0, 0);
        group.add(head);
        
        // Eyes
        const eyeGeometry = new THREE.SphereGeometry(0.03, 6, 6);
        const eyeMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
        
        const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        leftEye.position.set(-0.4, 0.05, 0.1);
        group.add(leftEye);
        
        const rightEye = leftEye.clone();
        rightEye.position.z = -0.1;
        group.add(rightEye);
        
        return group;
    }

    generateGuineaPig() {
        const group = new THREE.Group();
        
        // Rounded body
        const bodyGeometry = new THREE.SphereGeometry(0.6, 12, 10);
        bodyGeometry.scale(1.3, 0.8, 0.9);
        const body = new THREE.Mesh(bodyGeometry, this.materials.brownFur);
        body.castShadow = true;
        group.add(body);
        
        // Head
        const headGeometry = new THREE.SphereGeometry(0.3, 10, 8);
        const head = new THREE.Mesh(headGeometry, this.materials.brownFur);
        head.position.set(0.6, 0.1, 0);
        group.add(head);
        
        // Small ears
        const earGeometry = new THREE.SphereGeometry(0.08, 6, 4);
        const leftEar = new THREE.Mesh(earGeometry, this.materials.brownFur);
        leftEar.position.set(0.5, 0.3, -0.15);
        group.add(leftEar);
        
        const rightEar = leftEar.clone();
        rightEar.position.z = 0.15;
        group.add(rightEar);
        
        // Short legs
        const legGeometry = new THREE.CylinderGeometry(0.05, 0.05, 0.2, 6);
        const legPositions = [
            [0.3, -0.4, 0.2],
            [0.3, -0.4, -0.2],
            [-0.3, -0.4, 0.2],
            [-0.3, -0.4, -0.2]
        ];
        
        legPositions.forEach(pos => {
            const leg = new THREE.Mesh(legGeometry, this.materials.brownFur);
            leg.position.set(...pos);
            group.add(leg);
        });
        
        return group;
    }

    generateHamster() {
        const group = new THREE.Group();
        
        // Chubby body
        const bodyGeometry = new THREE.SphereGeometry(0.5, 12, 10);
        bodyGeometry.scale(1, 0.8, 0.8);
        const body = new THREE.Mesh(bodyGeometry, this.materials.orangeFur);
        body.castShadow = true;
        group.add(body);
        
        // Head with cheek pouches
        const headGeometry = new THREE.SphereGeometry(0.25, 10, 8);
        headGeometry.scale(1.2, 1, 1);
        const head = new THREE.Mesh(headGeometry, this.materials.orangeFur);
        head.position.set(0.5, 0.1, 0);
        group.add(head);
        
        // Cheek pouches
        const cheekGeometry = new THREE.SphereGeometry(0.1, 6, 6);
        const leftCheek = new THREE.Mesh(cheekGeometry, this.materials.orangeFur);
        leftCheek.position.set(0.6, 0, -0.15);
        group.add(leftCheek);
        
        const rightCheek = leftCheek.clone();
        rightCheek.position.z = 0.15;
        group.add(rightCheek);
        
        // Round ears
        const earGeometry = new THREE.SphereGeometry(0.06, 6, 4);
        const leftEar = new THREE.Mesh(earGeometry, this.materials.orangeFur);
        leftEar.position.set(0.4, 0.25, -0.1);
        group.add(leftEar);
        
        const rightEar = leftEar.clone();
        rightEar.position.z = 0.1;
        group.add(rightEar);
        
        // Tiny legs
        const legGeometry = new THREE.CylinderGeometry(0.04, 0.04, 0.15, 6);
        const legPositions = [
            [0.2, -0.35, 0.15],
            [0.2, -0.35, -0.15],
            [-0.2, -0.35, 0.15],
            [-0.2, -0.35, -0.15]
        ];
        
        legPositions.forEach(pos => {
            const leg = new THREE.Mesh(legGeometry, this.materials.orangeFur);
            leg.position.set(...pos);
            group.add(leg);
        });
        
        // Short tail
        const tailGeometry = new THREE.SphereGeometry(0.04, 4, 4);
        const tail = new THREE.Mesh(tailGeometry, this.materials.orangeFur);
        tail.position.set(-0.5, 0, 0);
        group.add(tail);
        
        return group;
    }

    generateGoldfish() {
        const group = new THREE.Group();
        
        // Body - oval shape
        const bodyGeometry = new THREE.SphereGeometry(0.4, 12, 10);
        bodyGeometry.scale(1.5, 0.8, 0.5);
        const body = new THREE.Mesh(bodyGeometry, this.materials.fishScales);
        body.castShadow = true;
        group.add(body);
        
        // Tail fin
        const tailGeometry = new THREE.ConeGeometry(0.3, 0.6, 6);
        tailGeometry.rotateZ(-Math.PI / 2);
        tailGeometry.scale(0.3, 1, 1);
        const tail = new THREE.Mesh(tailGeometry, this.materials.fishScales);
        tail.position.set(-0.8, 0, 0);
        group.add(tail);
        
        // Dorsal fin
        const dorsalGeometry = new THREE.ConeGeometry(0.15, 0.3, 4);
        dorsalGeometry.scale(0.2, 1, 1);
        const dorsal = new THREE.Mesh(dorsalGeometry, this.materials.fishScales);
        dorsal.position.set(0, 0.4, 0);
        group.add(dorsal);
        
        // Side fins
        const finGeometry = new THREE.SphereGeometry(0.15, 6, 4);
        finGeometry.scale(0.2, 0.8, 1);
        
        const leftFin = new THREE.Mesh(finGeometry, this.materials.fishScales);
        leftFin.position.set(0.2, 0, -0.3);
        leftFin.rotation.y = -0.3;
        group.add(leftFin);
        
        const rightFin = leftFin.clone();
        rightFin.position.z = 0.3;
        rightFin.rotation.y = 0.3;
        group.add(rightFin);
        
        // Eyes
        const eyeGeometry = new THREE.SphereGeometry(0.05, 8, 8);
        const eyeMaterial = new THREE.MeshBasicMaterial({ color: 0x000000 });
        
        const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        leftEye.position.set(0.5, 0.1, -0.15);
        group.add(leftEye);
        
        const rightEye = leftEye.clone();
        rightEye.position.z = 0.15;
        group.add(rightEye);
        
        return group;
    }

    generateGenericAnimal() {
        const group = new THREE.Group();
        
        // Basic quadruped structure
        const bodyGeometry = new THREE.SphereGeometry(0.8, 12, 10);
        bodyGeometry.scale(1.5, 0.8, 0.7);
        const body = new THREE.Mesh(bodyGeometry, this.materials.brownFur);
        body.castShadow = true;
        group.add(body);
        
        // Head
        const headGeometry = new THREE.SphereGeometry(0.4, 10, 8);
        const head = new THREE.Mesh(headGeometry, this.materials.brownFur);
        head.position.set(1.2, 0.2, 0);
        group.add(head);
        
        // Legs
        const legGeometry = new THREE.CylinderGeometry(0.1, 0.1, 0.6, 8);
        const legPositions = [
            [0.6, -0.5, 0.3],
            [0.6, -0.5, -0.3],
            [-0.6, -0.5, 0.3],
            [-0.6, -0.5, -0.3]
        ];
        
        legPositions.forEach(pos => {
            const leg = new THREE.Mesh(legGeometry, this.materials.brownFur);
            leg.position.set(...pos);
            leg.castShadow = true;
            group.add(leg);
        });
        
        return group;
    }
}