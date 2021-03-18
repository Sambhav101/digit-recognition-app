// get canvas element from html document
var myCanvas = document.getElementById("canvas");

var user_draw = false;

// run the function when the window loads
window.onload = function () {
  if (myCanvas) {
    var isDown = false;
    var ctx = myCanvas.getContext("2d");
    var canvasX, canvasY;
    ctx.lineWidth = 30;

    // start drawing when the mouse touches the canvas until it is lifted
    $(myCanvas)
      .mousedown(function (e) {
        isDown = true;
        user_draw = true;
        ctx.beginPath();
        console.log(e.pageX - myCanvas.offsetLeft);
        console.log(e.pageY - myCanvas.offsetTop);
        canvasX = e.pageX - myCanvas.offsetLeft;
        canvasY = e.pageY - myCanvas.offsetTop;
        ctx.moveTo(canvasX, canvasY);
      })
      .mousemove(function (e) {
        if (isDown != false) {
          canvasX = e.pageX - myCanvas.offsetLeft;
          canvasY = e.pageY - myCanvas.offsetTop;
          ctx.lineTo(canvasX, canvasY);
          ctx.stroke();
        }
      })
      .mouseup(function (e) {
        isDown = false;
        ctx.closePath();
      });
  }
};

// get the encoded canvas image and send to server through ajax post
function saveImage() {
  if (!user_draw) {
    alert("Please draw something!");
  } else {
    var imgURL = myCanvas.toDataURL();
    $.ajax({
      type: "POST",
      url: "/",
      data: imgURL,

      // get the returned data from the server
      success: function (response) {
        console.log(typeof response);
        $("#answer").html(response[1]);
        $("#percent").html(response.slice(4, -1));
        $("#prediction").css("display", "block");
      },
    });
  }
}

// clear canvas when reset button is clicked
function reset() {
  var context = myCanvas.getContext("2d");
  context.clearRect(0, 0, myCanvas.width, myCanvas.height);
  $("#prediction").css("display", "none");
  user_draw = false;
}
