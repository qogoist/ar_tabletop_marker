"use strict";
var Game;
(function (Game) {
    var ƒ = FudgeCore;
    var ƒui = FudgeUserInterface;
    class GameState extends ƒ.Mutable {
        constructor() {
            super(...arguments);
            this.clicks = 0;
        }
        reduceMutator(_mutator) { }
    }
    Game.GameState = GameState;
    Game.gameState = new GameState();
    class Hud {
        static start() {
            let domHud = document.querySelector("div#hud");
            Hud.controller = new ƒui.Controller(Game.gameState, domHud);
            Hud.controller.updateUserInterface();
        }
    }
    Game.Hud = Hud;
})(Game || (Game = {}));
//# sourceMappingURL=Hud.js.map