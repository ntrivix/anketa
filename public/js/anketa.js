/**
 * Created by Nikol on 14.7.2017..
 */

$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});

var anketaData = {};

function populateCas(cas) {
    casId = $(cas).find(".id_cas").val();
    $(cas).find("form").each(function (key, val) {
        if (anketaData[casId] != undefined) {
            idPitanja = $(val).find(".id_pitanja").val();
            qtype = $(val).find("input[name='qtype']").val();
            if (qtype == 'P') {
                if (anketaData[casId][idPitanja] != undefined)
                    $(val).find(":radio[value="+anketaData[casId][idPitanja]+"]").attr('checked',true);
            } else {
                if (anketaData[casId][idPitanja] != undefined)
                    teks = $(val).find("textarea").val(anketaData[casId][idPitanja]);
            }
        }
    });
}

function saveAnketa() {
    cas = $(".cas.visible");
    validateCas(cas);
    localStorage.setItem($("#id_ankete").val(), JSON.stringify(anketaData));
}

function processCas(cas) {
    if (validateCas(cas)) {
        tId = $(cas).find(".id_cas").val();
        console.log("trenutni ID "+tId);
        next = $(cas).next(".cas");
        nextId = $(next).find(".id_cas").val();
        console.log("sledeci ID "+nextId);
        $("#ind_"+tId).removeClass("active");
        $("#ind_"+nextId).addClass("active");
        $(cas).removeClass("visible");
        $(cas).hide();

        $(next).removeClass("hide").show();
        $(next).addClass("visible");
        window.scrollTo(0, 0);
        return true;
    } else {
        //prikazi greske
        $(cas).effect( "shake", { times: 4, distance: 4}, 600 );
        return false;
    }
}

function validateCas(cas) {
    isValid = true;
    casId = $(cas).find(".id_cas").val();
    anketaData[casId] = {};
    $(cas).find("form").each(function (key, val) {
        idPitanja = $(val).find(".id_pitanja").val();
        qtype = $(val).find("input[name='qtype']").val();
        if (qtype == 'P'){
            checkedVal = $(val).find("input[name='p"+casId+"_"+idPitanja+"']:checked").val();
            if (checkedVal == undefined) {
                isValid = false;
            } else
                anketaData[casId][idPitanja] = checkedVal;
        } else {
            teks = $(val).find("textarea").val();
            anketaData[casId][idPitanja] = teks;
        }

    });
    return isValid;
}

$(document).ready(function () {

    savedData = JSON.parse(localStorage.getItem($("#id_ankete").val()));
    if (savedData != undefined)
        anketaData = savedData;

    $(".cas").each(function (key, val) {
        populateCas(val);
    });
    populateCas($(".cas.visible"));

    $(".next-button").click(function () {
        cas = $(this).closest(".cas");
        processCas(cas);
    });

    $(".prev-button").click(function () {
        cas = $(this).closest(".cas");
        tId = $(cas).find(".id_cas").val();
        prev = $(cas).prev(".cas");
        prevId = $(prev).find(".id_cas").val();
        $("#ind_"+tId).removeClass("active");
        $("#ind_"+prevId).addClass("active");
        $(cas).remove("visible");
        $(cas).hide();

        $(prev).removeClass("hide").show();
        $(prev).addClass("visible");
        window.scrollTo(0, 0);
    });

    $(".finish-button").click(function () {
        cas = $(this).closest(".cas");
        if (processCas(cas)){
            $.post($("#id_ankete").val()+"/submit", anketaData)
                .done(function( data ) {
                    alert("Uspesno ste zavrsili anketu!");
                }).fail(function(xhr, status, error) {
                // error handling
                console.log(status);
                console.log(error);
                });
        };
    });

    setInterval(saveAnketa, 1000);
});