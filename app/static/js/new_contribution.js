let candidateElem = document.getElementById('candidate');
let candidateHiddenElem = document.getElementById('candidate_hidden');
let contributorElem = document.getElementById('contributor');
let contributorHiddenElem = document.getElementById('contributor_hidden');

candidateElem.addEventListener('keyup', function() {
    suggestions(candidateElem);
});

contributorElem.addEventListener('keyup', function() {
    suggestions(contributorElem);
});

document.onclick = function(event) {
    switch(event.target.className) {
        case 'candidateName':
            candidateElem.value = event.target.innerText;
            candidateHiddenElem.value = event.target.id;
            document.getElementById('candidateList').remove();
            break;
        case 'contributorName':
            contributorElem.value = event.target.innerText;
            contributorHiddenElem.value = event.target.id;
            document.getElementById('contributorList').remove();
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
}