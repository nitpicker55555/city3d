const viewer = new Cesium.Viewer("cesiumContainer", {
    timeline: false,
    animation: false,
    sceneModePicker: false,
    baseLayerPicker: false,
    // The globe does not need to be displayed,
    // since the Photorealistic 3D Tiles include terrain
    globe: false,
});

const { scene, camera } = viewer;
scene.verticalExaggeration = 3.0;

camera.setView({
    destination: new Cesium.Cartesian3(
        -2710292.813384663,
        -4360657.061518585,
        3793571.786860543
    ),
    orientation: new Cesium.HeadingPitchRoll(
        5.794062761901799,
        -0.30293409742984756,
        0.0009187098191985044
    ),
});

// Enable rendering the sky
scene.skyAtmosphere.show = true;

// Add Photorealistic 3D Tiles
try {
    const tileset = await Cesium.createGooglePhotorealistic3DTileset();
    scene.primitives.add(tileset);
} catch (error) {
    console.log(`Error loading Photorealistic 3D Tiles tileset.
    ${error}`);
}

const viewModel = {
    exaggeration: scene.verticalExaggeration,
    relativeHeight: scene.verticalExaggerationRelativeHeight,
};

function updateExaggeration() {
    scene.verticalExaggeration = Number(viewModel.exaggeration);
    scene.verticalExaggerationRelativeHeight = Number(
        viewModel.relativeHeight
    );
}

Cesium.knockout.track(viewModel);
const toolbar = document.getElementById("toolbar");
Cesium.knockout.applyBindings(viewModel, toolbar);
for (const name in viewModel) {
    if (viewModel.hasOwnProperty(name)) {
        Cesium.knockout
            .getObservable(viewModel, name)
            .subscribe(updateExaggeration);
    }
}
