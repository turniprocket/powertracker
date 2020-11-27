let partyElem = document.getElementById('party');
let partyHiddenElem = document.getElementById('party_hidden');

partyElem.addEventListener('keyup', function(){
    suggestions(partyElem);
});

document.onclick = function(event) {
    switch(event.target.className) {
        case 'partyName':
            partyElem.value = event.target.innerText;
            partyHiddenElem.value = event.target.id;
            document.getElementById('partyList').remove();
            break;
        case 'form-control':
            let elms = document.getElementsByClassName('autoComplete');
            for (let elm of elms) {
                elm.remove();
            }
            break;
        default:
            break;
    }
};