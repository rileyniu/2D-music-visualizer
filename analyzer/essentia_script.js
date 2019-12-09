function readFile(files) {
    var fileReader = new FileReader();
        fileReader.readAsArrayBuffer(files[0]);
        fileReader.onload = function(e) {
            playAudioFile(e.target.result); // file = e.target.result
            //console.log(("Filename: '" + files[0].name + "'"), ( "(" + ((Math.floor(files[0].size/1024/1024*100))/100) + " MB)" ));
        }
}
function playAudioFile(file) {
    var context = new window.AudioContext();
        context.decodeAudioData(file, function(buffer) {
            var source = context.createBufferSource();
                source.buffer = buffer;
                source.loop = false;
                source.connect(context.destination);
                source.start(0); 
        });
}

// function loadDoc() {
//     var xhttp = new XMLHttpRequest();
//     xhttp.onreadystatechange = function() {
//       if (this.readyState == 4 && this.status == 200) {
//        document.getElementById("demo").innerHTML = this.responseText;
//       }
//     };
//     xhttp.open("GET", "ajax_info.txt", true);
//     xhttp.send();
// }

// $(document).ready(function(){
//     $.ajax({
//         type: "POST",
//         url: "~/essentia_python.py",
//         data: { param: text}
//     }).done(function( o ) {
//         alert('Cynthia He'); 
//     });
//   });

