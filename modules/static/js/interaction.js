    var timeOut;
    var class_to_train = 'class1'
    var record_BG = false;

  $(document).ready(function(){
    //init menu function 
    $(".menu-icon").on('click',clickMenu);

    // Toggle mechanic for buttons
    $("#canvas-wrapper").on('mousedown touchstart', function(e){
      if(predict){
        recordBtn = true;
        timeOut=setInterval(function() {
          socket.emit('msgEvent', {data: class_to_train});
        }, 100);
        e.preventDefault(); //prevent native mobile action
      }
    });

    $("#canvas-wrapper").on('mouseup touchend', function(e){
      socket.emit('msgEvent', {data:"btn_release"});
      clearInterval(timeOut)
      recordBtn = false;
      e.preventDefault(); //prevent native mobile action
    });

    //train btn
    $("#train").on('click', function(){
      console.log("train");
      socket.emit('msgEvent',{data:"train"});
    })

    //Reset btn
    $("#reset").mousedown(function(){
      socket.emit('msgEvent',{data:"reset"});
    })

    function requestInfo(){
       socket.emit('msgEvent',{data:"get-info"});
    }   

  
    //Class to train toogle
    $("#bg-toggle").mousedown(function(){
      if(!record_BG){
        $("#bg-toggle").text("Background sound - ON");
        record_BG = true;
        class_to_train = 'class0';
      }
      else{
        $("#bg-toggle").text("Background sound - OFF");
        record_BG = false;
        class_to_train = 'class1';
      }
      requestInfo();
    })   
    
    //Prevent selection
    $('body').disableSelection();
    $("canvas").on('touchstart click', (e)=>{
      e.preventDefault();
    });
  });



  //Feedback mechanics on commands (Training and reseting)
  var timeOut_progress = null; 
  function progress_feedback(word){
    $("#header-text").text(word)
    var progress = ".";
    timeOut_progress = setInterval(function(){
      $("#header-text").text(word+progress);
      progress += "."; 
      if(progress.length > 3) progress = ".";
      },500);
  }

  //Menu btn
  var showMenu = false;
  function clickMenu(){
    if(predict){
      console.log("clicked");
      if(!showMenu){
        $(".menu").animate({
          top: '-=300%'
        },700,function(){
          showMenu = true;
        })
      }
    else{
      $(".menu").animate({
        top: '+=300%'
        },700,function(){
          showMenu = false;
        })
      }
    }
  }

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