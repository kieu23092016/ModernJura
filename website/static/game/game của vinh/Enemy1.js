class Enemy1 extends Phaser.GameObjects.Sprite {
    constructor(scene){
        var x = config.width - 50;
        var y = config.height;

        super(scene, x, y, "ship");

        scene.add.existing(this);

        this.play("ship1_anim");
        scene.enemies.add(this);

    }

    update() {
        this.y += 1;
        if (this.y > config.height) {
            this.y = 0;
            var randomX = Phaser.Math.Between(0, config.width);
            this.x = randomX;
        }
    }
}