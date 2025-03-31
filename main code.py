let shooter;
let lasers = [];
let enemies = [];
let enemySpeed = 1;
let moveDown = false; // Flag to move the enemies down
let rows = 5; // 5 rows of enemies
let shooterImg; // Variable to hold the custom shooter image
let laserImg; // this is the football for cheer to perform a nice catch
let song;
let reply;
let cheerImg; // Cheer image for enemies
let EnemyLaser = []; // Array to hold enemy lasers

function preload() {
  // these are audios for "nice catch cheer" and "not my name quarterback"
  song = loadSound('audiomass.jpg');
  reply = loadSound('not my name qb.jpg');
  // Load the custom PNG image for the shooter
  shooterImg = loadImage('https://deckard.openprocessing.org/user504878/visual2563965/h5ba89366a252f1b4d7a2c0b91a8e1d37/not%20my%20name%20quater%20back!.png'); // Replace with the actual path to your image
  laserImg = loadImage('https://deckard.openprocessing.org/user504878/visual2563965/h5ba89366a252f1b4d7a2c0b91a8e1d37/thing%20for%20cheer%20to%20catch%20(real).png');
  cheerImg = loadImage('cheer.png'); // This will be used for the enemy image
}

function setup() {
  createCanvas(windowWidth, windowHeight);

  // Create a shooter at the bottom of the canvas
  shooter = new Shooter(width / 2, height - 30);

  // Create enemies
  createEnemies();
}

function draw() {
  background(0);

  // Update and display the shooter
  shooter.update();
  shooter.display();

  // Update and display all lasers
  for (let i = lasers.length - 1; i >= 0; i--) {
    lasers[i].update();
    lasers[i].display();

    // Remove lasers that are off-screen
    if (lasers[i].y < 0) {
      lasers.splice(i, 1);
    }
  }

  // Update and display all enemies
  for (let enemy of enemies) {
    enemy.move();
    enemy.show();
    enemy.shoot();  // Call the shoot method for each enemy
  }

  // Update and display all enemy lasers
  for (let i = EnemyLaser.length - 1; i >= 0; i--) {
    EnemyLaser[i].update();
    EnemyLaser[i].display();

    // Check for collision with the shooter
    if (EnemyLaser[i].hits(shooter)) {
      // Handle collision (e.g., end the game, reduce health, etc.)
      console.log("Shooter hit by enemy laser!");
      // Optionally, remove the enemy laser after collision
      EnemyLaser.splice(i, 1);
    }

    // Remove lasers that are off-screen
    if (EnemyLaser[i].y > height) {
      EnemyLaser.splice(i, 1);
    }
  }

  // Check for collision between lasers and enemies
  for (let i = enemies.length - 1; i >= 0; i--) {
    let enemy = enemies[i];
    // Check for collision with each laser
    for (let j = lasers.length - 1; j >= 0; j--) {
      if (enemy.hits(lasers[j])) {
        // Remove the enemy and the laser
        enemies.splice(i, 1);
        lasers.splice(j, 1);
        song.play();
        enemySpeed *= max(1, -Math.log10(Math.abs(enemySpeed) + 1) + 1.5);
        break;
      }
    }
  }
}

// Shooter class (square that moves left and right)
class Shooter {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.size = 50; // You can adjust this based on the image size
    this.cooldownTime = 400; // Cooldown time in milliseconds (400ms = 0.4 seconds)
    this.lastShotTime = 0; // Time when the last shot was fired
  }

  update() {
    if (keyIsDown(LEFT_ARROW)) {
      this.x -= 5;
    }
    if (keyIsDown(RIGHT_ARROW)) {
      this.x += 5;
    }

    // Prevent shooter from moving off-screen
    this.x = constrain(this.x, 0, width - this.size);
  }

  display() {
    // Display the custom shooter image instead of a rectangle
    imageMode(CENTER); // This ensures the image is centered on the shooter's position
    image(shooterImg, this.x, this.y, this.size * 2, this.size * 2); // Display the image
  }

  shoot() {
    let currentTime = millis(); // Get the current time in milliseconds

    // Only shoot if the cooldown has passed since the last shot
    if (currentTime - this.lastShotTime > this.cooldownTime) {
      // Create a new laser and add it to the lasers array
      lasers.push(new Laser(this.x + this.size / 2, this.y));
      this.lastShotTime = currentTime; // Update the last shot time
    }
  }
}

// Laser class
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
    // Display the custom laser image instead of a rectangle
    imageMode(CENTER);
    image(laserImg, this.x, this.y, this.width * 5, this.height * 4); // Display the image
  }
}

// Shoot a laser when the spacebar is pressed
function keyPressed() {
  if (key === ' ') {
    shooter.shoot();
  }
}

// Enemy class
class Enemy {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.size = 30;
    this.lastShotTime = 0;  // Time of last shot
    this.shootCooldown = random(1500, 3000);  // Random cooldown between 1.5 to 3 seconds
  }

  move() {
    this.x += enemySpeed;

    // If we hit the right edge of the screen, move the enemies down and reverse direction
    if (this.x + this.size >= width || this.x - this.size <= 0) {
      for (let enemy of enemies) {
        enemy.y += 10;
      }
      enemySpeed *= -1;
    }
  }

  show() {
    imageMode(CENTER);
    image(cheerImg, this.x, this.y, this.size * 2, this.size * 2);  // Show the enemy image
  }

  shoot() {
    // Check if enough time has passed since the last shot
    let currentTime = millis();
    if (currentTime - this.lastShotTime > this.shootCooldown) {
      // Create a new enemy laser and add it to the lasers array
      EnemyLaser.push(new enemyLaser(this.x, this.y + this.size));  // Shoot from the enemy's position
      this.lastShotTime = currentTime;  // Update the last shot time
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

// Create enemies
function createEnemies() {
  let cols = 12; // Fixed number of enemies horizontally

  // Create enemies
  for (let i = 0; i < cols; i++) {
    for (let j = 0; j < rows; j++) {
      enemies.push(new Enemy(i * (width / cols) + (width / cols) / 2, j * 60 + 30));
    }
  }
}

// Enemy Laser class
class enemyLaser {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.width = 5;
    this.height = 10;
    this.speed = 5; // Speed of enemy laser
  }

  update() {
    this.y += this.speed;  // Move the laser downwards
  }

  display() {
    imageMode(CENTER);
    image(laserImg, this.x, this.y, this.width * 5, this.height * 4); // Display the laser
  }

  hits(shooter) {
    return (
      shooter.x < this.x + this.width / 2 &&
      shooter.x + shooter.size > this.x - this.width / 2 &&
      shooter.y < this.y + this.height / 2 &&
      shooter.y + shooter.size > this.y - this.height / 2
    ); // Detect collision between the laser and the shooter
  }
}
