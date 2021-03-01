namespace Game {
  import ƒ = FudgeCore;

  window.addEventListener("load", hdnLoad);

  export let url: String = window.location.origin;

  let viewport: ƒ.Viewport;
  let graph: ƒ.Node;
  let tank: ƒ.Node;

  type Player = {
    id: number;
    name: string;
    position: number;
    rotation: number;
  };

  let player: Player;

  async function hdnLoad(_event: Event): Promise<void> {
    /* GET PLAYER OBJECT FROM SERVER */
    const res: Response = await fetch(window.location.href, { method: "POST" });
    player = await res.json();
    console.log("Player:");
    console.log(player);

    /* FUDGE INITIALIZATION */
    const canvas: HTMLCanvasElement = document.querySelector("canvas");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    graph = new ƒ.Node("Graph");
    tank = generateMap();
    graph.addChild(tank);
    createLights();

    let cmpCamera: ƒ.ComponentCamera = new ƒ.ComponentCamera();
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

    ƒ.Loop.addEventListener(ƒ.EVENT.LOOP_FRAME, hndLoop);
    ƒ.Loop.start(ƒ.LOOP_MODE.TIME_GAME, 120);
  }

  function hndLoop(_event: ƒ.Eventƒ): void {
    viewport.draw();
  }

  async function hdnClick(_event: Event): Promise<void> {
    const element: HTMLButtonElement = _event.currentTarget as HTMLButtonElement;
    const turret: ƒ.Node = tank.getChild(0);

    let rotation: ƒ.Vector3;

    if (element.id === "rotate_left") {
      rotation = new ƒ.Vector3(0, 15, 0);
    }

    if (element.id === "rotate_right") {
      rotation = new ƒ.Vector3(0, -15, 0);
    }

    turret.cmpTransform.local.rotate(rotation);

    const currentRotation: number = turret.cmpTransform.local.rotation.y;
    const res: Response = await fetch(
      `${url}/${player.id}/rotate:${currentRotation}`,
      {
        method: "POST",
      }
    );

    if (res.status == 200) return;
  }

  function generateMap(): ƒ.Node {
    let tank: ƒ.Node = new ƒ.Node("Tank");
    let meshTank: ƒ.MeshCube = new ƒ.MeshCube();
    let cmpTank: ƒ.ComponentMesh = new ƒ.ComponentMesh(meshTank);
    tank.addComponent(cmpTank);
    cmpTank.pivot.scale(new ƒ.Vector3(2, 0.5, 3));

    let material: ƒ.Material = new ƒ.Material(
      "Tank",
      ƒ.ShaderFlat,
      new ƒ.CoatColored(ƒ.Color.CSS("Pink"))
    );
    let cmpMaterial: ƒ.ComponentMaterial = new ƒ.ComponentMaterial(material);
    tank.addComponent(cmpMaterial);

    let cmpTransformTank: ƒ.ComponentTransform = new ƒ.ComponentTransform(
      ƒ.Matrix4x4.IDENTITY()
    );
    tank.addComponent(cmpTransformTank);

    let turret: ƒ.Node = new ƒ.Node("Turret");
    let meshTurret: ƒ.MeshSphere = new ƒ.MeshSphere("Turret", 12, 12);
    let cmpTurret: ƒ.ComponentMesh = new ƒ.ComponentMesh(meshTurret);
    turret.addComponent(cmpTurret);

    let cmpMaterialTurret: ƒ.ComponentMaterial = new ƒ.ComponentMaterial(
      material
    );
    turret.addComponent(cmpMaterialTurret);

    let cmpTransformTurret: ƒ.ComponentTransform = new ƒ.ComponentTransform(
      ƒ.Matrix4x4.IDENTITY()
    );
    turret.addComponent(cmpTransformTurret);
    turret.cmpTransform.local.translate(new ƒ.Vector3(0, 0.4, 0));

    let gun: ƒ.Node = new ƒ.Node("Gun");

    let materialGun: ƒ.Material = new ƒ.Material(
      "Gun",
      ƒ.ShaderFlat,
      new ƒ.CoatColored(ƒ.Color.CSS("Lightgray"))
    );

    let cmpMaterialGun: ƒ.ComponentMaterial = new ƒ.ComponentMaterial(
      materialGun
    );
    gun.addComponent(cmpMaterialGun);

    let meshGun: ƒ.MeshCube = new ƒ.MeshCube();
    let cmpMeshGun: ƒ.ComponentMesh = new ƒ.ComponentMesh(meshGun);
    gun.addComponent(cmpMeshGun);
    cmpMeshGun.pivot.scale(new ƒ.Vector3(0.2, 0.2, 1.5));

    let cmpTransformGun: ƒ.ComponentTransform = new ƒ.ComponentTransform(
      ƒ.Matrix4x4.IDENTITY()
    );
    gun.addComponent(cmpTransformGun);
    gun.cmpTransform.local.translate(new ƒ.Vector3(0, 0.1, 0.5));

    turret.addChild(gun);
    tank.addChild(turret);

    // tank.cmpTransform.local.scale(ƒ.Vector3.ONE(2));

    return tank;
  }

  function createLights(): void {
    let cmpLightAmbient: ƒ.ComponentLight = new ƒ.ComponentLight(
      new ƒ.LightAmbient(new ƒ.Color(0.1, 0.1, 0.1))
    );
    let cmpLightDirection: ƒ.ComponentLight = new ƒ.ComponentLight(
      new ƒ.LightDirectional(new ƒ.Color(1, 1, 1))
    );

    cmpLightDirection.pivot.lookAt(new ƒ.Vector3(-10, -10, 0));

    graph.addComponent(cmpLightAmbient);
    graph.addComponent(cmpLightDirection);
  }
}
