
    var normalizer = 2;
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext("2d");

    var row = 33;
    var col = 20; 
    var xRes = canvas.width / row;
    var yRes = canvas.height / col;
    console.log("hello");
    var x = 0; 
    function drawSpectogram(data){
      console.log("x: "+x);
      //Draw the spectrogram  
      for (var y = data.length-1; y >= 0; y--) {
          var value = Math.floor(data[y]);
          var hue = 140 //+(Math.abs(value)/6);
          var bri = value / normalizer;
          ctx.fillStyle = 'hsl('+ hue +',100%,'+bri+'%)';
          ellipse(ctx,xRes * x, yRes * y, xRes/2, yRes/2);
          //ctx.fillRect(xRes * x, yRes * y, xRes, yRes);
        }
        
        if(x >row-2) x = 0;
        else x++;

      }
    

    function mapRange (value, a, b, c, d) {
      value = (value - a) / (b - a);
      return c + value * (d - c);
    }

    function ellipse(context, cx, cy, rx, ry){
        context.save(); // save state
        context.beginPath();

        context.translate(cx-rx, cy-ry);
        context.scale(rx, ry);
        context.arc(1, 1, 1, 0, 2 * Math.PI, false);

        context.restore(); // restore to original state
        context.fill();
}