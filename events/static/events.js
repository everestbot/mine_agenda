$ ( documento ). pronto ( function () {

    $ ( ' .edit-event ' ). clique ( function () {
        / *   recupera o id do objeto que invoca esta rotina e popula os
            campos de 'id' (oculto), descrição e prioridade. Um dado é
            preenchida diretamente no gabarito. * /
        deixe valores =  isso . id . dividir ( ' - ' );
        $( ' #editInputId ' ). prop ( ' valor ' , valores [ 1 ]);
        $( ' #editInputEvent ' ). prop ( ' valor ' , este . texto );
        $( ' #editInputPriority ' ). prop ( ' valor ' , valores [ 2 ]);

        $ ( ' #editEvent ' ). modal ( ' toggle ' );
    }) // clique ()

}) // function ()