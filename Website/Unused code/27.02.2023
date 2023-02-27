import * as THREE from 'three'
import { WebGLMultisampleRenderTarget } from 'three'
import { randFloat, randInt } from 'three/src/math/MathUtils'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import GUI from 'lil-gui'

/*
Debug GUI
*/

const gui = new GUI()

const parameters = {
	color: '#ffffff',
    z_speed: 0.0025,
    x_speed: 0.0005,
    y_speed: 0.001
}

/*
Cursor
*/

/*
    The javascrip code below gets the current position of the 
    mouse and the executes the defined function. The X-Value of the 
    mouse is gets bigger to the right and Y-Value gets smaller at the
    top.
*/
const cursor = {
    x: 0,
    y: 0
}
window.addEventListener('mousemove', (event) => {
    cursor.x = event.clientX / sizes.width - 0.5
    // We invert the y value (i.e. using another -), because of how it functions within three.js
    // and thereby prevent animations, based on this value, to look unnatural.
    cursor.y = - (event.clientY / sizes.height - 0.5) 
})

/* 
Canvas
*/
const canvas = document.querySelector('canvas.webgl')

/*
Scene
*/
const scene = new THREE.Scene()


/*
Objects
*/

const geometry_torus = new THREE.TorusGeometry( 10, 0.4, 24, 96 )
const material_torus = new THREE.MeshBasicMaterial( { color: 0xf5f5f5, transparent: true, opacity: 0.5 } )
const torus = new THREE.Mesh( geometry_torus, material_torus )
torus.rotation.x = Math.PI / 2

const moonTexture = new THREE.TextureLoader().load('Images/moon.jpg');

const moon = new THREE.Mesh(
  new THREE.SphereGeometry(3, 64, 64),
  new THREE.MeshStandardMaterial({
    map: moonTexture,
  })
);

/*
Cloning the objects
*/

const moon_2 = moon.clone()
const torus_2 = torus.clone()
const moon_3 = moon.clone()
const torus_3 = torus.clone()
const moon_4 = moon.clone()
const torus_4 = torus.clone()

moon_2.position.set(15,5,25)
torus_2.position.set(15,5,25)
moon_3.position.set(-15,5,25)
torus_3.position.set(-15,5,25)
moon_4.position.set(15,5,-25)
torus_4.position.set(15,5,-25)

/*
Adding the objects
*/

scene.add(torus)
scene.add(moon)
scene.add(moon_2)
scene.add(torus_2)
scene.add(torus_3)
scene.add(moon_3)
scene.add(torus_4)
scene.add(moon_4)

/*
Adding the objects to the debug menu (only one because I am to lazy to add all)
*/

gui.add(moon.position, 'y', -20, 20, 0.05).name('Moon Y') // The last three values are the minimum value, the maximum value and the step/ precision.
gui.add(moon.position, 'x', -20, 20, 0.05).name('Moon X') // Alternativ we can use gui.add(moon.position, 'x').min(-20).max(20).step(0.05)
gui.add(moon.position, 'z', -20, 20, 0.05).name('Moon Z')
gui.add(moon, 'visible').name('Moon') // This allows toggeling the boolean that decides wheter to show or not show an Object
gui.add(moon.material, 'wireframe').name('Moon wireframe') // This allows toggeling the wireframe of an object



//gui.addColor(material_torus, '#ff00ff')

gui.add(torus.position, 'y', -20, 20, 0.05).name('Torus Y')
gui.add(torus.position, 'x', -20, 20, 0.05).name('Torus X')
gui.add(torus.position, 'z', -20, 20, 0.05).name('Torus Z')
gui.add(torus, 'visible').name('Torus')
gui.add(torus.material, 'wireframe').name('Torus wireframe') 

gui
    .addColor(parameters, 'color')
    .onChange(() => 
    {
        material_torus.color.set(parameters.color)
    })

/*
const geometry_sphere = new THREE.SphereGeometry( 2.5, 25, 50 );
const material_sphere = new THREE.MeshBasicMaterial( { color: 0xffff00 } );
const sphere = new THREE.Mesh( geometry_sphere, material_sphere );
scene.add(sphere);
*/

/*
Lights
*/

const pointLight = new THREE.PointLight(0xD2AFFF);
pointLight.position.set(3, 3, 3);

const ambientLight = new THREE.AmbientLight(0xAB90F7);
scene.add(pointLight, ambientLight);

/*
Background
*/

const spaceTexture = new THREE.TextureLoader().load('Images/Space.jpg');
scene.background = spaceTexture;


/*
Sizes
*/

const sizes = {
    width: window.innerWidth,
    height: window.innerHeight
}


// If the window is resized, we will also resize the displayed part and adjust the aspect ratios.

window.addEventListener('resize', () => 
{
    sizes.width = window.innerWidth,
    sizes.height = window.innerHeight

    // Update camera aspect ratio
    camera.aspect = sizes.width/ sizes.height
    camera.updateProjectionMatrix()

    renderer.setSize(sizes.width, sizes.height)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
})

// Adding fullscreen functionality

window.addEventListener('dblclick', () =>
{
    // Utilising webkit should also ensure compatibility with safari

    const fullscreenElement = document.fullscreenElement || document.webkitFullscreenElement

    if(!fullscreenElement)
    {
        if(canvas.requestFullscreen)
        {
            canvas.requestFullscreen()
        }
        else if(canvas.webkitRequestFullscreen)
        {
            canvas.webkitRequestFullscreen()
        }
        
    }
    else
    {
        if (document.exitFullscreen)
        {
            document.exitFullscreen()
        }
        else if(document.webkitExitFullscreen)
        {
            document.exitFullscreen()
        }
        
    }
})

/*
Camera
*/

const camera = new THREE.PerspectiveCamera(75, sizes.width/ sizes.height)
camera.position.z = 15
scene.add(camera)

/*
Orbit Control
*/

// We pass the camera and canvas as input, where the canvas is the area of the website, on which interactions with
// the camera can be triggered (e.g. camera can be moved or zoomed).
const controls = new OrbitControls(camera, canvas) 
controls.enableDamping = true

/*
Renderer
*/

const renderer = new THREE.WebGLRenderer({
    canvas: canvas
})
renderer.setSize(sizes.width, sizes.height)
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))

/*
Clock
*/

const clock = new THREE.Clock()

/*
Animation/ frame update
*/

const tick = () =>
{
    /*
    Clock
    */

    const elapsedTime = clock.getElapsedTime()
    
    /*
    Update the object
    */

    torus.rotation.z += parameters.z_speed
    torus.rotation.y += parameters.x_speed

    moon.rotation.z += parameters.z_speed
    moon.rotation.x += parameters.y_speed

    torus_2.rotation.z -= parameters.z_speed
    torus_2.rotation.y -= parameters.x_speed

    moon_2.rotation.z -= parameters.z_speed
    moon_2.rotation.x -= parameters.y_speed

    torus_3.rotation.z += parameters.z_speed
    torus_3.rotation.y += parameters.x_speed

    moon_3.rotation.z += parameters.z_speed
    moon_3.rotation.x += parameters.y_speed

    torus_4.rotation.z -= parameters.z_speed
    torus_4.rotation.y -= parameters.x_speed

    moon_4.rotation.z -= parameters.z_speed
    moon_4.rotation.x -= parameters.y_speed


  // Animation Loop
  

    // camera.position.set(cursor.x * 3.5, cursor.y * 3.5, 5) = Moving the camera according to mouse position

    /*  
        This code is substituted by the OrbitControl in Three.js

        Moving camera in a circle around the mesh. Multiplying by Math.PI * 2 allows a bigger rotation (more revolutions)
        and by 4 places the camera further from the mesh
        camera.position.set(Math.sin(cursor.x * Math.PI * 2) * 4, cursor.y * Math.PI * 2, Math.cos(cursor.x * Math.PI * 2) * 4) 
        camera.lookAt(mesh.position)
    */

    // We update the controls, for the damping to work properly
    controls.update()

    renderer.render(scene, camera)

    window.requestAnimationFrame(tick)
}

tick()