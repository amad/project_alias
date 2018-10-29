      $.fn.extend({
        disableSelection: function() {
            this.each(function() {
                this.onselectstart = function() {
                    return false;
                };
                this.unselectable = "on";
                $(this).css('-moz-user-select', 'none');
                $(this).css('-webkit-user-select', 'none');
            });
            return this;
        }
      });
      function button_interaction(){
      var timeOut;
      // Toggle mechanic for buttons
      $(".toggle").on('mousedown touchstart', function(e){
        var msg = $(this).attr('id');
        timeOut=setInterval(function() {
           socket.emit('msgEvent', {data: msg});
        }, 100);
      })
      $(".toggle").on('mouseup touchend', function(e){
        socket.emit('msgEvent', {data:"btn_release"});
        clearInterval(timeOut)
        e.preventDefault();
      })

      //train btn
      $("#train").on('click', function(){
        console.log("train");
        socket.emit('msgEvent',{data:"train"});
      })

      
      //Reset btn
       $("#reset").mousedown(function(){
        socket.emit('msgEvent',{data:"reset"});
      })
      
    }

    function menu_interaction(){
      //Menu btn
      var showMenu = false;
      $(".icon-wrapper").on('click',function(){
        if(!showMenu){
          $(".menu").animate({
            top: '-=30%'
          },700,function(){
            showMenu = true;
          })
      }
      else{
        $(".menu").animate({
            top: '+=30%'
          },700,function(){
            showMenu = false;
          })
        }
      });
    }