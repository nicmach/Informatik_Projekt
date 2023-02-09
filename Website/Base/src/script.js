import * as THREE from 'three'
import { WebGLMultisampleRenderTarget } from 'three'
import { randFloat, randInt } from 'three/src/math/MathUtils'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

// Cursor
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

// Canvas
const canvas = document.querySelector('canvas.webgl')

// Scene
const scene = new THREE.Scene()

// Object
const geometry = new THREE.BoxGeometry(1, 1, 1)
const material = new THREE.MeshBasicMaterial({ color: 0xff0000 })
const mesh = new THREE.Mesh(geometry, material)
//mesh.position.set(0,0,0)
scene.add(mesh)

const geometry2 = new THREE.BoxGeometry(1, 1, 1)
const material2 = new THREE.MeshBasicMaterial({ color: 0xffff00 })
const mesh2 = new THREE.Mesh(geometry2, material2)
mesh2.position.set(1,1,1)
scene.add(mesh2)

const geometry3 = new THREE.BoxGeometry(1, 1, 1)
const material3 = new THREE.MeshBasicMaterial({ color: 0xffffff })
const mesh3 = new THREE.Mesh(geometry3, material3)
mesh3.position.set(-1,-1,-1)
scene.add(mesh3)



// Sizes
const sizes = {
    width: 800,
    height: 600
}

// Camera
/*
const aspectRatio = sizes.width/ sizes.height
const camera = new THREE.OrthographicCamera(
    -1 * aspectRatio,
    1 * aspectRatio,
    1,
    -1,
    0.1, // This is the near value, which...
    100 // with this far value defines the range in which we can see objects.
)
*/
const camera = new THREE.PerspectiveCamera(75, sizes.width/ sizes.height)
camera.position.z = 5
scene.add(camera)

// Orbit Control

// We pass the camera and canvas as input, where the canvas is the area of the website, on which interactions with
// the camera can be triggered (e.g. camera can be moved or zoomed).
const controls = new OrbitControls(camera, canvas) 
controls.enableDamping = true

// Renderer
const renderer = new THREE.WebGLRenderer({
    canvas: canvas
})
renderer.setSize(sizes.width, sizes.height)

// Clock
const clock = new THREE.Clock()


// Animation/ frame update

const tick = () =>
{
    // Clock
    const elapsedTime = clock.getElapsedTime()
    
    // Update the object

    mesh.position.x += randFloat(-0.005,0.005) * elapsedTime
    mesh.position.y += randFloat(-0.005, 0.005) * elapsedTime
    mesh.position.z += randFloat(-0.005, 0.005) * elapsedTime
    mesh.rotation.x += 0.0025 * elapsedTime
    mesh.rotation.y += 0.0025 * elapsedTime
    mesh.rotation.z += 0.0025 * elapsedTime

    mesh2.position.x += randFloat(-0.005,0.005) * elapsedTime
    mesh2.position.y += randFloat(-0.005, 0.005) * elapsedTime
    mesh2.position.z += randFloat(-0.005, 0.005) * elapsedTime
    mesh2.rotation.x += 0.0025 * elapsedTime
    mesh2.rotation.y += 0.0025 * elapsedTime
    mesh2.rotation.z += 0.0025 * elapsedTime

    mesh3.position.x += randFloat(-0.005,0.005) * elapsedTime
    mesh3.position.y += randFloat(-0.005, 0.005) * elapsedTime
    mesh3.position.z += randFloat(-0.005, 0.005) * elapsedTime
    mesh3.rotation.x += 0.0025 * elapsedTime
    mesh3.rotation.y += 0.0025 * elapsedTime
    mesh3.rotation.z += 0.0025 * elapsedTime
    
    // Update camera

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