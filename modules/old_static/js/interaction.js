

   $(document).ready(function(){

    var timeOut;
      // Toggle mechanic
      $(".toggle").mousedown(function(){
        var msg = $(this).attr('id');
        timeOut=setInterval(function() {
           console.log("send data");
           socket.emit('msgEvent', {data: msg});
        }, 100);
      })

      $(".toggle").mouseup(function(){
        clearInterval(timeOut)
      })

      //train btn
      $("#train").mousedown(function(){
        socket.emit('msgEvent',{data:"train"});
      })

      /*
      //Reset btn
       $("#reset").mousedown(function(){
        socket.emit('msgEvent',{data:"reset"});
      })
      */

      //Menu btn
      var showMenu = false;
      $(".icon-wrapper").click(function(){
      	if(!showMenu){
	        $(".menu").animate({
	          top: '-=160'
	        },700,function(){
	        	showMenu = true;
	        })
	    }
	    else{
	    	$(".menu").animate({
	         	top: '+=160'
	        },700,function(){
	        	showMenu = false;
	        })
	    }
      });
});