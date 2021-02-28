"use strict";
var Game;
(function (Game) {
    var ƒ = FudgeCore;
    window.addEventListener("load", hdnLoad);
    Game.url = "http://" + window.location.host;
    let viewport;
    let graph;
    function hdnLoad(_event) {
        const canvas = document.querySelector("canvas");
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        graph = new ƒ.Node("Graph");
        graph.addChild(generateMap());
        let cmpCamera = new ƒ.ComponentCamera();
        cmpCamera.pivot.translate(new ƒ.Vector3(0, 20, 10));
        cmpCamera.pivot.lookAt(ƒ.Vector3.ZERO());
        viewport = new ƒ.Viewport();
        viewport.initialize("Viewport", graph, cmpCamera, canvas);
        viewport.draw();
        Game.Hud.start();
        document.querySelector("#counter").addEventListener("click", hdnClick);
        ƒ.Loop.addEventListener("loopFrame" /* LOOP_FRAME */, hndLoop);
        ƒ.Loop.start(ƒ.LOOP_MODE.TIME_GAME, 120);
    }
    function hndLoop(_event) {
        viewport.draw();
    }
    async function hdnClick(_event) {
        const response = await fetch(Game.url + "/add");
        const counter = await response.json();
        Game.gameState.clicks = counter;
    }
    function generateMap() {
        let map = new ƒ.Node("Map");
        let mesh = new ƒ.MeshQuad();
        let cmpMesh = new ƒ.ComponentMesh(mesh);
        map.addComponent(cmpMesh);
        let material = new ƒ.Material("Map", ƒ.ShaderUniColor, new ƒ.CoatColored(ƒ.Color.CSS("WHITE")));
        let cmpMaterial = new ƒ.ComponentMaterial(material);
        map.addComponent(cmpMaterial);
        cmpMesh.pivot.scale(ƒ.Vector3.ONE(10));
        cmpMesh.pivot.rotateX(-90);
        return map;
    }
})(Game || (Game = {}));
//# sourceMappingURL=Main.js.map