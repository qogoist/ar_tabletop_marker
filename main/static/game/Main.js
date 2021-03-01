"use strict";
var Game;
(function (Game) {
    var ƒ = FudgeCore;
    window.addEventListener("load", hdnLoad);
    Game.url = window.location.origin;
    let viewport;
    let graph;
    let tank;
    let player;
    async function hdnLoad(_event) {
        /* GET PLAYER OBJECT FROM SERVER */
        const res = await fetch(window.location.href, { method: "POST" });
        player = await res.json();
        console.log("Player:");
        console.log(player);
        /* FUDGE INITIALIZATION */
        const canvas = document.querySelector("canvas");
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        graph = new ƒ.Node("Graph");
        tank = generateMap();
        graph.addChild(tank);
        createLights();
        let cmpCamera = new ƒ.ComponentCamera();
        cmpCamera.backgroundColor = new ƒ.Color(1, 1, 1, 1);
        cmpCamera.pivot.translate(new ƒ.Vector3(0, 10, 4));
        cmpCamera.pivot.lookAt(ƒ.Vector3.ZERO());
        viewport = new ƒ.Viewport();
        viewport.initialize("Viewport", graph, cmpCamera, canvas);
        viewport.draw();
        console.log(graph);
        // Hud.start();
        document.querySelector("#rotate_right").addEventListener("click", hdnClick);
        document.querySelector("#rotate_left").addEventListener("click", hdnClick);
        ƒ.Loop.addEventListener("loopFrame" /* LOOP_FRAME */, hndLoop);
        ƒ.Loop.start(ƒ.LOOP_MODE.TIME_GAME, 120);
    }
    function hndLoop(_event) {
        viewport.draw();
    }
    async function hdnClick(_event) {
        const element = _event.currentTarget;
        const turret = tank.getChild(0);
        let rotation;
        if (element.id === "rotate_left") {
            rotation = new ƒ.Vector3(0, 15, 0);
        }
        if (element.id === "rotate_right") {
            rotation = new ƒ.Vector3(0, -15, 0);
        }
        turret.cmpTransform.local.rotate(rotation);
        const currentRotation = turret.cmpTransform.local.rotation.y;
        const res = await fetch(`${Game.url}/${player.id}/rotate:${currentRotation}`, {
            method: "POST",
        });
        if (res.status == 200)
            return;
    }
    function generateMap() {
        let tank = new ƒ.Node("Tank");
        let meshTank = new ƒ.MeshCube();
        let cmpTank = new ƒ.ComponentMesh(meshTank);
        tank.addComponent(cmpTank);
        cmpTank.pivot.scale(new ƒ.Vector3(2, 0.5, 3));
        let material = new ƒ.Material("Tank", ƒ.ShaderFlat, new ƒ.CoatColored(ƒ.Color.CSS("Pink")));
        let cmpMaterial = new ƒ.ComponentMaterial(material);
        tank.addComponent(cmpMaterial);
        let cmpTransformTank = new ƒ.ComponentTransform(ƒ.Matrix4x4.IDENTITY());
        tank.addComponent(cmpTransformTank);
        let turret = new ƒ.Node("Turret");
        let meshTurret = new ƒ.MeshSphere("Turret", 12, 12);
        let cmpTurret = new ƒ.ComponentMesh(meshTurret);
        turret.addComponent(cmpTurret);
        let cmpMaterialTurret = new ƒ.ComponentMaterial(material);
        turret.addComponent(cmpMaterialTurret);
        let cmpTransformTurret = new ƒ.ComponentTransform(ƒ.Matrix4x4.IDENTITY());
        turret.addComponent(cmpTransformTurret);
        turret.cmpTransform.local.translate(new ƒ.Vector3(0, 0.4, 0));
        let gun = new ƒ.Node("Gun");
        let materialGun = new ƒ.Material("Gun", ƒ.ShaderFlat, new ƒ.CoatColored(ƒ.Color.CSS("Lightgray")));
        let cmpMaterialGun = new ƒ.ComponentMaterial(materialGun);
        gun.addComponent(cmpMaterialGun);
        let meshGun = new ƒ.MeshCube();
        let cmpMeshGun = new ƒ.ComponentMesh(meshGun);
        gun.addComponent(cmpMeshGun);
        cmpMeshGun.pivot.scale(new ƒ.Vector3(0.2, 0.2, 1.5));
        let cmpTransformGun = new ƒ.ComponentTransform(ƒ.Matrix4x4.IDENTITY());
        gun.addComponent(cmpTransformGun);
        gun.cmpTransform.local.translate(new ƒ.Vector3(0, 0.1, 0.5));
        turret.addChild(gun);
        tank.addChild(turret);
        // tank.cmpTransform.local.scale(ƒ.Vector3.ONE(2));
        return tank;
    }
    function createLights() {
        let cmpLightAmbient = new ƒ.ComponentLight(new ƒ.LightAmbient(new ƒ.Color(0.1, 0.1, 0.1)));
        let cmpLightDirection = new ƒ.ComponentLight(new ƒ.LightDirectional(new ƒ.Color(1, 1, 1)));
        cmpLightDirection.pivot.lookAt(new ƒ.Vector3(-10, -10, 0));
        graph.addComponent(cmpLightAmbient);
        graph.addComponent(cmpLightDirection);
    }
})(Game || (Game = {}));
//# sourceMappingURL=Main.js.map