let partyElem = document.getElementById('party');
let partyHiddenElem = document.getElementById('party_hidden');
let officeSoughtElem = document.getElementById('office_sought');
let officeSoughtHiddenElem = document.getElementById('office_sought_hidden');
let officeHeldElem = document.getElementById('office_held');
let officeHeldHiddenElem = document.getElementById('office_held_hidden');
let treasurerElem = document.getElementById('treasurer');
let treasurerHiddenElem = document.getElementById('treasurer_hidden');

partyElem.addEventListener('keyup', function() {
    suggestions(partyElem);
});
officeSoughtElem.addEventListener('keyup', function() {
    suggestions(officeSoughtElem);
});
officeHeldElem.addEventListener('keyup', function() {
    suggestions(officeHeldElem);
});
treasurerElem.addEventListener('keyup', function() {
    suggestions(treasurerElem);
});

document.onclick = function(event) {
    switch(event.target.className) {
        case 'partyName':
            partyElem.value = event.target.innerText;
            partyHiddenElem.value = event.target.id;
            document.getElementById('partyList').remove();
            break;
        case 'office_soughtName':
            officeSoughtElem.value = event.target.innerText;
            officeSoughtHiddenElem.value = event.target.id;
            document.getElementById('office_soughtList').remove();
            break;
        case 'office_held':
            officeHeldElem.value = event.target.innerText;
            officeHeldHiddenElem.value = event.target.id;
            document.getElementById('office_heldList').remove();
            break;
        case 'treasurer':
            treasurerElem.value = event.target.innerText;
            treasurerHiddenElem = event.target.id;
            document.getElementById('treasurerList');
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