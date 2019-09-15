// $("navbar").hide();
//
// $("html").mousemove(function( event ) {
//     $("navbar").show();
//
//     myStopFunction();
//     myFunction();
// });
//
// function myFunction() {
//     myVar = setTimeout(function(){
//         $("navbar").hide();
//     }, 1000);
// }
// function myStopFunction() {
//     if(typeof myVar != 'undefined'){
//         clearTimeout(myVar);
//     }
// }

$('.header').click(function(){

$(this).nextUntil('tr.header').slideToggle(1000);
});
