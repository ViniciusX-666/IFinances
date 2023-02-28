// $(document).ready(function () {
//   $("#botao").click(function () {
//     alert("Seja bem vindo");
//   });
// });

$(document).ready(function () {
  $("#valor").mask("R$ 000000000.00",{reverse: true});
});

$(document).ready(function () {
  $("#sair").click(function () {
    $("#sair").attr("disabled", true);
    $("#sair").text("Sair");
  });
});
