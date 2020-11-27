let governmentElem = document.getElementById('government');
let governmentHiddenElem = document.getElementById('government_hidden');
let heldByElem = document.getElementById('held_by');
let heldByHiddenElem = document.getElementById('held_by_hidden');

governmentElem.addEventListener('keyup', function() {
    suggestions(governmentElem);
});
heldByElem.addEventListener('keyup', function() {
    suggestions(heldByElem);
});

document.onclick = function(event) {
    switch(event.target.className) {
        case 'governmentName':
            governmentElem.value = event.target.innerText;
            governmentHiddenElem.value = event.target.id;
            document.getElementById('governmentList').remove();
            break;
        case 'held_byName':
            heldByElem.value = event.target.innerText;
            heldByHiddenElem.value = event.target.id;
            document.getElementById('held_byList').remove();
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