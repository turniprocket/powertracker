from flask import current_app

def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    #TODO make sure that items are converted to strings/text before being stored in the index to allow for partial matches
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)

def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)

def query_index(index, query, search_fields, return_fields, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    query = '*' + query + '*'
    search = current_app.elasticsearch.search(
        index=index,
        body={'query': {'query_string': {'query': query, 'fields': search_fields}},
            'from': (page - 1) * per_page, 'size': per_page})
    results = []

    for result in search['hits']['hits']:
        if return_fields[0] == '*':
            item = result['_source']
        else:
            item = {}
            for return_field in return_fields:
                item[return_field] = result['_source'][return_field]
        
        results.append(item)
    
    return results, search['hits']['total']['value']