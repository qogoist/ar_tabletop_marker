namespace Game {
    import ƒ = FudgeCore;

    window.addEventListener("load", hdnLoad);

    export let url: String = "http://" + window.location.host;

    let viewport: ƒ.Viewport;
    let graph: ƒ.Node;

    function hdnLoad(_event: Event): void {
        const canvas: HTMLCanvasElement = document.querySelector("canvas");
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        graph = new ƒ.Node("Graph");
        graph.addChild(generateMap());

        let cmpCamera: ƒ.ComponentCamera = new ƒ.ComponentCamera();
        cmpCamera.pivot.translate(new ƒ.Vector3(0, 20, 10));
        cmpCamera.pivot.lookAt(ƒ.Vector3.ZERO());


        viewport = new ƒ.Viewport();
        viewport.initialize("Viewport", graph, cmpCamera, canvas);

        viewport.draw();

        Hud.start();


        document.querySelector("#counter").addEventListener("click", hdnClick);

        ƒ.Loop.addEventListener(ƒ.EVENT.LOOP_FRAME, hndLoop);
        ƒ.Loop.start(ƒ.LOOP_MODE.TIME_GAME, 120);
    }

    function hndLoop(_event: ƒ.Eventƒ): void {
        viewport.draw();
    }

    async function hdnClick(_event: Event): Promise<void> {
        const response: Response = await fetch(url + "/add");
        const counter: number = await response.json();

        gameState.clicks = counter;
    }

    function generateMap(): ƒ.Node {
        let map: ƒ.Node = new ƒ.Node("Map");

        let mesh: ƒ.MeshQuad = new ƒ.MeshQuad();
        let cmpMesh: ƒ.ComponentMesh = new ƒ.ComponentMesh(mesh);
        map.addComponent(cmpMesh);

        let material: ƒ.Material = new ƒ.Material("Map", ƒ.ShaderUniColor, new ƒ.CoatColored(ƒ.Color.CSS("WHITE")));
        let cmpMaterial: ƒ.ComponentMaterial = new ƒ.ComponentMaterial(material);
        map.addComponent(cmpMaterial);

        cmpMesh.pivot.scale(ƒ.Vector3.ONE(10));
        cmpMesh.pivot.rotateX(-90);

        return map;
    }
}