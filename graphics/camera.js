function Camera() {
    // direction: E:0, N:1, W:2, S:3
    this.e = vec3.create();
    this.d = 0;
    this.Mper = mat4.create();
    this.Mobjview = mat4.create();
    this.MfixedObjview = mat4.create();
    this.targetE = vec3.create();
    this.targetD = 0;
    this.eFrame = 0;
    this.dFrame = 0;
}

// prototype object chains allow objects to inherit features from one another

Camera.prototype.canMove = function(d, maze) {
    var x = this.targetE[0];
    var y = this.targetE[1];
    var dx = d[0];
    var dy = d[1];
    x = x + dx;
    y = y + dy;
    return x >= 0 && y >= 0 &&
           x < maze.length && y < maze[0].length &&
           maze[x][y] != 1;
};

Camera.prototype.updateEyeMatrix = function() {
    var angle = ROTATE * this.d;
    var east = vec3.fromValues(1, 0, 0);
    var dir = vec3.create();
    vec3.rotateZ(dir, east, dir, angle);
    // vec3.add(dir, vec3.fromValues(0,0,0.3),dir);
    mat4.lookAt(this.MfixedObjview, vec3.create(), dir, up);
    var eyePos = vec3.fromValues(0.5, 0.5, 0);
    vec3.add(eyePos, this.e, eyePos);
    vec3.add(dir, dir, eyePos);
    mat4.lookAt(this.Mobjview, eyePos, dir, up);
    mat4.perspective(this.Mper, getFov(), 4.0/3.0, 0.1, 100.0);
};

Camera.prototype.moveEye = function() {
    // update current position, direction, and matrix
    var height = getEyeHeight();
    this.targetE[2] = height;
    this.e[2] = height;
    if (this.eFrame > 1){
        var diff = vec3.create();
        vec3.sub(diff, this.targetE, this.e);
        vec3.scale(diff, diff, 1.0 / this.eFrame);
        vec3.add(this.e, this.e, diff);
        this.eFrame -= 1;
    }else if (this.eFrame > 0){
        this.e[0] = this.targetE[0];
        this.e[1] = this.targetE[1];
        this.eFrame -= 1;
    }
    if (this.dFrame > 1){
        var diff = this.targetD - this.d;
        this.d += diff * (1.0 / this.dFrame);
        this.dFrame -= 1;
    }else if (this.dFrame > 0){
        this.d = this.targetD;
        this.dFrame -= 1;
    }
};

Camera.prototype.initEye = function(maze) {
    var start = maze.startPosition;
    vec3.set(this.e, start[0], start[1], getEyeHeight());
    vec3.set(this.targetE, start[0], start[1], getEyeHeight());
    this.d = maze.startHeading;
    this.targetD = maze.startHeading;
};

Camera.prototype.updateEye = function(dir, eps) {
        // add increment
    if (dir == 37) { // 'left'
        // add increment
        this.targetD = (this.targetD + 1)
        this.dFrame = frameCap;
    }

    if (dir == 38) { // 'up'
        var d = directions[posMod(this.targetD, 4)];
        if(this.canMove(d, maze.data)){
            vec3.add(this.targetE, this.targetE, d);
            this.eFrame = frameCap;
        }
    }

    if (dir == 39) { // 'right'
        this.targetD = (this.targetD - 1);
        this.dFrame = frameCap;
    }

    if (dir == 40) { // 'down'
        var d = vec3.create();
        vec3.scale(d, directions[posMod(this.targetD, 4)], -1);
        if(this.canMove(d, maze.data)){
            vec3.add(this.targetE, this.targetE, d);
            this.eFrame = frameCap;
        }
    }
};
