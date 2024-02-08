import * as THREE from 'https://unpkg.com/three@0.150.0/build/three.module.js';
import { OBJLoader } from 'https://threejs.org/examples/jsm/loaders/OBJLoader.js';
import { GLTFLoader  } from 'https://threejs.org/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'https://unpkg.com/three/examples/jsm/controls/OrbitControls.js';
// import * as BufferGeometryUtils from 'https://unpkg.com/three/examples/jsm/utils/BufferGeometryUtils.js';
// import Chart from 'https://cdn.skypack.dev/chart.js';
let scene, camera, renderer, controls,raycaster;
const mouse = new THREE.Vector2();
const clickCoordinates = new THREE.Vector3();
const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(600, 6000, 600); // 假设光源位于场景的上方
directionalLight.castShadow = true;

const size = 5000 // 选择一个足够大的数值以覆盖物体及其周围区域
directionalLight.shadow.camera.left = -size;
directionalLight.shadow.camera.right = size;
directionalLight.shadow.camera.top = size;
directionalLight.shadow.camera.bottom = -size;

directionalLight.shadow.camera.near = 10; // 根据场景大小调整
directionalLight.shadow.camera.far = 5000; // 确保far值足够大以覆盖物体到光源的距离

directionalLight.shadow.mapSize.width = 4960; // 提高阴影质量
directionalLight.shadow.mapSize.height = 4960; // 提高阴影质量


const aspectRatio = window.innerWidth / window.innerHeight;
console.log(directionalLight.shadow.camera)
const ambientLight = new THREE.AmbientLight(0x404040);
const cam = directionalLight.shadow.camera;
camera = new THREE.PerspectiveCamera(75, aspectRatio, 1, 60000);
camera.position.set(0, 0, 600); // 设置相机位置
const cameraHelper2 = new THREE.CameraHelper( cam );
cameraHelper2.visible = true;

scene = new THREE.Scene();
scene.add( cameraHelper2 );
// cameraHelper.visible = true;
// scene.add( cameraHelper );
// 光源
let x_axis=0
let y_axis=0
let z_axis=0



scene.add(directionalLight);
const helper = new THREE.DirectionalLightHelper( directionalLight,1);
helper.visible = true;
scene.add( helper );
init();
animate();
let Model_;

function init() {

    scene.background = new THREE.Color(0x8FBCD4); // 背景色



    const helper2 = new THREE.DirectionalLightHelper( directionalLight );
    helper2.visible = true;
    // scene.add( helper2 );
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.domElement.style.position='absolute'
    document.body.appendChild(renderer.domElement);



    // const ambientLight = new THREE.AmbientLight(0xcccccc, 0.4);
    // scene.add(ambientLight);

    // directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);


    document.getElementById('lightSliderx').addEventListener('input', function(event) {
        const angle = event.target.value;
        updateLightAnglex(angle);
    });
    document.getElementById('lightSlidery').addEventListener('input', function(event) {
        const angle = event.target.value;
        updateLightAngley(angle);
    });
    document.getElementById('lightSliderz').addEventListener('input', function(event) {
        const angle = event.target.value;
        updateLightAnglez(angle);
    });
    const material = new THREE.MeshStandardMaterial({
        color: 0xff0000, // 红色
        roughness: 0.5, // 粗糙度
        metalness: 0.5, // 金属感
    });
    material.castShadow=true
    material.receiveShadow = true;
    const loader = new OBJLoader();
    const floorGeometry = new THREE.PlaneGeometry(2000,2000)
    const material_plane = new THREE.MeshPhysicalMaterial({
        color:0x808080,
        side:THREE.DoubleSide,
        metalness:0,
        roughness:0.1
    })



    // plane.receiveShadow = true; // 允许接收阴影

    // scene.add(plane);
    loader.load('q.obj', function (object) {
        object.traverse((child) => {
            // console.log(child)
            child.material = material;
            child.castShadow = true; // 使模型投射阴影
            child.receiveShadow = true; // 使模型接收阴影
        });
        object.rotation.y = Math.PI ;
        // object.rotation.z = Math.PI / 2;
        object.rotation.x = Math.PI / 2;
        const bbox = new THREE.Box3().setFromObject(object);
        const size = bbox.getSize(new THREE.Vector3());
        const center = bbox.getCenter(new THREE.Vector3());
        camera.lookAt(center);
        const maxDimension = Math.max(size.x, size.y, size.z);
        controls.maxDistance = maxDimension * 10;

        controls.target = center;

        console.log(center,"center_obj")
        controls.update();
        x_axis=center.x
        y_axis=center.y
        z_axis=center.z
        directionalLight.position.x=center.x+1500
        directionalLight.position.y=center.y+1500
        directionalLight.position.z=center.z+1500
        directionalLight.target.position.x=center.x
        directionalLight.target.position.y=center.y
        directionalLight.target.position.z=center.z


        console.log(directionalLight.position)
        // 计算尺寸（宽度、高度、深度）
        const width = bbox.max.x - bbox.min.x;
        const height = bbox.max.y - bbox.min.y;
        const depth = bbox.max.z - bbox.min.z;

        // 输出尺寸到控制台
        console.log(`Width: ${width}, Height: ${height}, Depth: ${depth}`,"obj")




        const plane = new THREE.Mesh(floorGeometry,material_plane)
        plane.geometry = new THREE.PlaneGeometry(width*2, depth*2);

        // 调整平面位置以匹配OBJ模型底部
        plane.position.x = bbox.min.x + width / 2;
        plane.position.z = bbox.min.z + depth / 2;
        plane.position.y = bbox.min.y+20 ; // 根据实际需要可能需要调整

        object.castShadow = true; // 使模型投射阴影
        object.receiveShadow = true; // 使模型接收阴影
        scene.add(object);
        Model_ = object;
        const bbox_plane = new THREE.Box3().setFromObject(plane);
        plane.rotation.x = Math.PI / 2;
        // 计算尺寸（宽度、高度、深度）
        const width2 = bbox_plane.max.x - bbox_plane.min.x;
        const height2 = bbox_plane.max.y - bbox_plane.min.y;
        const depth2 = bbox_plane.max.z - bbox_plane.min.z;
        plane.castShadow=true
        plane.receiveShadow=true
        // 输出尺寸到控制台
        console.log(`Width: ${width2}, Height: ${height2}, Depth: ${depth2}`,"plane");
        // const bbox = new THREE.Box3().setFromObject(object);
        const size2 = bbox_plane.getSize(new THREE.Vector3());
        const center2 = bbox_plane.getCenter(new THREE.Vector3());
        // camera.lookAt(center);
        const maxDimension2 = Math.max(size2.x, size2.y, size2.z);
        controls.maxDistance = maxDimension2 * 10;
        // controls.target = center2;
        console.log(center2,"center_plane")

        // plane.position.y = object.position.y;
        console.log(plane)
        console.log(object)
        scene.add(plane)
        console.log(scene)

    });


    controls = new OrbitControls(camera, renderer.domElement);
    controls.minDistance = 10;
    controls.maxDistance = 1000; // 最大距离
    renderer.domElement.addEventListener('click', onClick, false);
    renderer.shadowMap.enabled = true; // 开启阴影
    renderer.shadowMap.type = THREE.PCFSoftShadowMap; // 阴影平滑类型
    raycaster = new THREE.Raycaster();
    window.addEventListener('resize', onWindowResize, false);
}
function createTimeSeries(list) {
    const totalMinutes = 24 * 60; // 一天总共有1440分钟
    const interval = totalMinutes / list.length; // 根据列表长度计算时间间隔
    let timeSeries = [];

    for (let i = 0; i < list.length; i++) {
        // 计算每个时间点
        const minutes = Math.round(interval * i);
        const hours = Math.floor(minutes / 60);
        const mins = minutes % 60;

        // 格式化时间为 HH:mm 格式
        const formattedTime = `${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}`;
        timeSeries.push(formattedTime);
    }

    return timeSeries;
}

function onClick(event) {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObject(Model_, true);

    if (intersects.length > 0) {
        const oldContainer = document.getElementById('canvasContainer');
        if (oldContainer) {
            document.body.removeChild(oldContainer);
        }
        let light_list=[]
        clickCoordinates.copy(intersects[0].point);

        let reflectance

        console.log('点击坐标:', clickCoordinates);
        // console.log('光线反射值:', reflectance);
        const step = 5; // 或根据需要调整
        let currentValue=0

// 设置间隔时间（毫秒）
        const intervalTime = 1; // 每100毫秒移动一次

// 创建一个定时器，逐步增加滑块的值
        const interval = setInterval(() => {
            // 增加当前值
            currentValue += step;

            // 检查是否达到最大值
            if (currentValue > parseInt(360)) {
                // console.log(`Reached max value: ${slider.max}`);
                clearInterval(interval); // 停止定时器
                console.log(light_list)


                // 创建新的容器
                var container = document.createElement('div');
                container.id = 'canvasContainer';
                container.style.width = '300px';
                container.style.height = '300px';
                container.style.position = 'absolute';
                container.style.left = event.pageX + 'px';
                container.style.top = event.pageY + 'px';
                container.style.zIndex='999'
                container.style.backgroundColor = '#FFFFFF'; //
                // 创建新的Canvas元素
                var canvas = document.createElement('canvas');
                canvas.id = 'dynamicCanvas';

                container.appendChild(canvas);
                document.body.appendChild(container);

                var ctx = canvas.getContext('2d');
                // 使用Chart.js绘制折线图
                var myChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: createTimeSeries(light_list),
                        datasets: [{
                            label: 'Light strength',
                            data: light_list,
                            fill: false,
                            borderColor: 'rgb(75, 192, 192)',
                            tension: 0.1
                        }]
                    },
                    options: {
                        maintainAspectRatio: false, // 确保图表大小符合容器大小
                        responsive: true // 让图表响应容器大小的变化
                    }
                });

            } else {
                updateLightAngle(currentValue)
                reflectance = calculateReflectance(intersects[0]);
                light_list.push(reflectance)
                // slider.value = currentValue; // 更新滑块的值
                // console.log(`Current slider value: ${currentValue}`); // 在控制台输出当前值
            }
        }, intervalTime);


    }}

function calculateReflectance(intersection) {
    // 获取法线
    const normal = intersection.normal.clone();

    // 获取到光源的向量
    const lightDirection = new THREE.Vector3();
    // directionalLight.getWorldDirection(lightDirection);
    // console.log(lightDirection)
    // console.log(directionalLight)
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
    helper.update();
    render();
}
function updateLightAngle(angle) {
    directionalLight.position.x=x_axis+angle*100
    directionalLight.position.y=y_axis+angle*100
    directionalLight.position.z=z_axis+angle*100
    // const radians = angle * (Math.PI / 180);
    // directionalLight.position.x = Math.cos(radians);
    // directionalLight.position.z = Math.sin(radians);
    render();
}
function updateLightAnglex(angle) {

    directionalLight.position.x=x_axis+angle*100
    directionalLight.target.position.x=x_axis
    // directionalLight.position.y=y_axis+angle*100
    // directionalLight.position.z=z_axis+angle*100
    // const radians = angle * (Math.PI / 180);
    // directionalLight.position.x = Math.cos(radians);
    // directionalLight.position.z = Math.sin(radians);
    render();
}
function updateLightAngley(angle) {
    // directionalLight.position.x=x_axis+angle*100
    directionalLight.position.y=y_axis+angle*100
    directionalLight.target.position.y=y_axis
    // directionalLight.position.z=z_axis+angle*100
    // const radians = angle * (Math.PI / 180);
    // directionalLight.position.x = Math.cos(radians);
    // directionalLight.position.z = Math.sin(radians);
    render();
}
function updateLightAnglez(angle) {
    // directionalLight.position.x=x_axis+angle*100
    // directionalLight.position.y=y_axis+angle*100
    directionalLight.position.z=z_axis+angle*100
    directionalLight.target.position.z=z_axis
    // const radians = angle * (Math.PI / 180);
    // directionalLight.position.x = Math.cos(radians);
    // directionalLight.position.z = Math.sin(radians);
    render();
}
function render() {
    cameraHelper2.update();
    helper.update();
    renderer.render(scene, camera);
    // console.log(scene)
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}