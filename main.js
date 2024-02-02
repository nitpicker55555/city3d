import * as THREE from 'https://unpkg.com/three@0.156.0/build/three.module.js';
import { OBJLoader } from 'https://threejs.org/examples/jsm/loaders/OBJLoader.js';
import { OrbitControls } from 'https://unpkg.com/three/examples/jsm/controls/OrbitControls.js';
let scene, camera, renderer, controls,raycaster;
const mouse = new THREE.Vector2();
const clickCoordinates = new THREE.Vector3();
const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
directionalLight.position.set(0, 1, 0);
const ambientLight = new THREE.AmbientLight(0x404040);
init();
animate();
let Model_;

function init() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x8FBCD4); // 背景色

    const aspectRatio = window.innerWidth / window.innerHeight;
    camera = new THREE.PerspectiveCamera(75, aspectRatio, 1, 60000);
    camera.position.set(0, 0, 60000); // 设置相机位置

    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);


    // const ambientLight = new THREE.AmbientLight(0xcccccc, 0.4);
    // scene.add(ambientLight);

    // directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);

    scene.add(directionalLight);
    document.getElementById('lightSlider').addEventListener('input', function(event) {
        const angle = event.target.value;
        updateLightAngle(angle);
    });

    const loader = new OBJLoader();
    loader.load('q.obj', function (object) {
        scene.add(object);
        Model_ = object;

        const box = new THREE.Box3().setFromObject(object);
        const size = box.getSize(new THREE.Vector3());
        const center = box.getCenter(new THREE.Vector3());
        camera.lookAt(center);
        const maxDimension = Math.max(size.x, size.y, size.z);
        controls.maxDistance = maxDimension * 10;
        controls.target = center;
        controls.update();
    });


    controls = new OrbitControls(camera, renderer.domElement);
    controls.minDistance = 10;
    controls.maxDistance = 10000000; // 最大距离
    renderer.domElement.addEventListener('click', onClick, false);

    raycaster = new THREE.Raycaster();
    window.addEventListener('resize', onWindowResize, false);
}
function onClick(event) {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObject(Model_, true);

    if (intersects.length > 0) {
        clickCoordinates.copy(intersects[0].point);

        const reflectance = calculateReflectance(intersects[0]);

        console.log('点击坐标:', clickCoordinates);
        console.log('光线反射值:', reflectance);
    }
}

function calculateReflectance(intersection) {
    // 获取法线
    const normal = intersection.normal.clone();

    // 获取到光源的向量
    const lightDirection = new THREE.Vector3();
    directionalLight.getWorldDirection(lightDirection);
    console.log(lightDirection)
    console.log(directionalLight)
    // 计算光线反射
    const dotProduct = Math.max(normal.dot(directionalLight.position), 0);
    const reflectance = dotProduct * directionalLight.intensity;

    return reflectance;
}
const material = new THREE.MeshPhongMaterial({ color: 0xff0000, emissive: 0x330000 });

function getReflectionValue(intersection) {
    const materialColor = material.color;
    const emissiveColor = material.emissive;
    const lightColor = pointLight.color;
    const lightPosition = pointLight.position;

    // 计算光线反射值
    const ambient = materialColor.clone().multiply(lightColor);
    const diffuse = materialColor.clone().multiply(lightColor).multiplyScalar(
        Math.max(0, intersection.face.normal.dot(lightPosition.clone().normalize()))
    );
    const emissive = emissiveColor.clone().multiply(lightColor);

    const reflectionValue = {
        ambient: ambient,
        diffuse: diffuse,
        emissive: emissive
    };

    // 返回反射值
    return reflectionValue;
}
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    render();
}
function updateLightAngle(angle) {
    const radians = angle * (Math.PI / 180);
    directionalLight.position.y = Math.cos(radians);
    directionalLight.position.z = Math.sin(radians);
    render();
}
function render() {
    renderer.render(scene, camera);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}