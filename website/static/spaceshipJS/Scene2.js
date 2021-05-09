class Scene2 extends Phaser.Scene {
    constructor() {
        super("playGame");

    }

    create() {
        //background
        this.background = this.add.tileSprite(0, 0, config.width, config.height, "background");
        this.background.setOrigin(0, 0);

        //player
        this.player = this.physics.add.sprite(config.width / 2 - 8, config.height - 64, "player");
        this.player.play("thrust");
        this.cursorKeys = this.input.keyboard.createCursorKeys();
        this.player.setCollideWorldBounds(true);

        //beam
        this.spacebar = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);
        this.projectiles = this.add.group();

        //enemy
        this.Nkey = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.N);
        this.enemies = this.physics.add.group();
        this.physics.world.setBoundsCollision();

        //collision
        this.physics.add.overlap(this.player, this.enemies, this.hurtPlayer, null, this);
        this.physics.add.overlap(this.projectiles, this.enemies, this.hitEnemy, null, this);

        //audio
        this.instrumental = this.sound.add("instrumental_audio")
        this.instrumental.play({
            repeat: -1
        });
        this.shootSound = this.sound.add("shoot_audio");

        //score
        var graphics = this.add.graphics();
        graphics.fillStyle(0x000000, 1);
        graphics.beginPath();
        graphics.moveTo(0, 0);
        graphics.lineTo(config.width, 0);
        graphics.lineTo(config.width, 20);
        graphics.lineTo(0, 20);
        graphics.lineTo(0, 0);
        graphics.closePath();
        graphics.fillPath();

        this.score = 0;
        var scoreFormated = this.zeroPad(this.score, 6);
        this.scoreLabel = this.add.bitmapText(10, 5, "pixelFont", "SCORE " + scoreFormated, 16);

        //create ship
        this.createEnemy1();
        this.createEnemy2();
        this.createEnemy3();
        this.createEnemy1();
        this.createEnemy2();
        this.createEnemy3();
        this.createEnemy1();
        this.createEnemy2();
        this.createEnemy3();
    }

    createEnemy1() {
        new Enemy1(this);
    }
    createEnemy2() {
        new Enemy2(this);
    }
    createEnemy3() {
        new Enemy3(this);
    }

    hurtPlayer(player,enemy) {

        //enemy.destroy();

        enemy.y = 0;
        var randomX = Phaser.Math.Between(0, config.width);
        enemy.x = randomX;


        if (this.player.alpha < 1) {
            return;
        }

        new Explosion(this, player.x, player.y);


        player.disableBody(true, true);


        this.time.addEvent({
            delay: 1000,
            callback: this.resetPlayer,
            callbackScope: this,
            loop: false
        });
    }

    resetPlayer() {
        var x = config.width / 2 - 8;
        var y = config.height + 64;
        this.player.enableBody(true, x, y, true, true);


        this.player.alpha = 0.5;

        var tween = this.tweens.add({
            targets: this.player,
            y: config.height - 64,
            ease: 'Power1',
            duration: 1500,
            repeat: 0,
            onComplete: function () {
                this.player.alpha = 1;
            },
            callbackScope: this
        });
    }

    hitEnemy(projectile, enemy) {
        new Explosion(this, enemy.x, enemy.y);
        projectile.destroy();
        //enemy.destroy();
        enemy.y = 0;
        var randomX = Phaser.Math.Between(0, config.width);
        enemy.x = randomX;

        this.score += 15;
        var scoreFormated = this.zeroPad(this.score, 6);
        this.scoreLabel.text = "SCORE " + scoreFormated;
    }

    zeroPad(number, size) {
        var stringNumber = String(number);
        while (stringNumber.length < (size || 2)) {
            stringNumber = "0" + stringNumber;
        }
        return stringNumber;
    }


    update() {
        this.movePlayerManager();
        

        if (Phaser.Input.Keyboard.JustDown(this.Nkey)) {
            if (this.player.active) {
                this.createEnemy1();
                this.createEnemy2();
                this.createEnemy3();
            }
        }


        //beam
        if (Phaser.Input.Keyboard.JustDown(this.spacebar)) {
            if (this.player.active) {
                this.shootBeam();
            }
        }
        for (var i = 0; i < this.projectiles.getChildren().length; i++) {
            var beam = this.projectiles.getChildren()[i];
            beam.update();
        }
        for (var i = 0; i < this.enemies.getChildren().length; i++) {
            var enemy = this.enemies.getChildren()[i];
            enemy.update();
        }
    }

    /*createEnemy1() {
        new Enemy1(this);
    }
    createEnemy2() {
        new Enemy2(this);
    }
    createEnemy3() {
        new Enemy3(this);
    }*/


    shootBeam() {
        new Beam(this);
        this.shootSound.play();
    }

    movePlayerManager() {

        this.player.setVelocity(0);

        if (this.cursorKeys.left.isDown) {
            this.player.setVelocityX(-gameSettings.playerSpeed);
        } else if (this.cursorKeys.right.isDown) {
            this.player.setVelocityX(gameSettings.playerSpeed);
        }

        if (this.cursorKeys.up.isDown) {
            this.player.setVelocityY(-gameSettings.playerSpeed);
        } else if (this.cursorKeys.down.isDown) {
            this.player.setVelocityY(gameSettings.playerSpeed);
        }
    }

}
