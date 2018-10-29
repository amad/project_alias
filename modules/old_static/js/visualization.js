 /////////////////////////////////////////////////////
    // SPECTOGRAM

  var normalizer = 2;
  //Initialize slider     
  var slider = document.getElementById("myRange");
    slider.oninput = function() {
      normalizer = this.value;
      console.log(normalizer);
    }

    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext("2d");

    var resolution = 33;
    var xRes = canvas.width / resolution;
    var yRes = canvas.height / resolution;

    function drawSpectogram(data){
      //Draw the spectrogram
      for (var x = 0; x < data.length-1; x++) {
        for (var y = data[0].length-1; y > 0; y--) {

          var value = Math.floor(data[x][y]);
          var hue = 140 //+(Math.abs(value)/6);
          var bri = value / normalizer;
          ctx.fillStyle = 'hsl('+ hue +',100%,'+bri+'%)';
          ctx.fillRect(xRes * x, yRes * y, xRes, yRes);
        }
      }
    }

    function mapRange (value, a, b, c, d) {
      value = (value - a) / (b - a);
      return c + value * (d - c);
    }