let shooter;
let lasers = [];
let enemies = [];
let enemySpeed = 1;
let moveDown = false;
let rows = 5;
let shooterImg;
let laserImg;
let song;
let reply;
let cheerImg;
let enemyLasers = [];

function preload() {
  song = loadSound('audiomass.jpg');
  reply = loadSound('not my name qb.jpg');
  shooterImg = loadImage('https://deckard.openprocessing.org/user504878/visual2563965/h5ba89366a252f1b4d7a2c0b91a8e1d37/not%20my%20name%20quater%20back!.png');
  laserImg = loadImage('https://deckard.openprocessing.org/user504878/visual2563965/h5ba89366a252f1b4d7a2c0b91a8e1d37/thing%20for%20cheer%20to%20catch%20(real).png');
  cheerImg = loadImage('cheer.png');
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  shooter = new Shooter(width / 2, height - 30);
  createEnemies();
}

function draw() {
  background(0);
  shooter.update();
  shooter.display();
  for (let i = lasers.length - 1; i >= 0; i--) {
    lasers[i].update();
    lasers[i].display();
    if (lasers[i].y < 0) {
      lasers.splice(i, 1);
    }
  }
  for (let enemy of enemies) {
    enemy.move();
    enemy.show();
    enemy.shoot();
  }
  for (let i = enemyLasers.length - 1; i >= 0; i--) {
    enemyLasers[i].update();
    enemyLasers[i].display();
    if (enemyLasers[i].hits(shooter)) {
      console.log("Shooter hit by enemy laser!");
      enemyLasers.splice(i, 1);
    }
    if (enemyLasers[i].y > height) {
      enemyLasers.splice(i, 1);
    }
  }
  for (let i = enemies.length - 1; i >= 0; i--) {
    let enemy = enemies[i];
    for (let j = lasers.length - 1; j >= 0; j--) {
      if (enemy.hits(lasers[j])) {
        enemies.splice(i, 1);
        lasers.splice(j, 1);
        song.play();
        enemySpeed *= Math.max(1, -Math.log10(Math.abs(enemySpeed) + 1) + 1.5);
        break;
      }
    }
  }
}

class Shooter {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.size = 50;
    this.cooldownTime = 400;
    this.lastShotTime = 0;
  }

  update() {
    if (keyIsDown(LEFT_ARROW)) {
      this.x -= 5;
    }
    if (keyIsDown(RIGHT_ARROW)) {
      this.x += 5;
    }
    this.x = constrain(this.x, 0, width - this.size);
  }

  display() {
    imageMode(CENTER);
    image(shooterImg, this.x, this.y, this.size * 2, this.size * 2);
  }

  shoot() {
    let currentTime = millis();
    if (currentTime - this.lastShotTime > this.cooldownTime) {
      lasers.push(new Laser(this.x + this.size / 2, this.y));
      this.lastShotTime = currentTime;
    }
  }
}

class Laser {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.width = 5;
    this.height = 10;
  }

  update() {
    this.y -= 5;
  }

  display() {
    imageMode(CENTER);
    image(laserImg, this.x, this.y, this.width * 5, this.height * 4);
  }
}

function keyPressed() {
  if (key === ' ') {
    shooter.shoot();
  }
}

class Enemy {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.size = 30;
    this.lastShotTime = 0;
    this.shootCooldown = random(1500, 3000);
  }

  move() {
    this.x += enemySpeed;
    if (this.x + this.size >= width || this.x - this.size <= 0) {
      for (let enemy of enemies) {
        enemy.y += 10;
      }
      enemySpeed *= -1;
    }
  }

  show() {
    imageMode(CENTER);
    image(cheerImg, this.x, this.y, this.size * 2, this.size * 2);
  }

  shoot() {
    let currentTime = millis();
    if (currentTime - this.lastShotTime > this.shootCooldown) {
      enemyLasers.push(new EnemyLaser(this.x, this.y + this.size));
      this.lastShotTime = currentTime;
    }
  }

  hits(bullet) {
    return (
      bullet.x > this.x - this.size / 2 &&
      bullet.x < this.x + this.size / 2 &&
      bullet.y > this.y - this.size / 2 &&
      bullet.y < this.y + this.size / 2
    );
  }
}

function createEnemies() {
  let cols = 12;
  for (let i = 0; i < cols; i++) {
    for (let j = 0; j < rows; j++) {
      enemies.push(new Enemy(i * (width / cols) + (width / cols) / 2, j * 60 + 30));
    }
  }
}

class EnemyLaser {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.width = 5;
    this.height = 10;
    this.speed = 5;
  }

  update() {
    this.y += this.speed;
  }

  display() {
    imageMode(CENTER);
    image(laserImg, this.x, this.y, this.width * 5, this.height * 4);
  }

  hits(shooter) {
    return (
      shooter.x < this.x + this.width / 2 &&
      shooter.x + shooter.size > this.x - this.width / 2 &&
      shooter.y < this.y + this.height / 2 &&
      shooter.y + shooter.size > this.y - this.height / 2
    );
  }
}
