 /////////////////////////////////////////////////////////////
    // Visualization 
    var centerX, centerY;
 
    var rowLength = 20;
    var angle;
    var recordBtn = false;
    var vis = [];
    var count = 0; 
    var canvas; 

    function setup() {
      var canvasDiv = document.getElementById('canvas-wrapper')
      var width = canvasDiv.offsetWidth;
      var height = canvasDiv.offsetHeight;
      canvas = createCanvas(width, height);
      canvas.parent('canvas-wrapper');
      background(255);
      frameRate(24);

      centerY = height/2;
      centerX = width/2;
      angle = radians(360/rowLength);
      vis.push(new Visualization());
      vis[0].init();
    }

    function draw(){
      background(255);
      for(var i = 0; i < vis.length; i++){
        if(recordBtn && i == vis.length-1) vis[i].active = true;
        else vis[i].active = false;  
        vis[i].drawVisualization();
      }
      if(recordBtn){
        fill(0);
        rect( round((width-176)/2) , 4 , count*round((176/32)) , 4 ); 
      }
    } 

    function receiveData(data){
      console.log("count: " + count);
      if(count < 32){
        vis[vis.length-1].updateVisualization(data);
        count++;
      }
      else{
          if(recordBtn){
            vis.push(new Visualization());
            vis[vis.length-1].init();
            recordBtn = false;
          }
          else vis[vis.length-1].shrink = true; 
          count = 0; 
      }
    }

    function resetVisualizations(){
      vis = []; 
      vis.push(new Visualization());
      vis[0].init();
    }


    function Visualization(){

      var radius = 100;
      this.x = []; 
      this.y = [];
      this.initX = [];
      this.initY = []; 
      this.opacity = 0; 
      this.col = 0; 
      this.active = true;
      this.shrink = false; 


      this.init = function(){
        for(var i = 0; i <= rowLength-1; i++){
          this.x[i] = cos(angle * i) * radius;
          this.y[i] = sin(angle * i) * radius;
          this.initX[i] = this.x[i];
          this.initY[i] = this.y[i];
        }
      }

      this.decreaseVisualization = function(){
        for(var i = 0; i <= rowLength-1; i++){
          var distance = dist(this.x[i], this.y[i], this.initX[i], this.initY[i]);
          var decreaseVal = map(distance,5,50,1,7);
          
           if(distance > 5 ){
            this.x[i] -= cos(angle * i) * decreaseVal;
            this.y[i] -= sin(angle * i) * decreaseVal;
          }
          else{
            this.x[i] = this.initX[i]
            this.y[i] = this.initY[i];
            if(compareArray(this.x,this.initX)) this.shrink = false;  
          }
        }
      }

      this.updateVisualization = function(data){
        for(var i = 0; i < rowLength; i++){
          var val = abs(data[i])
          if(val < 20) val = 0; 
          val = val/8;
          //console.log("val: " + val + " | " + "data abs: " + abs(data[i]) + " | " + "data: " +data[i]);
          this.x[i] += cos(angle * i) * val;
          this.y[i] += sin(angle * i) * val;
        }
      }

      this.drawVisualization = function(){
        strokeWeight(4);
        if(this.active){
          this.opacity = 255;
          this.col = 0; 
        }
        else{
          if(this.opacity > 0) this.opacity -= 50; 
          else if (count == 0){
            this.col = 255; 
            this.opacity = 255; 
         }
       }
        fill(this.col,this.opacity);
        stroke(0);
        if(this.shrink) this.decreaseVisualization(); 
        
        beginShape();
        curveVertex(this.x[rowLength-1] + centerX, this.y[rowLength-1] + centerY);
        for(var i = 0; i <= rowLength-1; i++){
          curveVertex(this.x[i] + centerX, this.y[i] + centerY);
          //ellipse(this.x[i] + centerX, this.y[i] + centerY, 5, 5);
        }
        curveVertex(this.x[0] + centerX, this.y[0] + centerY);
        curveVertex(this.x[1] + centerX, this.y[1] + centerY);
        endShape();
      }
    }

    function compareArray(a,b){
      for (var i = 0; i < a.length; ++i) {
        if (a[i] !== b[i]) return false;
      }
      return true;
    }

    function windowResized() {
      var canvasDiv = document.getElementById('canvas-wrapper')
      var width = canvasDiv.offsetWidth;
      var height = canvasDiv.offsetHeight;
      resizeCanvas(width , height);
      centerY = height/2;
      centerX = width/2;
    } 