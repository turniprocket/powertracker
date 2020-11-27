function suggestions(element) {
    if (document.getElementById(element.id + 'List') != null) {
        document.getElementById(element.id + 'List').remove();
    }
    if (document.getElementById(element.id).value == '') {
        return 0;
    }
    let listElem = document.createElement('ul');
    listElem.id = element.id + 'List';
    listElem.className = 'autocompleteList';
    listElem.classList.add('autocomplete');
    element.insertAdjacentElement('afterend', listElem);

    let url = new URL(base_url);
    let query = element.value;
    url.searchParams.set('q', query);
    url.searchParams.set('index', element.id);
    url.searchParams.set('json', 'y');

    (async () => {
        let response = await fetch(url);
        let results = await response.json();
        if (results[0] == undefined) {
            return 0;
        } else {
            for (let result of results) {
                let listItems = document.createElement('li');
                let nameElem = document.createElement('a');
                listItems.className = 'autocompleteListItems';
                nameElem.className = element.id + 'Name';
                nameElem.id = result.public_id;
                nameElem.href = '#';
                nameElem.innerText = result.name;
                listItems.append(nameElem);
                listElem.append(listItems);
            }
        }
    })()
};