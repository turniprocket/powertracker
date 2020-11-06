let candidateElem = document.getElementById('candidate');
let candidateHiddenElem = document.getElementById('candidate_hidden');
let contributorElem = document.getElementById('contributor');
let contributorHiddenElem = document.getElementById('contributor_hidden');

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
};

candidateElem.addEventListener('keyup', function() {
    if (document.getElementById('candidateList') != null) {
        document.getElementById('candidateList').remove();
    }
    if (document.getElementById('candidate').value == '') {
        return 0;
    }
    let candidateListElem = document.createElement('ul');
    candidateListElem.id = 'candidateList';
    candidateListElem.className = 'candidateList';
    candidateListElem.classList.add('autoComplete');
    candidateElem.insertAdjacentElement('afterend', candidateListElem);

    let url = new URL(base_url);
    let query = candidateElem.value;
    url.searchParams.set('q', query);
    url.searchParams.set('index', 'candidates');
    url.searchParams.set('json', 'y');

    (async () => {
        let response = await fetch(url);
        let results = await response.json();
        if (results[0] == undefined) {
            return 0;
        } else {
            for (let result of results) {
                let listElem = document.createElement('li');
                let nameElem = document.createElement('a');
                listElem.className = 'candidateListItems';
                nameElem.className = 'candidateName';
                nameElem.id = result.public_id;
                nameElem.href = '#';
                nameElem.innerText = result.first_name + ' ' + result.last_name;
                listElem.append(nameElem);
                candidateListElem.append(listElem);
            }
        }
    })()
});

contributorElem.addEventListener('keyup', function() {
    if (document.getElementById('contributorList') != null) {
        document.getElementById('contributorList').remove();
    }
    if (document.getElementById('contributor').value == '') {
        return 0;
    }
    let contributorListElem = document.createElement('ul');
    contributorListElem.id = 'contributorList';
    contributorListElem.className = 'contributorList';
    contributorListElem.classList.add('autoComplete');
    contributorElem.insertAdjacentElement('afterend', contributorListElem);

    let url = new URL(base_url);
    let query = contributorElem.value;
    url.searchParams.set('q', query);
    url.searchParams.set('index', 'contributors');
    url.searchParams.set('json', 'y');

    (async () => {
        let response = await fetch(url);
        let results = await response.json();
        if (results[0] == undefined) {
            return 0;
        } else {
            for (let result of results) {
                let listElem = document.createElement('li');
                let nameElem = document.createElement('a');
                listElem.className = 'contributorListItems';
                nameElem.className = 'contributorName';
                nameElem.id = result.public_id;
                nameElem.href = '#';
                nameElem.innerText = result.first_name + ' ' + result.last_name;
                listElem.append(nameElem);
                contributorListElem.append(listElem);
            }
        }
    })()
});